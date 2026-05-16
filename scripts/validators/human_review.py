import re
from pathlib import Path
from .common import ValidatorResult

def validate_human_review(review_path, requested_scope):
    """
    Validates a human review markdown file.
    Checks for 'Status: approved' and 'Scope' matching the requested scope.
    """
    path = Path(review_path)
    if not path.exists():
        return ValidatorResult(
            status="fail",
            validator_name="human_review",
            findings=["HUMAN-REVIEW.md not found"],
            failure_modes=["missing_evidence"]
        )
    
    content = path.read_text(encoding="utf-8")
    
    # Extract status (deprecated but kept for compatibility)
    status_match = re.search(r"\*\*Status:\*\*\s*(.*)", content, re.IGNORECASE)
    status = status_match.group(1).strip().lower() if status_match else "unknown"
    
    # Extract decision (new primary authority)
    decision_match = re.search(r"\*\*Decision:\*\*\s*(.*)", content, re.IGNORECASE)
    decision = decision_match.group(1).strip().lower() if decision_match else "unknown"
    
    # Extract reviewer
    reviewer_match = re.search(r"\*\*Reviewer:\*\*\s*(.*)", content, re.IGNORECASE)
    reviewer = reviewer_match.group(1).strip() if reviewer_match else ""
    
    # Extract date
    date_match = re.search(r"\*\*Date:\*\*\s*(.*)", content, re.IGNORECASE)
    date = date_match.group(1).strip() if date_match else ""
    
    # Extract scope (supports **Scope:** or **Approval Scope:**)
    scope_match = re.search(r"\*\*(?:Approval\s+)?Scope:\*\*\s*(.*)", content, re.IGNORECASE)
    actual_scope = scope_match.group(1).strip().lower() if scope_match else "unknown"
    
    findings = []
    failure_modes = []
    
    # Decision authority logic
    is_approved = False
    if "approved" in decision:
        is_approved = True
    elif decision == "unknown" and status == "approved":
        # Fallback for legacy files
        is_approved = True
    
    if not is_approved:
        findings.append(f"Decision is '{decision}', expected 'approved'")
        failure_modes.append("review_not_approved")
    
    # Governance checks
    if not reviewer:
        findings.append("Missing 'Reviewer' field")
        failure_modes.append("missing_reviewer")
    
    if not date:
        findings.append("Missing 'Date' field")
        failure_modes.append("missing_date")
    
    # Map requested_scope to expected artifact scope
    scope_map = {
        "stable": "stable_promotion_authorized",
        "workflow": "workflow_promotion_authorized"
    }
    expected_scope = scope_map.get(requested_scope, requested_scope)
    
    if actual_scope != expected_scope:
        findings.append(f"Scope is '{actual_scope}', expected '{expected_scope}'")
        failure_modes.append("scope_mismatch")
        
    if not findings:
        return ValidatorResult(
            status="pass",
            validator_name="human_review",
            findings=[f"Human review authorized by {reviewer} on {date} for scope: {actual_scope}"],
            artifact_path=str(path),
            checked_scope=requested_scope
        )
    else:
        return ValidatorResult(
            status="fail",
            validator_name="human_review",
            findings=findings,
            failure_modes=failure_modes,
            artifact_path=str(path),
            checked_scope=requested_scope
        )
