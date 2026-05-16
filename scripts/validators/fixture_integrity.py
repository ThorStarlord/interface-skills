from pathlib import Path
from .common import ValidatorResult

def validate_fixture_integrity(fixture_path):
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
    # Exclude rubric, results, and hidden files
    content_files = [f for f in path.glob("**/*") if f.is_file() 
                    and f.suffix in ('.md', '.json', '.js', '.ts', '.html', '.css')
                    and "expected" not in str(f) 
                    and not f.name.startswith(".")]
    
    if not content_files:
        findings.append(f"Fixture '{path.name}' contains no relevant input content files (.md, .json, etc.)")
        failure_modes.append("trivial_fixture")
    else:
        total_size = sum(f.stat().st_size for f in content_files)
        if total_size < 100: # Heuristic for non-trivial content
            findings.append(f"Fixture content is too thin ({total_size} bytes). Possible placeholder.")
            failure_modes.append("trivial_content")
        else:
            findings.append(f"Content depth verified: {len(content_files)} files, {total_size} bytes total.")

    # 3. Adversarial Intent Tagging
    if "messy" in path.name.lower() or "adversarial" in path.name.lower():
        findings.append("Adversarial intent detected: This is a 'messy' fixture designed for failure-mode testing.")
        # This doesn't fail integrity, it just tags it.

    status = "pass" if not failure_modes else "fail"
    return ValidatorResult(
        status=status,
        validator_name="fixture_integrity",
        findings=findings,
        failure_modes=failure_modes
    )
