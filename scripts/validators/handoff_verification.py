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
    
    # Check 2: Identifier Density & Propagation Proof (ADR 0008)
    if upstream_artifact:
        up_content = Path(upstream_artifact).read_text(encoding="utf-8")
        # Look for standard ID patterns
        up_ids = set(re.findall(r"\b[A-Z]{2,4}-\d{3,5}\b|\b[a-z0-9]{8}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{4}-[a-z0-9]{12}\b|\bspec_[a-z0-9]+\b|\brun_[a-z0-9]+\b", up_content))
        if up_ids:
            found_ids = [i for i in up_ids if i in content]
            if len(found_ids) >= 3: # Higher threshold for 'real' proof in Phase 3
                is_real = True
                findings.append(f"Handoff Evidence: High identifier density ({len(found_ids)} matches).")
            elif len(found_ids) >= 1:
                findings.append(f"Handoff Evidence: Identifier linkage detected ({len(found_ids)} matches).")

    # Check 3: Semantic Data Point Extraction & Matching (Semantic Proof)
    if upstream_artifact:
        up_content = Path(upstream_artifact).read_text(encoding="utf-8")
        # Extract meaningful strings (Findings, Descriptions, etc.)
        # Look for content in lists or headers
        potential_data = re.findall(r"(?:##|###|####|-)\s+(.{20,})", up_content)
        data_points = [d.strip() for d in potential_data if len(d.strip()) > 30]
        
        if data_points:
            # Check if significant fragments of these points exist in downstream
            matches = 0
            for point in data_points[:10]: # Check top 10 points
                fragment = point[:40].lower() # Check first 40 chars
                if fragment in content.lower():
                    matches += 1
            
            if matches >= 2:
                is_real = True
                findings.append(f"Semantic Handoff Proof: {matches} unique data points from upstream were consumed by downstream.")
            elif matches == 1:
                findings.append(f"Semantic Handoff Link: 1 unique data point from upstream found in downstream.")

    if is_real:
        actual_mode = "real"
    else:
        actual_mode = "simulated"
        findings.append("Actual handoff mode: simulated (lacks sufficient evidence of direct semantic consumption)")


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

