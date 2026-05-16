from pathlib import Path
import re
import yaml
from .common import ValidatorResult

def validate_workflow_link(run_dir, current_step, previous_step=None, workflow_id=None, registry_path=None):
    """
    Validates the continuity and registry alignment between workflow steps.
    """
    findings = []
    failure_modes = []
    
    # 0. Registry Alignment (ADR 0008)
    if workflow_id and registry_path:
        reg_path = Path(registry_path)
        if reg_path.exists():
            try:
                reg = yaml.safe_load(reg_path.read_text(encoding="utf-8"))
                workflows = reg.get("workflows", [])
                wf = next((w for w in workflows if w["id"] == workflow_id), None)
                
                if not wf:
                    findings.append(f"Registry violation: Workflow ID '{workflow_id}' not found in registry.")
                    failure_modes.append("unregistered_workflow")
                else:
                    findings.append(f"Registry alignment verified for workflow '{workflow_id}'.")
                    
                    # Verify skill is part of this workflow
                    wf_skills = [s["skill"] for s in wf.get("steps", [])]
                    curr_skill = current_step.get("skill")
                    if curr_skill not in wf_skills:
                        findings.append(f"Registry violation: Skill '{curr_skill}' is not part of workflow '{workflow_id}'.")
                        failure_modes.append("invalid_workflow_step")
            except Exception as e:
                findings.append(f"Error reading workflow registry: {str(e)}")

    if not previous_step:
        return ValidatorResult(
            status="pass" if not failure_modes else "fail",
            validator_name="workflow_link",
            findings=findings + ["First step in workflow - no predecessor to link."],
            failure_modes=failure_modes
        )

    # 1. Physical Continuity
    prev_output = previous_step.get("artifact")
    curr_input = current_step.get("input_artifact")
    
    if curr_input and prev_output:
        if curr_input != prev_output:
            findings.append(f"Physical Continuity Break: Current input '{curr_input}' does not match previous output '{prev_output}'")
            failure_modes.append("mismatched_paths")
    
    # 2. Semantic Continuity & Thread Audit
    curr_artifact_rel = current_step.get("artifact")
    if not curr_artifact_rel:
        return ValidatorResult(
            status="fail",
            validator_name="workflow_link",
            findings=findings + ["Current step artifact path missing in manifest."],
            failure_modes=failure_modes + ["missing_manifest_entry"]
        )
        
    curr_artifact_path = Path(run_dir).parent.parent / curr_artifact_rel 
    if not curr_artifact_path.exists():
        curr_artifact_path = Path(run_dir) / curr_artifact_rel
        if not curr_artifact_path.exists():
            return ValidatorResult(
                status="fail",
                validator_name="workflow_link",
                findings=findings + [f"Output artifact not found: {curr_artifact_rel}"],
                failure_modes=failure_modes + ["missing_artifact"]
            )

    content = curr_artifact_path.read_text(encoding="utf-8")
    
    # Metadata Extraction
    frontmatter = {}
    fm_match = re.search(r"^---(.*?)---", content, re.DOTALL)
    if fm_match:
        try:
            frontmatter = yaml.safe_load(fm_match.group(1)) or {}
        except yaml.YAMLError:
            findings.append("Malformed frontmatter in output artifact.")
            failure_modes.append("malformed_metadata")

    # Traceability Audit: Intent ID / Run ID / Spec ID propagation
    # We look for ANY identifier that links the steps.
    identifiers = ["spec_id", "run_id", "intent_id", "workflow_run_id"]
    
    prev_artifact_rel = previous_step.get("artifact")
    prev_artifact_path = Path(run_dir).parent.parent / prev_artifact_rel if prev_artifact_rel else None
    
    if prev_artifact_path and prev_artifact_path.exists():
        prev_content = prev_artifact_path.read_text(encoding="utf-8")
        
        for id_key in identifiers:
            # Try to find ID in current frontmatter vs previous content/frontmatter
            curr_id = frontmatter.get(id_key)
            if not curr_id:
                # Try searching in raw content
                id_match = re.search(fr"{id_key}[:\s]+([\w-]+)", content, re.IGNORECASE)
                if id_match:
                    curr_id = id_match.group(1)
            
            if curr_id:
                if curr_id in prev_content:
                    findings.append(f"Semantic Thread Verified: Identifier '{id_key}={curr_id}' propagated from previous step.")
                    break # One valid link is enough for base continuity
        else:
            findings.append("Semantic Thread BREAK: No shared identifiers (spec_id, run_id, etc.) found between steps.")
            failure_modes.append("missing_semantic_thread")

    status = "pass" if not failure_modes else "fail"
    return ValidatorResult(
        status=status,
        validator_name="workflow_link",
        findings=findings,
        failure_modes=failure_modes,
        artifact_path=str(curr_artifact_rel)
    )
