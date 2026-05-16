import re
from pathlib import Path
from .behavioral_result import validate_behavioral_result
from .handoff_verification import validate_handoff

def evaluate_output_against_rubric(output_content, rubric_items):
    """
    Evaluates output against a set of rubric items using keyword heuristics.
    """
    def extract_subject(text, prefix_len):
        subject = text[prefix_len:].strip().rstrip('.')
        for sep in [" where ", " if ", " consistent with ", " as "]:
            if sep in subject.lower():
                subject = subject.lower().split(sep)[0].strip()
                break
        return subject

    def strip_articles(text):
        for article in ["the ", "a ", "an "]:
            if text.lower().startswith(article):
                return text[len(article):]
        return text

    results = []
    for item in rubric_items:
        found = False
        text_lower = item["text"].lower()
        
        if text_lower in output_content.lower():
            found = True
        elif text_lower.startswith("identifies "):
            subject = extract_subject(item["text"], 11)
            subj_stripped = strip_articles(subject)
            if subj_stripped.lower() in output_content.lower() or subject.lower() in output_content.lower():
                found = True
        elif text_lower.startswith("prioritizes "):
            subject = extract_subject(item["text"], 12)
            if strip_articles(subject).lower() in output_content.lower():
                found = True
        elif text_lower.startswith("accounts for "):
            subject = extract_subject(item["text"], 13)
            if strip_articles(subject).lower() in output_content.lower():
                found = True
        elif text_lower.startswith("does not "):
            subject = extract_subject(item["text"], 9)
            if subject.lower() not in output_content.lower():
                found = True
        
        results.append({
            "item": item["text"],
            "section": item["section"],
            "passed": found,
            "automation": "keyword_match" if found else "pending_manual"
        })
    return results

def classify_run_result(skill_name, fixture_name, skill_config, validators_status, rubric_results, output_content, input_content=None, fixture_path=None, artifact_path=None):
    """
    Unified classification kernel for promotion runs.
    """
    messy_fixture_rel = skill_config.get("messy_fixture", "")
    is_messy = (fixture_name == Path(messy_fixture_rel).name)
    
    if not validators_status.get("skill_structural_valid", True):
        return "fail", "Skill structural validation failed unexpectedly", "invalid_structure"
        
    behavioral_criteria = skill_config.get("behavioral_criteria", {})
    complexity_thresholds = behavioral_criteria.get("minimum_behavioral_complexity", {})
    
    bev_result = validate_behavioral_result(
        output_content, skill_name, complexity_thresholds, 
        input_content=input_content, fixture_path=fixture_path, artifact_path=artifact_path
    )
    
    rubric_passed = "N/A"
    if rubric_results:
        automated_fail = any(r["passed"] is False and r["automation"] != "pending_manual" for r in rubric_results)
        all_passed = all(r["passed"] for r in rubric_results)
        rubric_passed = not automated_fail if automated_fail else ("pending" if not all_passed else True)

    if is_messy:
        if rubric_passed is False or bev_result.status == "fail":
            return "expected_fail", f"Messy fixture defects correctly detected: {bev_result.findings[0] if bev_result.status == 'fail' else 'Rubric failure'}", "valid"
        else:
            return "fail", "Messy fixture defects NOT correctly detected (False Positive Pass)", "adversarial_failure"

    if bev_result.status == "fail":
        status = "valid"
        if "trivial_placeholders" in bev_result.failure_modes: status = "trivial"
        elif "low_complexity" in bev_result.failure_modes: status = "low_complexity"
        elif "hallucination_detected" in bev_result.failure_modes: status = "hallucination"
        return "fail", bev_result.findings[0], status
            
    if not validators_status.get("package_structural_valid", True):
        return "fail", "Clean fixture package validation failed", "invalid_package"

    if rubric_passed is False:
        return "fail", "Clean fixture failed automated rubric check", "rubric_failure"
        
    if rubric_passed in ("pending", "N/A") or any(r.get("automation") == "pending_manual" for r in rubric_results):
        return "needs_human_review", "Evidence requires human judgment", "needs_review"
        
    return "pass", "Clean fixture passed all automated checks", "valid"
