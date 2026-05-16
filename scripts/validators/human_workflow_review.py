import os
import re
from pathlib import Path
from scripts.validators.common import ValidatorResult

def validate_human_workflow_review(review_path, requested_scope="workflow"):
    """
    Validates a HUMAN-WORKFLOW-REVIEW.md file.
    Expects:
    - Decision: approved
    - Scope: matches requested_scope
    - Run ID: matches directory and is not a placeholder
    - All criteria checkboxes [x] checked.
    """
    if not review_path.exists():
        return ValidatorResult(
            validator_name="human_workflow_review",
            status="fail",
            findings=["Review file not found."],
            failure_modes=["missing_review"]
        )

    content = review_path.read_text(encoding="utf-8")
    findings = []
    failure_modes = []

    # 1. Decision Check
    decision_match = re.search(r"\*\*Decision:\*\*\s*(approved|rejected|pending)", content)
    if not decision_match:
        findings.append("Could not find Decision field.")
        failure_modes.append("invalid_format")
    else:
        decision = decision_match.group(1)
        if decision != "approved":
            findings.append(f"Decision is '{decision}', not 'approved'.")
            failure_modes.append("not_approved")
        else:
            findings.append("Decision verified: approved.")

    # 2. Scope Check
    scope_match = re.search(r"\*\*Scope:\*\*\s*(\S+)", content)
    if not scope_match:
        findings.append("Could not find Scope field.")
        failure_modes.append("invalid_format")
    else:
        scope = scope_match.group(1)
        if scope != requested_scope:
            findings.append(f"Scope mismatch: found '{scope}', expected '{requested_scope}'.")
            failure_modes.append("scope_mismatch")
        else:
            findings.append(f"Scope verified: {scope}.")

    # 3. Criteria Checkbox Check
    unchecked = re.findall(r"-\s*\[\s\]", content)
    if unchecked:
        findings.append(f"Found {len(unchecked)} unchecked review criteria.")
        failure_modes.append("incomplete_review")
    else:
        findings.append("All review criteria checkboxes are checked.")

    # 4. Traceability Check (ADR 0008)
    run_id_match = re.search(r"\*\*Run ID:\*\*\s*(\S+)", content)
    run_id = run_id_match.group(1) if run_id_match else None
    
    if not run_id or run_id.lower() in ("tbd", "[run-id]"):
        findings.append("Traceability failure: Run ID is missing or placeholder.")
        failure_modes.append("missing_traceability")
    elif run_id not in str(review_path):
        # Allow case-insensitive comparison for Windows paths
        if run_id.lower() not in str(review_path).lower():
            findings.append(f"Traceability mismatch: Run ID '{run_id}' does not match directory.")
            failure_modes.append("traceability_mismatch")
        else:
            findings.append(f"Traceability verified: Run ID {run_id} matches.")
    else:
        findings.append(f"Traceability verified: Run ID {run_id} matches.")

    status = "fail" if failure_modes else "pass"
    
    return ValidatorResult(
        validator_name="human_workflow_review",
        status=status,
        findings=findings,
        failure_modes=failure_modes
    )
