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
    decision_match = re.search(r"(?:\*\*Decision:\*\*|Decision:)\s*(approved|rejected|pending|approved for full-chain stability)", content, re.IGNORECASE)
    if not decision_match and "approved for full-chain stability" in content.lower():
        decision = "approved"
    elif decision_match:
        decision = decision_match.group(1).strip().lower()
        if "approved" in decision:
            decision = "approved"
    else:
        decision = "unknown"

    if decision != "approved":
        findings.append(f"Decision is '{decision}', not 'approved'.")
        failure_modes.append("not_approved")
    else:
        findings.append("Decision verified: approved.")

    # 2. Scope Check
    scope = None
    if "workflow_stability_authorized" in content.lower() or "workflow_promotion_authorized" in content.lower():
        scope = "workflow"
    else:
        scope_match = re.search(r"(?:\*\*Scope:\*\*|Scope:)\s*(\S+)", content, re.IGNORECASE)
        if scope_match:
            scope = scope_match.group(1).strip().lower()

    if not scope:
        findings.append("Could not find Scope field.")
        failure_modes.append("invalid_format")
    else:
        # Normalize scopes for workflow authority
        normalized_found = "workflow_promotion_authorized" if scope in ("workflow", "workflow_stability_authorized") else scope
        normalized_requested = "workflow_promotion_authorized" if requested_scope == "workflow" else requested_scope
        
        if normalized_found != normalized_requested:
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
    run_id_match = re.search(r"(?:\*\*Run\s+ID:\*\*|Run\s+ID:)\s*(\S+)", content, re.IGNORECASE)
    run_id = run_id_match.group(1) if run_id_match else None
    
    if not run_id:
        # Fallback to searching for the run ID pattern in the content (e.g. 2026-05-15-22-17-01-workflow-spec-recovery)
        pattern_match = re.search(r"(\d{4}-\d{2}-\d{2}-\d{2}-\d{2}-\d{2}-\S+?)(?:/|\s|\`|\))", content)
        if pattern_match:
            run_id = pattern_match.group(1).strip()
            
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
