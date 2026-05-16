from pathlib import Path
from .common import ValidatorResult

def validate_handoff(run_dir, skill_name, next_skill_name, requested_scope="stable"):
    """
    Validates if the downstream skill correctly consumed the output of the previous skill.
    Enforces 'real' handoff if requested_scope is 'workflow' (ADR 0007).
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
    findings = []
    failure_modes = []
    
    # 1. Check for consumption marker
    consumed_marker = "Input Evidence"
    if consumed_marker.lower() not in content.lower():
        findings.append(f"Downstream skill '{next_skill_name}' failed to acknowledge input evidence from '{skill_name}'")
        failure_modes.append("missing_consumption_marker")
    
    # 2. Detect Mode (Real vs Simulated)
    # Heuristic: Real handoff usually involves specific artifacts or reports mentioned.
    # Simulated handoff might just have the marker but no depth.
    keywords = ["spec-lint-report.md", "redline", "inventory", "blueprint", "brief"]
    found_keywords = [k for k in keywords if k.lower() in content.lower()]
    
    handoff_mode = "simulated"
    if found_keywords:
        handoff_mode = "real"
        findings.append(f"Real handoff detected via keywords: {', '.join(found_keywords)}")
    else:
        findings.append("Simulated handoff detected (no deep artifact keywords found)")

    # 3. Enforcement (ADR 0007)
    if requested_scope == "workflow" and handoff_mode != "real":
        findings.append("Workflow promotion REQUIRES real handoff (ADR 0007)")
        failure_modes.append("real_handoff_required")

    status = "pass" if not failure_modes else "fail"
    return ValidatorResult(
        status=status,
        validator_name="handoff_verification",
        findings=findings,
        failure_modes=failure_modes,
        checked_scope=requested_scope
    )
