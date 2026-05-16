from pathlib import Path
import re
import yaml
from .common import ValidatorResult

def validate_workflow_link(run_dir, current_step, previous_step=None):
    """
    Validates the continuity between two workflow steps.
    
    Args:
        run_dir: The directory of the current promotion run.
        current_step: Dict containing 'skill', 'artifact', etc. for the current step.
        previous_step: Optional dict for the previous step.
    """
    findings = []
    failure_modes = []
    
    if not previous_step:
        return ValidatorResult(
            status="pass",
            validator_name="workflow_link",
            findings=["First step in workflow - no predecessor to link."]
        )

    # 1. Physical Continuity: Input artifact matches previous output
    prev_output = previous_step.get("artifact")
    curr_input = current_step.get("input_artifact")
    
    if curr_input and prev_output:
        if curr_input != prev_output:
            findings.append(f"Physical Continuity Break: Current input '{curr_input}' does not match previous output '{prev_output}'")
            failure_modes.append("mismatched_paths")
    
    # 2. Semantic Continuity: Check for references in the output artifact
    curr_artifact_rel = current_step.get("artifact")
    if not curr_artifact_rel:
        return ValidatorResult(
            status="fail",
            validator_name="workflow_link",
            findings=["Current step artifact path missing in manifest."],
            failure_modes=["missing_manifest_entry"]
        )
        
    curr_artifact_path = Path(run_dir).parent.parent / curr_artifact_rel # Relative to repo root
    if not curr_artifact_path.exists():
        # Fallback for relative to run_dir if needed
        curr_artifact_path = Path(run_dir) / curr_artifact_rel
        if not curr_artifact_path.exists():
            return ValidatorResult(
                status="fail",
                validator_name="workflow_link",
                findings=[f"Output artifact not found: {curr_artifact_rel}"],
                failure_modes=["missing_artifact"]
            )

    content = curr_artifact_path.read_text(encoding="utf-8")
    
    # Extract frontmatter if present
    frontmatter = {}
    fm_match = re.search(r"^---(.*?)---", content, re.DOTALL)
    if fm_match:
        try:
            frontmatter = yaml.safe_load(fm_match.group(1))
        except yaml.YAMLError:
            findings.append("Malformed frontmatter in output artifact.")
            failure_modes.append("malformed_metadata")

    # Semantic Linkage Check
    based_on = frontmatter.get("based_on", "")
    prev_skill = previous_step.get("skill")
    
    # Pattern 1: frontmatter 'based_on' field
    if based_on:
        findings.append(f"Semantic Link found in frontmatter: based_on='{based_on}'")
    else:
        # Pattern 2: Search for skill name or previous artifact ID in content
        prev_artifact_rel = previous_step.get("artifact")
        prev_id = Path(prev_artifact_rel).stem if prev_artifact_rel else ""
        
        if prev_id and prev_id in content:
            findings.append(f"Semantic Link found in content: referenced previous ID '{prev_id}'")
        elif prev_skill and prev_skill in content:
            findings.append(f"Semantic Link found in content: referenced previous skill '{prev_skill}'")
        else:
            findings.append(f"Semantic Continuity Break: Output does not reference previous step '{prev_skill}' or artifact '{prev_id}'")
            failure_modes.append("missing_semantic_link")

    status = "pass" if not failure_modes else "fail"
    return ValidatorResult(
        status=status,
        validator_name="workflow_link",
        findings=findings,
        failure_modes=failure_modes,
        artifact_path=str(curr_artifact_rel)
    )
