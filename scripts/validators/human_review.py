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
    
    # Extract status
    status_match = re.search(r"\*\*Status:\*\*\s*(.*)", content, re.IGNORECASE)
    status = status_match.group(1).strip().lower() if status_match else "unknown"
    
    # Extract scope
    scope_match = re.search(r"\*\*Scope:\*\*\s*(.*)", content, re.IGNORECASE)
    actual_scope = scope_match.group(1).strip().lower() if scope_match else "unknown"
    
    findings = []
    failure_modes = []
    
    if status != "approved":
        findings.append(f"Status is '{status}', expected 'approved'")
        failure_modes.append("review_not_approved")
    
    # Map requested_scope to expected artifact scope
    # stable -> stable_promotion_authorized
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
            findings=[f"Human review authorized for scope: {actual_scope}"],
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
