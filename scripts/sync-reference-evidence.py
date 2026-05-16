#!/usr/bin/env python3
"""
scripts/sync-reference-evidence.py

Synchronizes successful promotion run artifacts into the canonical reference evidence (Gold Standard).
This implements the automated evidence lifecycle for the Skill Certification System.

Usage:
  python scripts/sync-reference-evidence.py --run 2026-05-16-1234 --skill ui-orchestrator
"""

import argparse
import os
import json
import shutil
import hashlib
from pathlib import Path
from datetime import datetime

REPO_ROOT = Path(__file__).parent.parent
PROMOTION_RUNS_DIR = REPO_ROOT / "promotion-runs"

def get_content_hash(path):
    if not path.exists(): return None
    return hashlib.sha256(path.read_bytes()).hexdigest()

def sync_evidence(run_id, skill_name):
    print(f">>> Synchronizing Evidence for {skill_name} from run {run_id}")
    
    run_dir = PROMOTION_RUNS_DIR / run_id
    if not run_dir.exists():
        print(f"Error: Run directory {run_id} not found.")
        return False
        
    skill_ref_dir = REPO_ROOT / "skills" / skill_name / "references"
    skill_ref_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Find the result manifest
    # We look for successful results in the run
    fixtures_found = 0
    reference_record = {}
    
    # Add skill hash for Promotion Lock
    skill_md = REPO_ROOT / "skills" / skill_name / "SKILL.md"
    skill_hash = get_content_hash(skill_md)
    
    metadata = {
        "source_run": run_id,
        "synced_at": datetime.now().isoformat(),
        "skill_hash": skill_hash
    }
    
    for res_file in run_dir.glob("*/result.json"):
        with open(res_file, "r") as f:
            res = json.load(f)
            
        if res.get("classification") == "pass":
            fixture_name = res["fixture"]
            artifact_rel = res.get("pointers", {}).get("output_artifact")
            
            if artifact_rel:
                artifact_path = REPO_ROOT / artifact_rel
                if artifact_path.exists():
                    target_name = f"{fixture_name}_{artifact_path.name}"
                    shutil.copy2(artifact_path, skill_ref_dir / target_name)
                    
                    reference_record[target_name] = {
                        "fixture": fixture_name,
                        "source_path": artifact_rel,
                        "hash": get_content_hash(artifact_path),
                        "source_run": run_id
                    }
                    fixtures_found += 1
    
    # 2. Copy Human Review
    # We look for the top-level HUMAN-REVIEW.md (formal authorization) 
    # or the fixture-level review.md if not present.
    formal_review = run_dir / "HUMAN-REVIEW.md"
    if formal_review.exists():
        shutil.copy2(formal_review, skill_ref_dir / "HUMAN-REVIEW.md")
        print("    Curated formal HUMAN-REVIEW.md")
    else:
        # Fallback to the first fixture review if formal is missing (legacy support)
        fixture_reviews = list(run_dir.glob("*/review.md"))
        if fixture_reviews:
            shutil.copy2(fixture_reviews[0], skill_ref_dir / "HUMAN-REVIEW.md")
            print(f"    Curated fixture review as fallback: {fixture_reviews[0].parent.name}")

    # 3. Write Reference Record
    record_path = skill_ref_dir / "reference_record.json"
    full_record = {
        "metadata": metadata,
        "artifacts": reference_record
    }
    
    with open(record_path, "w", encoding="utf-8") as f:
        json.dump(full_record, f, indent=2)
        
    print(f"    Done. Synced {fixtures_found} artifacts to {skill_ref_dir.relative_to(REPO_ROOT)}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Sync promotion evidence")
    parser.add_argument("--run", required=True, help="Promotion Run ID")
    parser.add_argument("--skill", required=True, help="Skill Name")
    
    args = parser.parse_args()
    
    if sync_evidence(args.run, args.skill):
        print("\n>>> Evidence synchronized successfully. Promotion Lock updated.")
    else:
        sys.exit(1)

if __name__ == "__main__":
    main()
