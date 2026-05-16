import os
import sys
import json
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

PROMOTION_RUNS_DIR = REPO_ROOT / "promotion-runs"

def sync_references():
    """
    Synchronizes successful promotion run artifacts to skill reference directories.
    This is the core of Phase 3 Reference Lifecycle Management.
    """
    if not PROMOTION_RUNS_DIR.exists():
        print("No promotion runs to sync.")
        return

    # Find the latest successful run
    runs = []
    for run_dir in PROMOTION_RUNS_DIR.iterdir():
        if run_dir.is_dir():
            manifest_path = run_dir / "MANIFEST.json"
            if manifest_path.exists():
                try:
                    with open(manifest_path, "r", encoding="utf-8") as f:
                        runs.append((run_dir, json.load(f)))
                except: pass
    
    # Sort by timestamp desc
    runs.sort(key=lambda x: x[1].get("timestamp", ""), reverse=True)

    for run_dir, manifest in runs:
        # Check if this run is "Verified" (all steps passed)
        all_passed = all(s.get("status") == "pass" for s in manifest.get("steps", []))
        if not all_passed:
            continue
            
        # 1. Human Approval Gate (ADR 0008 Hardening)
        from scripts.validators.human_review import validate_human_review
        from scripts.validators.human_workflow_review import validate_human_workflow_review
        
        review_path = run_dir / "HUMAN-REVIEW.md"
        requested_scope = "stable" # Default for skill sync
        
        if not review_path.exists():
            review_path = run_dir / "HUMAN-WORKFLOW-REVIEW.md"
            requested_scope = "workflow"
            
        if not review_path.exists():
            print(f"  - [SKIP] {run_dir.name}: No Human Review found.")
            continue
            
        if requested_scope == "workflow":
            h_result = validate_human_workflow_review(review_path, requested_scope)
        else:
            h_result = validate_human_review(review_path, requested_scope)
            
        if h_result.status != "pass":
            print(f"  - [SKIP] {run_dir.name}: Human review not approved or scope mismatch: {', '.join(h_result.findings)}")
            continue

        print(f"\n>>> Syncing Approved Gold Standard: {manifest.get('run_id')}")
        
        for step in manifest.get("steps", []):
            skill_name = step.get("skill")
            artifact_rel = step.get("artifact")
            
            if not skill_name or not artifact_rel:
                continue
                
            skill_ref_dir = REPO_ROOT / "skills" / skill_name / "references"
            artifact_path = REPO_ROOT / artifact_rel
            
            if artifact_path.exists():
                skill_ref_dir.mkdir(parents=True, exist_ok=True)
                
                # Copy artifact to skill references
                dest_name = artifact_path.name
                dest_path = skill_ref_dir / dest_name
                
                # In Phase 3, we also generate/update a reference manifest
                print(f"  - Syncing {skill_name}: {dest_name}")
                shutil.copy2(artifact_path, dest_path)
                
                # Update reference metadata (ADR 0008 Schema)
                ref_meta_path = skill_ref_dir / "reference_record.json"
                meta = {"artifacts": {}, "approval_metadata": {}, "metadata": {}}
                if ref_meta_path.exists():
                    try:
                        old_meta = json.loads(ref_meta_path.read_text(encoding="utf-8"))
                        if "artifacts" in old_meta:
                            meta = old_meta
                        else:
                            # Migrate legacy schema
                            meta["artifacts"] = old_meta
                    except: pass
                
                # Calculate hash for integrity check
                content = artifact_path.read_text(encoding="utf-8")
                import hashlib
                artifact_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

                meta["artifacts"][dest_name] = {
                    "last_synced": manifest.get("timestamp"),
                    "source_run": manifest.get("run_id"),
                    "status": "verified_gold_standard",
                    "sha256": artifact_hash
                }
                
                meta["approval_metadata"] = {
                    "authorizing_run_id": manifest.get("run_id"),
                    "approval_type": "human_review" if review_path.name == "HUMAN-REVIEW.md" else "human_workflow_review",
                    "sync_date": manifest.get("timestamp")
                }
                
                # Add skill hash for staleness detection (ADR 0008)
                skill_md = REPO_ROOT / "skills" / skill_name / "SKILL.md"
                if skill_md.exists():
                    meta["metadata"]["skill_hash"] = hashlib.sha256(skill_md.read_bytes()).hexdigest()

                ref_meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
                
                # Copy the review itself as part of the gold standard evidence
                shutil.copy2(review_path, skill_ref_dir / review_path.name)


        # After syncing the latest verified run, we stop (idempotency/safety)
        break

if __name__ == "__main__":
    sync_references()
