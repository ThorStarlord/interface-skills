import os
import json
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
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
        review_path = run_dir / "HUMAN-REVIEW.md"
        if not review_path.exists():
            review_path = run_dir / "HUMAN-WORKFLOW-REVIEW.md"
            
        if not review_path.exists():
            print(f"  - [SKIP] {run_dir.name}: No Human Review found.")
            continue
            
        review_content = review_path.read_text(encoding="utf-8")
        import re
        decision_match = re.search(r"\*\*Decision:\*\*\s*approved", review_content)
        if not decision_match:
            print(f"  - [SKIP] {run_dir.name}: Human review exists but not 'approved'.")
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
                
                # Update reference metadata
                ref_meta_path = skill_ref_dir / "reference_record.json"
                meta = {}
                if ref_meta_path.exists():
                    try:
                        meta = json.loads(ref_meta_path.read_text(encoding="utf-8"))
                    except: pass
                
                # Calculate hash for integrity check
                content = artifact_path.read_text(encoding="utf-8")
                import hashlib
                artifact_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()

                meta[dest_name] = {
                    "last_synced": manifest.get("timestamp"),
                    "source_run": manifest.get("run_id"),
                    "status": "verified_gold_standard",
                    "sha256": artifact_hash
                }
                
                ref_meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")

        # After syncing the latest verified run, we stop (idempotency/safety)
        break

if __name__ == "__main__":
    sync_references()
