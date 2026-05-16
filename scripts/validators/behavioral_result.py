import re
from .common import ValidatorResult

def validate_behavioral_result(output_content, skill_name, thresholds=None, input_content=None):
    """
    Validates the shape, quality, and traceability of a behavioral result.
    """
    findings = []
    failure_modes = []
    thresholds = thresholds or {}
    
    # 1. Placeholder Check (Strict)
    placeholders = [r"\bTBD\b", r"\bTODO\b", r"\[insert", r"INSERT HERE", r"\[PLACEHOLDER\]", r"\[FIXME\]"]
    found_placeholders = [p for p in placeholders if re.search(p, output_content, re.IGNORECASE)]
    
    if found_placeholders:
        findings.append(f"Output contains trivial placeholders: {', '.join(found_placeholders)}")
        failure_modes.append("trivial_placeholders")

    # 2. Traceability & Boundedness (ID Propagation)
    # Detect common ID patterns: SURF-001, FIND-001, SPEC-001, etc.
    id_pattern = r"\b[A-Z]{3,4}-\d{3}\b"
    
    if input_content:
        input_ids = set(re.findall(id_pattern, input_content))
        output_ids = set(re.findall(id_pattern, output_content))
        
        # Traceability: Did we keep the IDs from the input?
        if input_ids:
            propagated_ids = input_ids.intersection(output_ids)
            if not propagated_ids and len(input_ids) > 0:
                findings.append(f"Traceability failure: None of the {len(input_ids)} input IDs were found in output.")
                failure_modes.append("traceability_loss")
            else:
                findings.append(f"Traceability verified: Propagated {len(propagated_ids)}/{len(input_ids)} IDs.")

        # Boundedness: Did we hallucinate new IDs?
        hallucinated_ids = output_ids - input_ids
        if hallucinated_ids and input_ids: # Only check if input had IDs
            findings.append(f"Boundedness failure: Hallucinated IDs detected: {', '.join(list(hallucinated_ids)[:5])}")
            failure_modes.append("hallucination_detected")

    # 3. Complexity Check (Skill-Specific)
    if thresholds:
        if skill_name == "ui-surface-inventory":
            min_surfaces = thresholds.get("min_surface_candidates", 0)
            surface_count = len(re.findall(r"(?:##|###|####)\s+Surface|Surface\s+\d+", output_content, re.IGNORECASE))
            if surface_count < min_surfaces:
                findings.append(f"Low complexity: {surface_count} surfaces found, need {min_surfaces}")
                failure_modes.append("low_complexity")
                
        elif skill_name == "ui-to-issues":
            min_findings = thresholds.get("min_findings", 0)
            finding_count = len(re.findall(r"^\s*-\s+\[ \]|(?:##|###)\s+Issue|Finding\s+\d+", output_content, re.MULTILINE | re.IGNORECASE))
            if finding_count < min_findings:
                findings.append(f"Low complexity: {finding_count} findings found, need {min_findings}")
                failure_modes.append("low_complexity")
        
        # New: Generic finding count for other report-based skills
        elif "min_findings" in thresholds:
            min_findings = thresholds.get("min_findings")
            finding_count = len(re.findall(r"(?:^|\n)\s*(?:##|###|####|-)\s+", output_content))
            if finding_count < min_findings:
                findings.append(f"Low behavioral complexity: {finding_count} items found, need {min_findings}")
                failure_modes.append("low_complexity")

    if not findings:
        return ValidatorResult(
            status="pass",
            validator_name="behavioral_result",
            findings=["Output meets behavioral quality and traceability standards"]
        )
    else:
        # If we have findings but no failure modes (e.g. just informational tags), it passes
        status = "fail" if failure_modes else "pass"
        return ValidatorResult(
            status=status,
            validator_name="behavioral_result",
            findings=findings,
            failure_modes=failure_modes
        )
