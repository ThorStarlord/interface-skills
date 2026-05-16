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
    
    # 2. Semantic Continuity & Thread Audit (ADR 0008 Hardening)
    curr_artifact_rel = current_step.get("artifact")
    if not curr_artifact_rel:
        return ValidatorResult(
            status="fail",
            validator_name="workflow_link",
            findings=findings + ["Current step artifact path missing in manifest."],
            failure_modes=failure_modes + ["missing_manifest_entry"]
        )
        
    # Improved Path Resolution
    def resolve_path(base, rel):
        if not rel: return None
        candidates = [
            Path(base) / rel,
            Path(base).parent / rel,
            Path(base).parent.parent / rel,
            Path(rel)
        ]
        for p in candidates:
            if p.exists() and p.is_file():
                return p
        return None

    curr_artifact_path = resolve_path(run_dir, curr_artifact_rel)
    if not curr_artifact_path:
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
    identifiers = ["spec_id", "run_id", "intent_id", "workflow_run_id", "parent_run_id"]
    
    prev_artifact_rel = previous_step.get("artifact")
    prev_artifact_path = resolve_path(run_dir, prev_artifact_rel)
    
    if prev_artifact_path:
        prev_content = prev_artifact_path.read_text(encoding="utf-8")
        
        matches = []
        for id_key in identifiers:
            # Try to find ID in current frontmatter vs previous content/frontmatter
            curr_id = frontmatter.get(id_key)
            if not curr_id:
                # Try searching in raw content
                id_match = re.search(fr"{id_key}[:\s]+([\w-]+)", content, re.IGNORECASE)
                if id_match:
                    curr_id = id_match.group(1)
            
            if curr_id and curr_id in prev_content:
                matches.append(f"{id_key}={curr_id}")
        
        if len(matches) >= 2:
            findings.append(f"Semantic Thread Hardened: Multiple identifiers propagated: {', '.join(matches)}")
        elif len(matches) == 1:
            findings.append(f"Semantic Thread Verified: Single identifier link '{matches[0]}'.")
        else:
            findings.append("Semantic Thread BREAK: No shared identifiers (spec_id, run_id, etc.) found between steps.")
            failure_modes.append("missing_semantic_thread")

        # Semantic Preservation Check (ADR 0008 Hardening)
        # Verify if the core domain nouns are preserved across steps
        prev_nouns = set(re.findall(r"\b[A-Z][a-z]{6,}\b", prev_content))
        curr_nouns = set(re.findall(r"\b[A-Z][a-z]{6,}\b", content))
        
        common_fm = {"Section", "Content", "Status", "Report", "Fixture", "Surface", "Finding", "Description"}
        prev_nouns = {n.lower() for n in prev_nouns if n not in common_fm}
        curr_nouns = {n.lower() for n in curr_nouns if n not in common_fm}
        
        if prev_nouns:
            preserved = prev_nouns.intersection(curr_nouns)
            preservation_rate = len(preserved) / len(prev_nouns)
            if preservation_rate < 0.3: # ADR 0008: 30% preservation of domain nouns
                findings.append(f"Semantic Drift failure: Only {len(preserved)}/{len(prev_nouns)} core domain terms preserved ({preservation_rate:.0%}).")
                failure_modes.append("semantic_drift")
            else:
                findings.append(f"Semantic Preservation verified: {len(preserved)} core domain terms preserved across steps.")

        # Final Workflow Intent Audit (ADR 0008)
        if workflow_id:
            # Check for the presence of the workflow's specific intent identifiers or goals
            wf_parts = workflow_id.split("-")
            intent_keywords = [p for p in wf_parts if len(p) > 3]
            
            # Check if these keywords appear in significant sections (Headers)
            headers = re.findall(r"^#+ (.*)", content, re.MULTILINE)
            header_text = " ".join(headers).lower()
            
            matched_intent = [k for k in intent_keywords if k.lower() in header_text or k.lower() in content.lower()[:500]]
            if len(matched_intent) < len(intent_keywords) * 0.5:
                findings.append(f"Workflow Intent warning: Artifact lacks strong alignment with workflow ID keywords ({matched_intent}).")
            else:
                findings.append(f"Workflow Intent verified: Artifact headers/intro align with '{workflow_id}'.")


    status = "pass" if not failure_modes else "fail"
    return ValidatorResult(
        status=status,
        validator_name="workflow_link",
        findings=findings,
        failure_modes=failure_modes,
        artifact_path=str(curr_artifact_rel)
    )
