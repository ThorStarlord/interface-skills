import re
import json
from pathlib import Path
from .common import ValidatorResult
from .zero_repair import validate_zero_repair

def validate_handoff(run_dir, skill_name, next_skill_name, requested_scope="stable", upstream_artifact=None, downstream_artifact=None, fixture_path=None, expected_mode=None):
    """
    Validates if the downstream skill correctly consumed the output of the previous skill.
    Enforces 'real' handoff if requested_scope is 'workflow' (ADR 0007) or if expected_mode is 'real'.
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
    
    # 1. Consumption Contract: Verify upstream artifact mention & content usage
    if upstream_artifact:
        up_path = Path(upstream_artifact)
        up_name = up_path.name
        
        # 1.1 Citation Check
        if up_name.lower() not in content.lower():
            findings.append(f"Consumption Contract Violation: Downstream skill failed to cite upstream artifact '{up_name}'")
            failure_modes.append("consumption_contract_violation")
        else:
            findings.append(f"Consumption Contract Verified: Upstream artifact '{up_name}' cited.")

        # 1.2 Semantic Continuity (ADR 0008)
        # Check if any unique keywords/IDs from upstream are present in downstream
        up_content = up_path.read_text(encoding="utf-8")
        # Extract unique-ish words (>= 6 chars) or IDs
        up_identifiers = set(re.findall(r"\b[A-Z]{3,4}-\d{3}\b|\b[A-Z][a-z]{5,}\b", up_content))
        # Filter out common markdown words
        common = {"Source", "Content", "Section", "Status", "Report", "Fixture"}
        up_identifiers = {i for i in up_identifiers if i not in common}
        
        if up_identifiers:
            matched = [i for i in up_identifiers if i.lower() in content.lower()]
            if not matched:
                findings.append("Semantic Continuity Warning: No unique identifiers from upstream were found in downstream output.")
            else:
                findings.append(f"Semantic Continuity Verified: {len(matched)} upstream identifiers found in downstream.")

    # 2. Detect Mode (Real vs Simulated)
    # Real handoff means the downstream skill actually used the specific artifacts of the upstream
    real_handoff_keywords = ["spec-lint-report.md", "redline", "inventory", "blueprint", "brief", "orchestrator", "reconcile"]
    found_keywords = [k for k in real_handoff_keywords if k.lower() in content.lower()]
    
    actual_mode = "simulated"
    if found_keywords:
        actual_mode = "real"
        findings.append(f"Actual handoff mode: real (detected via keywords: {', '.join(found_keywords)})")
    else:
        actual_mode = "simulated"
        findings.append("Actual handoff mode: simulated (no deep artifact keywords found)")

    # 3. Enforcement (ADR 0007 / ADR 0008)
    enforced_mode = expected_mode
    if requested_scope == "workflow" and not enforced_mode:
        enforced_mode = "real" # Default for workflow scope
        
    if enforced_mode == "real" and actual_mode != "real":
        findings.append(f"Handoff Enforcement Failure: Expected 'real' handoff but detected '{actual_mode}'")
        failure_modes.append("real_handoff_required")
    elif enforced_mode:
        findings.append(f"Handoff mode requirement met: {actual_mode}")

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
        checked_scope=requested_scope,
        detected_mode=actual_mode
    )

