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
            elif len(propagated_ids) < len(input_ids) * 0.8: # ADR 0008: Stricter (80%)
                findings.append(f"Traceability warning: Only {len(propagated_ids)}/{len(input_ids)} input IDs were propagated (Target: 80%+).")
            else:
                findings.append(f"Traceability verified: Propagated {len(propagated_ids)}/{len(input_ids)} IDs.")

        # 3.2 Boundedness: Did we hallucinate new IDs?
        hallucinated_ids = output_ids - input_ids
        if hallucinated_ids and input_ids: # Only check if input had IDs
            findings.append(f"Boundedness failure: Hallucinated IDs detected: {', '.join(list(hallucinated_ids)[:5])}")
            failure_modes.append("hallucination_detected")

        # 3.3 Semantic Derivation: Deep grounding check (ADR 0008)
        # Extract meaningful domain terms (Proper nouns or long technical terms)
        domain_terms = set(re.findall(r"\b[A-Z][a-z]{5,}\b|\b[a-z]{8,}\b", input_content))
        common_words = {"section", "content", "status", "report", "finding", "surface", "inventory", "fixture", "context", "description", "observed"}
        domain_terms = {w.lower() for w in domain_terms if w.lower() not in common_words}
        
        # Phase 3 Hardening: Extract long phrase fragments (Semantic Proof)
        # Look for 4-6 word sequences that appear to be descriptive
        descriptive_phrases = re.findall(r"([a-z]{4,}(?:\s+[a-z]{4,}){3,5})", input_content.lower())
        descriptive_phrases = [p for p in descriptive_phrases if len(p.split()) >= 4]
        
        grounding_score = 0
        if domain_terms:
            matched_terms = {w for w in domain_terms if w in output_content.lower()}
            derivation_ratio = len(matched_terms) / len(domain_terms) if domain_terms else 0
            if derivation_ratio >= 0.2:
                grounding_score += 1
                findings.append(f"Semantic Grounding (Keywords): Verified ({len(matched_terms)}/{len(domain_terms)}).")
            else:
                findings.append(f"Semantic Grounding (Keywords): Warning ({len(matched_terms)}/{len(domain_terms)}).")

        if descriptive_phrases:
            # Check if any significant phrase fragments are preserved or paraphrased
            phrase_matches = 0
            for phrase in descriptive_phrases[:20]: # Check a representative sample
                # Use smaller fragments for robustness to paraphrasing
                words = phrase.split()
                fragment = " ".join(words[:3]) # 3-word fragment
                if fragment in output_content.lower():
                    phrase_matches += 1
            
            if phrase_matches >= 2:
                grounding_score += 1
                findings.append(f"Semantic Grounding (Phrasal): Verified ({phrase_matches} phrase fragments detected).")
            else:
                findings.append(f"Semantic Grounding (Phrasal): Low evidence ({phrase_matches} matches).")

        if grounding_score == 0 and (domain_terms or descriptive_phrases):
            findings.append("Semantic Grounding failure: Output appears disconnected from input reality.")
            failure_modes.append("low_grounding")
        elif grounding_score == 2:
            findings.append("Full Semantic Proof: Strong evidence of domain-grounded derivation.")

        # 3.4 Judgment Fidelity: Proximity Check (ADR 0010)
        # Verify that judgment keywords appear near propagated IDs
        if input_ids and output_ids:
            judgment_keywords = ["priority", "status", "issue", "finding", "detected", "severity", "category"]
            propagated_ids = input_ids.intersection(output_ids)
            
            fidelity_hits = 0
            for skill_id in propagated_ids:
                # Find the position of the ID in output
                for match in re.finditer(re.escape(skill_id), output_content):
                    start = max(0, match.start() - 100)
                    end = min(len(output_content), match.end() + 100)
                    context = output_content[start:end].lower()
                    
                    if any(kw in context for kw in judgment_keywords):
                        fidelity_hits += 1
                        break # Found a judgment near this instance of the ID
            
            if propagated_ids:
                fidelity_ratio = fidelity_hits / len(propagated_ids)
                if fidelity_ratio >= 0.5:
                    findings.append(f"Judgment Fidelity verified: {fidelity_hits}/{len(propagated_ids)} IDs linked to judgment context.")
                else:
                    findings.append(f"Judgment Fidelity warning: Only {fidelity_hits}/{len(propagated_ids)} IDs linked to judgment context (Target: 50%+).")
                    # We don't fail yet, but we log it as a heuristic weakness
    # 4. Complexity Check (Skill-Specific Matrix)
    if thresholds:
        min_items = thresholds.get("min_findings") or thresholds.get("min_surface_candidates") or 0
        
        # Item identification patterns
        item_patterns = [
            r"(?:##|###|####)\s+Surface|Surface\s+\d+",
            r"^\s*-\s+\[ \]|(?:##|###)\s+Issue|Finding\s+\d+",
            r"(?:##|###|####)\s+Component|Module|View"
        ]
        
        total_items = 0
        for pattern in item_patterns:
            total_items += len(re.findall(pattern, output_content, re.MULTILINE | re.IGNORECASE))
        
        if total_items < min_items:
            findings.append(f"Judgment Fidelity Warning: Low complexity ({total_items} items, target {min_items}). Fixture may be too simple or skill may be under-performing.")
            failure_modes.append("low_complexity")
        else:
            findings.append(f"Complexity verified: {total_items} items detected.")

    status = "pass" if not failure_modes else "fail"
    return ValidatorResult(
        status=status,
        validator_name="behavioral_result",
        findings=findings,
        failure_modes=failure_modes
    )

