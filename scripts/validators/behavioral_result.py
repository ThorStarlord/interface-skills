import re
from .common import ValidatorResult

def validate_behavioral_result(output_content, skill_name, thresholds=None):
    """
    Validates the shape and quality of a behavioral result.
    """
    findings = []
    failure_modes = []
    
    # 1. Placeholder Check
    placeholders = [r"\bTBD\b", r"\bTODO\b", r"\[insert", r"INSERT HERE", r"\[PLACEHOLDER\]"]
    found_placeholders = [p for p in placeholders if re.search(p, output_content, re.IGNORECASE)]
    
    if found_placeholders:
        findings.append(f"Output contains trivial placeholders: {', '.join(found_placeholders)}")
        failure_modes.append("trivial_placeholders")

    # 2. Complexity Check
    if thresholds:
        if skill_name == "ui-surface-inventory":
            min_surfaces = thresholds.get("min_surface_candidates", 0)
            surface_count = len(re.findall(r"(?:##|###|####)\s+Surface|Surface\s+\d+", output_content, re.IGNORECASE))
            if surface_count < min_surfaces:
                findings.append(f"Low complexity: {surface_count} surfaces found, need {min_surfaces}")
                failure_modes.append("low_complexity")
                
        if skill_name == "ui-to-issues":
            min_findings = thresholds.get("min_findings", 0)
            finding_count = len(re.findall(r"^\s*-\s+\[ \]|(?:##|###)\s+Issue|Finding\s+\d+", output_content, re.MULTILINE | re.IGNORECASE))
            if finding_count < min_findings:
                findings.append(f"Low complexity: {finding_count} findings found, need {min_findings}")
                failure_modes.append("low_complexity")

    if not findings:
        return ValidatorResult(
            status="pass",
            validator_name="behavioral_result",
            findings=["Output meets behavioral quality standards"]
        )
    else:
        return ValidatorResult(
            status="fail",
            validator_name="behavioral_result",
            findings=findings,
            failure_modes=failure_modes
        )
