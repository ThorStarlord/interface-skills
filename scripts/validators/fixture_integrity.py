from pathlib import Path
from .common import ValidatorResult

def validate_fixture_integrity(fixture_path):
    """
    Validates structural integrity of a test fixture.
    """
    path = Path(fixture_path)
    
    if not path.exists() or not path.is_dir():
        return ValidatorResult(
            status="fail",
            validator_name="fixture_integrity",
            findings=[f"Fixture directory not found: {path.name}"],
            failure_modes=["missing_fixture"]
        )

    findings = []
    failure_modes = []
    
    # 1. Rubric Presence
    rubric_path = path / "expected" / "rubric.md"
    if not rubric_path.exists():
        findings.append(f"Fixture '{path.name}' is missing expected/rubric.md")
        failure_modes.append("missing_rubric")
        
    # 2. Basic Content Check
    # (Checking for empty directory or missing critical inputs could go here)
    
    if not findings:
        return ValidatorResult(
            status="pass",
            validator_name="fixture_integrity",
            findings=[f"Fixture '{path.name}' integrity verified"]
        )
    else:
        return ValidatorResult(
            status="fail",
            validator_name="fixture_integrity",
            findings=findings,
            failure_modes=failure_modes
        )
