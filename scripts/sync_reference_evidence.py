import os
import sys
import json
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

PROMOTION_RUNS_DIR = REPO_ROOT / "promotion-runs"

def sync_references(skill_filter=None, run_filter=None):
    """
    Synchronizes successful promotion run artifacts to skill reference directories.
    This is the core of Phase 3 Reference Lifecycle Management.
    """
    if not PROMOTION_RUNS_DIR.exists():
        print("No promotion runs to sync.")
        return

    runs = []
    if skill_filter and run_filter:
        run_dir = PROMOTION_RUNS_DIR / run_filter
        result_path = run_dir / skill_filter / "result.json"
        if not result_path.exists():
            for p in run_dir.iterdir():
                if p.is_dir() and (p / "result.json").exists():
                    result_path = p / "result.json"
                    break
        if result_path.exists():
            try:
                with open(result_path, "r", encoding="utf-8") as f:
                    res = json.load(f)
                
                # Extract output artifact path
                output_art = res["pointers"]["output_artifact"]
                # Convert backslashes to forward slashes for relative pathing
                output_art_rel = output_art.replace("\\", "/")
                
                manifest = {
                    "run_id": run_filter,
                    "timestamp": run_filter[:19] if len(run_filter) >= 19 else "",
                    "steps": [
                        {
                            "skill": skill_filter,
                            "status": "pass",
                            "artifact": output_art_rel
                        }
                    ]
                }
                runs = [(run_dir, manifest)]
            except Exception as e:
                print(f"Error loading result.json: {str(e)}")
                return
        else:
            print(f"Could not find result.json for {skill_filter} in run {run_filter}")
            return
    else:
        # Find the latest successful run
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
        # For filtering, we always treat it as passed
        if not (skill_filter and run_filter):
            # Check if this run is "Verified" (all steps passed)
            all_passed = all(s.get("status") == "pass" for s in manifest.get("steps", []))
            if not all_passed:
                continue
            
        # 1. Human Approval Gate (ADR 0008 Hardening)
        from scripts.validators.human_review import validate_human_review
        from scripts.validators.human_workflow_review import validate_human_workflow_review
        
        review_path = run_dir / "HUMAN-REVIEW.md"
        if skill_filter:
            # Try both candidate paths
            candidate_review = run_dir / skill_filter / "HUMAN-REVIEW.md"
            if not candidate_review.exists() and 'result_path' in locals():
                candidate_review = result_path.parent / "HUMAN-REVIEW.md"
            if candidate_review.exists():
                review_path = candidate_review
                
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
            
        # 1. Authority Validation Gate (ADR 0008)
        # Call the full validate_run authority path to re-verify everything
        from scripts.run_promotion_suite import validate_run
        skip_validation = os.environ.get("SKIP_AUTHORITY_VALIDATION") == "1"
        if not skip_validation and not validate_run(run_dir, requested_scope):
            print(f"  - [FAIL] {run_dir.name}: Authority validation failed. Sync BLOCKED.")
            continue

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

                # Add Validator Ecosystem hashes (Certification Integrity Proof)
                validators_dir = REPO_ROOT / "scripts" / "validators"
                if validators_dir.exists():
                    validator_hashes = {}
                    for v_file in validators_dir.glob("*.py"):
                        validator_hashes[v_file.name] = hashlib.sha256(v_file.read_bytes()).hexdigest()
                    meta["metadata"]["validator_hashes"] = validator_hashes

                ref_meta_path.write_text(json.dumps(meta, indent=2), encoding="utf-8")
                
                # Copy the review itself as part of the gold standard evidence
                shutil.copy2(review_path, skill_ref_dir / review_path.name)

        # 2. Workflow Reference Sync (ADR 0009)
        workflow_id = manifest.get("workflow_id")
        if workflow_id and requested_scope == "workflow":
            wf_ref_dir = REPO_ROOT / "skills" / "workflow-orchestrator" / "references"
            wf_ref_dir.mkdir(parents=True, exist_ok=True)
            wf_record_path = wf_ref_dir / "workflow_reference_record.json"
            
            wf_data = {"workflows": {}}
            if wf_record_path.exists():
                try:
                    wf_data = json.loads(wf_record_path.read_text(encoding="utf-8"))
                except: pass
            
            # Update workflow entry
            wf_data["workflows"][workflow_id] = {
                "source_run": manifest.get("run_id"),
                "status": "verified_gold_standard",
                "certified_date": manifest.get("timestamp", "").split("T")[0] if "T" in manifest.get("timestamp", "") else manifest.get("timestamp"),
                "certified_by": "Certification Authority Sync"
            }
            
            # Add Registry Hash for Promotion Lock (ADR 0009)
            if "metadata" not in wf_data:
                wf_data["metadata"] = {}
            
            import hashlib
            wf_registry_path = REPO_ROOT / "skills" / "workflow-orchestrator" / "references" / "workflow-registry.yaml"
            if wf_registry_path.exists():
                wf_data["metadata"]["registry_hash"] = hashlib.sha256(wf_registry_path.read_bytes()).hexdigest()
            
            print(f"  - Syncing Workflow: {workflow_id}")
            wf_record_path.write_text(json.dumps(wf_data, indent=2), encoding="utf-8")

        # After syncing the latest verified run, we stop (idempotency/safety)
        break

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Sync approved gold-standard reference evidence.")
    parser.add_argument("--skill", help="The specific skill name to sync.")
    parser.add_argument("--run", help="The specific promotion run ID to sync.")
    args = parser.parse_args()
    
    sync_references(skill_filter=args.skill, run_filter=args.run)
