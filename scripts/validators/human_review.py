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
    
    # Extract decision (primary authority)
    decision_match = re.search(r"\*\*Decision:\*\*\s*(.*)", content, re.IGNORECASE)
    decision = decision_match.group(1).strip().lower() if decision_match else "unknown"
    
    # Extract status (fallback/legacy)
    status_match = re.search(r"\*\*Status:\*\*\s*(.*)", content, re.IGNORECASE)
    status = status_match.group(1).strip().lower() if status_match else "unknown"
    
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
    
    # 1. Decision Authority Enforcement (ADR 0008)
    allowed_decisions = ["approved", "rejected", "needs_revision"]
    
    is_approved = False
    if decision in allowed_decisions:
        if decision == "approved":
            is_approved = True
            findings.append("Decision verified: approved.")
        else:
            findings.append(f"Promotion blocked: Human review decision is '{decision}'")
            failure_modes.append("review_rejected")
    elif status == "approved":
        # Legacy fallback
        is_approved = True
        findings.append("Note: Using legacy 'Status: approved' as decision authority.")
    else:
        findings.append(f"Invalid or missing Decision: '{decision}'. Must be one of: {', '.join(allowed_decisions)}")
        failure_modes.append("invalid_decision_format")
    
    # 2. Governance Mandatory Fields
    if not reviewer or reviewer.lower() in ("tbd", "todo", "[name]"):
        findings.append("Governance failure: 'Reviewer' field is missing or placeholder")
        failure_modes.append("missing_reviewer")
    
    if not date or date.lower() in ("tbd", "todo", "[date]"):
        findings.append("Governance failure: 'Date' field is missing or placeholder")
        failure_modes.append("missing_date")

    # 3. Rich Template Validation
    mandatory_sections = ["Behavioral Review", "Continuity Review"]
    for section in mandatory_sections:
        if not re.search(fr"###\s+{section}", content, re.IGNORECASE):
            findings.append(f"Missing mandatory review section: '### {section}'")
            failure_modes.append("incomplete_template")

    # 4. Governance Audit (Run ID Traceability)
    # Check for Run ID link and verify it's not a placeholder
    run_id_match = re.search(r"Run\s+ID[^0-9]+([0-9]{4}-[0-9]{2}-[0-9]{2}[^\s\)]+)", content, re.IGNORECASE)
    if not run_id_match:
        findings.append("Governance failure: HUMAN-REVIEW.md is not linked to a specific PROMOTION-RUN ID")
        failure_modes.append("missing_traceability")
    else:
        run_id = run_id_match.group(1)
        # Verify it's in the current path if we are in a promotion-run directory
        if "promotion-runs" in str(path):
            current_run_id = path.parent.name
            if run_id != current_run_id:
                findings.append(f"Traceability mismatch: Review Run ID '{run_id}' does not match directory '{current_run_id}'")
                failure_modes.append("traceability_mismatch")
            else:
                findings.append(f"Governance verified: Linked to Run ID {run_id}")

    # 5. Scope Enforcement
    scope_map = {
        "stable": "stable_promotion_authorized",
        "workflow": "workflow_promotion_authorized"
    }
    expected_scope = scope_map.get(requested_scope, requested_scope)
    
    if actual_scope != expected_scope:
        findings.append(f"Scope mismatch: Review is for '{actual_scope}', but '{expected_scope}' was requested.")
        failure_modes.append("scope_mismatch")
    else:
        findings.append(f"Scope verified: {actual_scope}.")
        
    status = "pass" if not failure_modes else "fail"
    return ValidatorResult(
        status=status,
        validator_name="human_review",
        findings=findings,
        failure_modes=failure_modes,
        artifact_path=str(path),
        checked_scope=requested_scope
    )

