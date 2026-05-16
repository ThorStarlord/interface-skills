from pathlib import Path
from .common import ValidatorResult
from .zero_repair import validate_zero_repair

def validate_handoff(run_dir, skill_name, next_skill_name, requested_scope="stable", upstream_artifact=None, downstream_artifact=None, fixture_path=None):
    """
    Validates if the downstream skill correctly consumed the output of the previous skill.
    Enforces 'real' handoff if requested_scope is 'workflow' (ADR 0007).
    """
    path = Path(run_dir)
    
    # 0. Presence Check
    if not downstream_artifact or not Path(downstream_artifact).exists():
        return ValidatorResult(
            status="fail",
            validator_name="handoff_verification",
            findings=[f"Downstream output artifact missing for '{next_skill_name}'"],
            failure_modes=["missing_output"]
        )

    content = Path(downstream_artifact).read_text(encoding="utf-8")
    findings = []
    failure_modes = []
    
    # 1. Consumption Contract: Verify upstream artifact mention
    if upstream_artifact:
        up_name = Path(upstream_artifact).name
        if up_name.lower() not in content.lower():
            findings.append(f"Consumption Contract Violation: Downstream skill failed to cite upstream artifact '{up_name}'")
            failure_modes.append("consumption_contract_violation")
        else:
            findings.append(f"Consumption Contract Verified: Upstream artifact '{up_name}' cited in downstream output.")

    # 2. Detect Mode (Real vs Simulated)
    keywords = ["spec-lint-report.md", "redline", "inventory", "blueprint", "brief", "orchestrator", "reconcile"]
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

    # 4. Zero-Repair Proof (Mechanical stability between steps)
    if fixture_path and downstream_artifact:
        z_result = validate_zero_repair(Path(fixture_path), Path(downstream_artifact))
        if z_result.status != "pass":
            findings.extend(z_result.findings)
            failure_modes.append("zero_repair_violation")
        else:
            findings.append("Mechanical proof verified: Step handoff is zero-manual-repair stable.")

    status = "pass" if not failure_modes else "fail"
    return ValidatorResult(
        status=status,
        validator_name="handoff_verification",
        findings=findings,
        failure_modes=failure_modes,
        checked_scope=requested_scope
    )
