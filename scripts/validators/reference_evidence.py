from pathlib import Path
from .common import ValidatorResult

def validate_reference_evidence(skill_name, reference_dir):
    """
    Validates the curated Promotion Reference Evidence.
    """
    path = Path(reference_dir)
    
    if not path.exists():
        return ValidatorResult(
            status="fail",
            validator_name="reference_evidence",
            findings=[f"Reference directory not found: {path}"],
            failure_modes=["missing_reference_dir"]
        )

    findings = []
    failure_modes = []
    
    # 1. Rubric Presence (Minimum for any reference)
    rubric_path = path / "expected" / "rubric.md"
    if not rubric_path.exists():
        findings.append(f"Reference for '{skill_name}' is missing expected/rubric.md")
        failure_modes.append("missing_rubric")
        
    # 2. Evidence completeness
    # (In a real scenario, we'd check for specific files mandated by the skill contract)
    
    if not findings:
        return ValidatorResult(
            status="pass",
            validator_name="reference_evidence",
            findings=[f"Reference evidence for '{skill_name}' verified"]
        )
    else:
        return ValidatorResult(
            status="fail",
            validator_name="reference_evidence",
            findings=findings,
            failure_modes=failure_modes
        )
