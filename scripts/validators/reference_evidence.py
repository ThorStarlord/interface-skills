from pathlib import Path
from .common import ValidatorResult

import json

def validate_reference_evidence(skill_name, reference_dir, requested_scope="stable"):
    """
    Validates the curated Promotion Reference Evidence (Gold Standard).
    """
    path = Path(reference_dir)
    
    if not path.exists():
        return ValidatorResult(
            status="fail",
            validator_name="reference_evidence",
            findings=[f"Reference directory not found for {skill_name}"],
            failure_modes=["missing_reference_dir"]
        )

    findings = []
    failure_modes = []
    
    # 1. Reference Record Presence & Approval Traceability
    record_path = path / "reference_record.json"
    authorizing_run_id = None
    if not record_path.exists():
        findings.append(f"Reference for '{skill_name}' is missing reference_record.json")
        failure_modes.append("missing_reference_record")
    else:
        try:
            record = json.loads(record_path.read_text(encoding="utf-8"))
            findings.append("Reference record found and parsed.")
            
            # 1.1 Approval Traceability (ADR 0008)
            approval_meta = record.get("approval_metadata", {})
            authorizing_run_id = approval_meta.get("authorizing_run_id")
            if not authorizing_run_id:
                findings.append("Traceability failure: reference_record.json is missing 'authorizing_run_id'")
                failure_modes.append("missing_approval_traceability")
            else:
                findings.append(f"Approval Traceability Verified: Authorizing Run ID: {authorizing_run_id}")

            # 2. Artifact Completeness
            artifacts = record.get("artifacts", {}) if "artifacts" in record else record
            for artifact_name, meta in artifacts.items():
                if artifact_name in ("approval_metadata", "metadata"): continue
                
                artifact_path = path / artifact_name
                if not artifact_path.exists():
                    findings.append(f"Missing referenced artifact: {artifact_name}")
                    failure_modes.append("incomplete_reference")
                else:
                    findings.append(f"Artifact '{artifact_name}' verified (source: {meta.get('source_run', 'unknown')})")
        except Exception as e:
            findings.append(f"Failed to parse reference_record.json: {str(e)}")
            failure_modes.append("corrupt_reference_record")

    # 3. Governance Evidence (HUMAN-REVIEW.md)
    review_path = path / "HUMAN-REVIEW.md"
    if not review_path.exists():
        review_path = path / "HUMAN-WORKFLOW-REVIEW.md"
        
    if not review_path.exists():
        findings.append(f"Reference for '{skill_name}' is missing authorizing HUMAN-REVIEW.md")
        failure_modes.append("missing_governance_evidence")
    else:
        findings.append(f"Authorizing governance artifact found: {review_path.name}")
        # Call full delegated validator (ADR 0008)
        from .human_review import validate_human_review
        from .human_workflow_review import validate_human_workflow_review
        
        if review_path.name == "HUMAN-WORKFLOW-REVIEW.md":
            h_result = validate_human_workflow_review(review_path, requested_scope)
        else:
            h_result = validate_human_review(review_path, requested_scope)
            
        if h_result.status != "pass":
            findings.extend(h_result.findings)
            failure_modes.extend(h_result.failure_modes)
        
        # Verify Traceability (Run ID Match)
        if authorizing_run_id:
            content = review_path.read_text(encoding="utf-8")
            if authorizing_run_id not in content:
                findings.append(f"Traceability failure: Authorizing Run ID '{authorizing_run_id}' not mentioned in {review_path.name}")
                failure_modes.append("traceability_mismatch")


    # 4. Cleanliness (Strict Dirty-Reference Detection)
    allowed_files = {"reference_record.json", "HUMAN-REVIEW.md", "SOURCE.md", "source-run.txt"}
    allowed_extensions = {'.md', '.json', '.png', '.jpg', '.pdf'}
    
    current_files = [f for f in path.glob("*") if f.is_file()]
    junk_files = []
    for f in current_files:
        if f.name in allowed_files: continue
        if f.suffix in allowed_extensions: continue
        junk_files.append(f.name)
        
    if junk_files:
        findings.append(f"Dirty reference directory: Unauthorized files found: {', '.join(junk_files)}")
        failure_modes.append("dirty_reference")
    else:
        findings.append("Reference directory cleanliness verified.")

    # 5. Promotion Lock (Staleness Check - ADR 0008)
    if record_path.exists():
        import hashlib
        def get_content_hash(path):
            if not path.exists(): return None
            return hashlib.sha256(path.read_bytes()).hexdigest()

        try:
            record = json.loads(record_path.read_text(encoding="utf-8"))
            stored_hash = record.get("metadata", {}).get("skill_hash")
            
            skill_md = Path("skills") / skill_name / "SKILL.md"
            if skill_md.exists() and stored_hash:
                current_hash = get_content_hash(skill_md)
                if current_hash != stored_hash:
                    findings.append(f"STALE REFERENCE: Skill '{skill_name}' has been modified since reference evidence was curated.")
                    failure_modes.append("stale_reference_evidence")
                    findings.append("> [!CAUTION]")
                    findings.append("> **Promotion Lock Active:** Registry update is blocked until reference evidence is resynchronized.")
                else:
                    findings.append("Reference evidence is current and synchronized with SKILL.md.")
        except Exception:
            pass

    status = "pass" if not failure_modes else "fail"
    return ValidatorResult(
        status=status,
        validator_name="reference_evidence",
        findings=findings,
        failure_modes=failure_modes
    )

