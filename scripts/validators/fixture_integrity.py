from pathlib import Path
from .common import ValidatorResult

def validate_fixture_integrity(fixture_path, skill_name=None):
    """
    Validates structural integrity and content depth of a test fixture.
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
    else:
        findings.append("Ground truth rubric found in expected/rubric.md")

    # 2. Content Depth (Non-Triviality)
    content_files = [f for f in path.glob("**/*") if f.is_file() 
                    and f.suffix in ('.md', '.json', '.js', '.ts', '.html', '.css')
                    and "expected" not in str(f) 
                    and not f.name.startswith(".")]
    
    if not content_files:
        findings.append(f"Fixture '{path.name}' contains no relevant input content files")
        failure_modes.append("trivial_fixture")
    else:
        total_size = sum(f.stat().st_size for f in content_files)
        if total_size < 100:
            findings.append(f"Fixture content is too thin ({total_size} bytes).")
            failure_modes.append("trivial_content")

    # 3. Input Artifact Verification (Skill-Specific)
    if skill_name:
        required_inputs = {
            "ui-orchestrator": ["reports/SPEC-LINT-REPORT.md"],
            "ui-spec-reconcile": ["reports/ORCHESTRATOR-RECOMMENDATION.md"],
            "ui-inspector": ["reports/SPEC-RECONCILE-SUMMARY.md"]
        }
        
        for req in required_inputs.get(skill_name, []):
            req_path = path / req
            if not req_path.exists():
                findings.append(f"Missing required input artifact for '{skill_name}': {req}")
                failure_modes.append("missing_input_artifact")

    # 4. Adversarial Intent Tagging
    if "messy" in path.name.lower() or "adversarial" in path.name.lower():
        findings.append("Adversarial intent detected: This is a 'messy' fixture.")

    status = "pass" if not failure_modes else "fail"
    return ValidatorResult(
        status=status,
        validator_name="fixture_integrity",
        findings=findings,
        failure_modes=failure_modes
    )
