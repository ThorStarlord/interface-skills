import re
from pathlib import Path
from .common import ValidatorResult
from .zero_repair import validate_zero_repair

def validate_behavioral_result(output_content, skill_name, thresholds=None, input_content=None, fixture_path=None, artifact_path=None):
    """
    Validates the shape, quality, and traceability of a behavioral result.
    """
    findings = []
    failure_modes = []
    thresholds = thresholds or {}
    
    # 0. Zero-Manual-Repair Integration (ADR 0005/0008)
    if fixture_path and artifact_path:
        z_result = validate_zero_repair(Path(fixture_path), Path(artifact_path))
        if z_result.status != "pass":
            findings.extend(z_result.findings)
            failure_modes.append("zero_repair_violation")
        else:
            findings.append("Mechanical proof verified: Zero-Manual-Repair contract intact.")
    
    # 1. Consumption Contract: Citation Traceability
    # The output should ideally cite its source or input artifacts to ensure a closed-loop audit.
    if fixture_path:
        source_context = Path(fixture_path).name
        if source_context.lower() not in output_content.lower() and "source" not in output_content.lower():
            # Soft failure for now, but logged
            findings.append(f"Consumption Warning: Output does not explicitly cite source context '{source_context}'")
    
    # 2. Placeholder Check (Strict)
    placeholders = [
        r"\bTBD\b", r"\bTODO\b", r"\[insert", r"INSERT HERE", r"\[PLACEHOLDER\]", 
        r"\[FIXME\]", r"\[\.\.\.\]", r"\[FILL ME\]", r"<.+>"
    ]
    found_placeholders = [p for p in placeholders if re.search(p, output_content, re.IGNORECASE)]
    
    if found_placeholders:
        findings.append(f"Output contains trivial placeholders: {', '.join(found_placeholders)}")
        failure_modes.append("trivial_placeholders")

    # 3. Traceability & Boundedness (ID Propagation)
    # Detect common ID patterns: SURF-001, FIND-001, SPEC-001, RECO-001, etc.
    id_pattern = r"\b[A-Z]{3,4}-\d{3}\b"
    
    if input_content:
        input_ids = set(re.findall(id_pattern, input_content))
        output_ids = set(re.findall(id_pattern, output_content))
        
        # 3.1 Traceability: Did we keep the IDs from the input?
        if input_ids:
            propagated_ids = input_ids.intersection(output_ids)
            if not propagated_ids:
                findings.append(f"Traceability failure: None of the {len(input_ids)} input IDs were found in output.")
                failure_modes.append("traceability_loss")
            elif len(propagated_ids) < len(input_ids) * 0.5: # Heuristic: at least 50%
                findings.append(f"Traceability warning: Only {len(propagated_ids)}/{len(input_ids)} input IDs were propagated.")
            else:
                findings.append(f"Traceability verified: Propagated {len(propagated_ids)}/{len(input_ids)} IDs.")

        # 3.2 Boundedness: Did we hallucinate new IDs?
        hallucinated_ids = output_ids - input_ids
        if hallucinated_ids and input_ids: # Only check if input had IDs
            findings.append(f"Boundedness failure: Hallucinated IDs detected: {', '.join(list(hallucinated_ids)[:5])}")
            failure_modes.append("hallucination_detected")

        # 3.3 Semantic Derivation: Check if unique keywords from input appear in output
        # (Excluding common structural words)
        input_keywords = set(re.findall(r"\b[a-zA-Z]{6,}\b", input_content))
        common_words = {"section", "content", "status", "report", "finding", "surface", "inventory", "fixture", "context"}
        input_keywords = {w.lower() for w in input_keywords if w.lower() not in common_words}
        
        if input_keywords:
            matched_keywords = {w for w in input_keywords if w in output_content.lower()}
            derivation_ratio = len(matched_keywords) / len(input_keywords) if input_keywords else 0
            if derivation_ratio < 0.1 and len(input_keywords) > 10: # Heuristic: at least 10% for large inputs
                findings.append(f"Semantic Derivation Warning: Low keyword overlap ({len(matched_keywords)}/{len(input_keywords)}). Output may not be sufficiently grounded in input.")
            else:
                findings.append(f"Semantic Derivation Verified: Output is grounded in input content ({len(matched_keywords)} shared keywords).")

    # 4. Complexity Check (Skill-Specific Matrix)
    # This logic should eventually move fully to registry, but kept here for depth
    if thresholds:
        min_items = thresholds.get("min_findings") or thresholds.get("min_surface_candidates") or 0
        
        # Determine item pattern based on skill
        item_pattern = r"(?:^|\n)\s*(?:##|###|####|-)\s+" # Generic markdown headers or list items
        if skill_name == "ui-surface-inventory":
            item_pattern = r"(?:##|###|####)\s+Surface|Surface\s+\d+"
        elif skill_name == "ui-to-issues":
            item_pattern = r"^\s*-\s+\[ \]|(?:##|###)\s+Issue|Finding\s+\d+"
            
        found_items = len(re.findall(item_pattern, output_content, re.MULTILINE | re.IGNORECASE))
        
        if found_items < min_items:
            findings.append(f"Low behavioral complexity: {found_items} items found, expected at least {min_items}")
            failure_modes.append("low_complexity")
        else:
            findings.append(f"Complexity verified: {found_items} items detected.")

    status = "pass" if not failure_modes else "fail"
    return ValidatorResult(
        status=status,
        validator_name="behavioral_result",
        findings=findings,
        failure_modes=failure_modes
    )

