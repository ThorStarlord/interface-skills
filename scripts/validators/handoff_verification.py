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

    # 2. Detect Mode (Real vs Simulated) - ADR 0008 Hardening
    # Real handoff means the downstream skill actually used the specific artifacts of the upstream
    actual_mode = "simulated"
    is_real = False
    
    # Check 1: Exact Citation of upstream_artifact basename
    if upstream_artifact:
        up_basename = Path(upstream_artifact).name
        if up_basename in content:
            is_real = True
            findings.append(f"Handoff Evidence: Exact citation of upstream artifact '{up_basename}' found.")
    
    # Check 2: Identifier Density (e.g. spec_id, run_id, or custom IDs like UI-123)
    if upstream_artifact:
        up_content = Path(upstream_artifact).read_text(encoding="utf-8")
        # Look for standard ID patterns
        up_ids = set(re.findall(r"\b[A-Z]{2,4}-\d{3,5}\b|\b[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}\b|\bspec_[a-z0-9]+\b|\brun_[a-z0-9]+\b", up_content))
        if up_ids:
            found_ids = [i for i in up_ids if i in content]
            if len(found_ids) >= 2: # Require at least 2 matching unique IDs for "real" proof
                is_real = True
                findings.append(f"Handoff Evidence: High identifier density ({len(found_ids)} matches).")
            elif len(found_ids) == 1:
                findings.append(f"Handoff Evidence: Single identifier match '{found_ids[0]}' (insufficient for 'real' proof).")

    # Check 3: Domain-specific keywords (fallback/supplementary)
    real_handoff_keywords = ["spec-lint-report.md", "redline-audit.md", "surface-inventory.md", "blueprint.md", "brief.md"]
    found_keywords = [k for k in real_handoff_keywords if k.lower() in content.lower()]
    if found_keywords:
        # Keywords alone don't prove consumption, but they support it
        findings.append(f"Handoff Evidence: Domain-specific artifact references found: {', '.join(found_keywords)}")
        if not is_real and len(found_keywords) >= 2:
            is_real = True # Two or more specific artifact names is strong evidence

    if is_real:
        actual_mode = "real"
        
        # Check 4: Deep Semantic Consumption (ADR 0008)
        # Verify that the downstream doesn't just mention the upstream artifact name,
        # but also includes content derived from it (more than just IDs).
        if upstream_artifact:
            up_content = Path(upstream_artifact).read_text(encoding="utf-8")
            # Heuristic: Check for unique sentences or phrases from upstream (simplified)
            # We look for matches of specific findings or surface descriptions
            potential_data_points = re.findall(r"##\s+(.*)|###\s+(.*)|-\s+(.*)", up_content)
            data_points = [p[0] or p[1] or p[2] for p in potential_data_points if len(p[0] or p[1] or p[2]) > 20]
            
            consumed_points = [p for p in data_points if p.lower()[:30] in content.lower()] # Check first 30 chars
            if consumed_points:
                findings.append(f"Deep Consumption Verified: {len(consumed_points)} semantic data points from upstream found in downstream.")
            elif data_points:
                findings.append("Deep Consumption Warning: Downstream mentions upstream artifact but lacks evidence of consuming specific semantic data points.")
                # We don't downgrade actual_mode to simulated yet, but we warn.
    else:
        actual_mode = "simulated"
        findings.append("Actual handoff mode: simulated (lacks sufficient evidence of direct consumption)")


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
        z_result = validate_zero_repair(Path(fixture_path), Path(downstream_artifact), requested_scope=requested_scope)
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

