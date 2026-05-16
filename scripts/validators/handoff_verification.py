from pathlib import Path
from .common import ValidatorResult

def validate_handoff(run_dir, skill_name, next_skill_name):
    """
    Validates if the downstream skill correctly consumed the output of the previous skill.
    """
    path = Path(run_dir)
    next_skill_file = path / f"downstream_{next_skill_name}.md"
    
    if not next_skill_file.exists():
        return ValidatorResult(
            status="fail",
            validator_name="handoff_verification",
            findings=[f"Downstream output file missing: {next_skill_file.name}"],
            failure_modes=["missing_output"]
        )

    content = next_skill_file.read_text(encoding="utf-8")
    
    # Existing keyword check from harness
    consumed_marker = "Input Evidence"
    if consumed_marker.lower() in content.lower():
        # Heuristic check for specific filenames or "redline" keyword
        # (This matches the logic in classify_downstream_result)
        keywords = ["spec-lint-report.md", "redline", "inventory"]
        found_keywords = [k for k in keywords if k.lower() in content.lower()]
        
        if found_keywords:
            return ValidatorResult(
                status="pass",
                validator_name="handoff_verification",
                findings=[f"Downstream consumption verified via keywords: {', '.join(found_keywords)}"]
            )
        else:
            # Fallback pass if at least the marker is found? 
            # Actually, the original logic was strict about specific files if it mentions "Input Evidence"
            pass

    return ValidatorResult(
        status="fail",
        validator_name="handoff_verification",
        findings=[f"Downstream skill '{next_skill_name}' failed to acknowledge input evidence from '{skill_name}'"],
        failure_modes=["missing_consumption_marker"]
    )
