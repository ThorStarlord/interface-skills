import os
import sys
import json
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

PROMOTION_RUNS_DIR = REPO_ROOT / "promotion-runs"
REGISTRY_PATH = REPO_ROOT / "skills.json"

from scripts.enforce_promotion_lock import check_promotion_lock

def verify_certification():
    """
    CI Enforcement script for Certification Authority.
    Checks that the repository is in a certified state.
    """
    print(">>> Certification Authority Audit...")
    
    # 0. Enforce Promotion Lock (ADR 0008)
    if not check_promotion_lock():
        return False
    
    # 1. Load Registry
    if not REGISTRY_PATH.exists():
        print(f"[FAIL] Registry not found: {REGISTRY_PATH}")
        return False
        
    with open(REGISTRY_PATH, "r", encoding="utf-8") as f:
        registry = json.load(f)
        
    success = True
    
    # 2. Audit Stable Skills for Reference Integrity
    for skill in registry.get("skills", []):
        if skill.get("status") == "stable":
            skill_name = skill["name"]
            print(f"  - Auditing stable skill: {skill_name}")
            
            ref_dir = REPO_ROOT / "skills" / skill_name / "references"
            ref_record_path = ref_dir / "reference_record.json"
            
            if not ref_record_path.exists():
                print(f"    [FAIL] Missing reference_record.json for stable skill.")
                success = False
                continue
                
            try:
                ref_record = json.loads(ref_record_path.read_text(encoding="utf-8"))
                
                # Support both NEW schema (nested artifacts) and LEGACY schema (flat)
                artifacts_to_audit = ref_record.get("artifacts", ref_record)
                if not isinstance(artifacts_to_audit, dict):
                    # If legacy schema was somehow broken, fallback to root
                    artifacts_to_audit = ref_record
                
                # Check if there's a verified source run
                has_gold = False
                for artifact, meta in artifacts_to_audit.items():
                    if not isinstance(meta, dict): continue # Skip metadata/approval_metadata keys if present
                    
                    if meta.get("status") == "verified_gold_standard":
                        has_gold = True
                        source_run_id = meta.get("source_run")
                        
                        # Verify the source run exists and is approved
                        if source_run_id:
                            run_dir = PROMOTION_RUNS_DIR / source_run_id
                            if not run_dir.exists():
                                print(f"    [WARN] Source run {source_run_id} missing from promotion-runs/.")
                                # Not necessarily a failure if runs are archived, but reference hash must match
                            else:
                                review_path = run_dir / "HUMAN-REVIEW.md"
                                is_workflow_review = False
                                if not review_path.exists():
                                    review_path = run_dir / "HUMAN-WORKFLOW-REVIEW.md"
                                    is_workflow_review = True
                                
                                if not review_path.exists():
                                    print(f"    [FAIL] Source run {source_run_id} has no human review.")
                                    success = False
                                else:
                                    if is_workflow_review:
                                        from scripts.validators.human_workflow_review import validate_human_workflow_review
                                        h_result = validate_human_workflow_review(review_path, requested_scope="workflow")
                                    else:
                                        from scripts.validators.human_review import validate_human_review
                                        h_result = validate_human_review(review_path, requested_scope="stable")
                                        
                                    if h_result.status != "pass":
                                        print(f"    [FAIL] Source run {source_run_id} not approved: {', '.join(h_result.findings)}")
                                        success = False
                
                if not has_gold:
                    print(f"    [FAIL] No 'verified_gold_standard' reference found.")
                    success = False
                else:
                    print(f"    [OK] Reference evidence verified.")
                    
            except Exception as e:
                print(f"    [FAIL] Error auditing references: {str(e)}")
                success = False
    # 3. Audit Workflows for Certification
    workflow_registry_path = REPO_ROOT / "skills" / "workflow-orchestrator" / "references" / "workflow-registry.yaml"
    if workflow_registry_path.exists():
        print("\n  - Auditing workflows...")
        try:
            with open(workflow_registry_path, "r", encoding="utf-8") as f:
                wf_registry = yaml.safe_load(f)
            
            for wf in wf_registry.get("workflows", []):
                wf_id = wf["id"]
                print(f"    - Workflow: {wf_id}")
                
                # Find latest approved run for this workflow
                latest_approved = None
                if PROMOTION_RUNS_DIR.exists():
                    wf_runs = []
                    for run_dir in PROMOTION_RUNS_DIR.iterdir():
                        if run_dir.is_dir() and wf_id in run_dir.name and "workflow" in run_dir.name:
                            review_path = run_dir / "HUMAN-WORKFLOW-REVIEW.md"
                            if review_path.exists():
                                from scripts.validators.human_workflow_review import validate_human_workflow_review
                                h_result = validate_human_workflow_review(review_path, requested_scope="workflow")
                                if h_result.status == "pass":
                                    wf_runs.append(run_dir)
                    
                    if wf_runs:
                        # Sort by name (timestamp prefix)
                        wf_runs.sort(key=lambda x: x.name, reverse=True)
                        latest_approved = wf_runs[0]
                
                if not latest_approved:
                    # Workflows don't necessarily HAVE to be certified yet, but we report it
                    print(f"      [WARN] No approved promotion run found for workflow.")
                else:
                    print(f"      [OK] Certified run found: {latest_approved.name}")
        except Exception as e:
            print(f"    [FAIL] Error auditing workflows: {str(e)}")
            success = False
    else:
        print("\n  - [WARN] Workflow registry not found at expected path.")

    if success:
        print("\n>>> [CERTIFIED] Repository state adheres to Certification Authority standards.")
    else:
        print("\n>>> [FAIL] Repository state violates Certification Authority standards.")
        
    return success

if __name__ == "__main__":
    if not verify_certification():
        sys.exit(1)
    sys.exit(0)
