import sys
import json
import hashlib
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
SKILLS_FILE = REPO_ROOT / "skills.json"

def get_content_hash(path):
    if not path.exists(): return None
    return hashlib.sha256(path.read_bytes()).hexdigest()

def check_promotion_lock():
    """
    Enforces the Registry Promotion Lock (ADR 0008).
    Prevents unauthorized status changes in the registry if the underlying 
    SKILL.md has drifted from the curated gold-standard evidence.
    """
    if not SKILLS_FILE.exists():
        print("skills.json not found.")
        return True

    try:
        registry = json.loads(SKILLS_FILE.read_text(encoding="utf-8"))
    except Exception as e:
        print(f"Failed to parse skills.json: {e}")
        return False

    locked_skills = []
    missing_records = []
    error_skills = []

    for skill in registry.get("skills", []):
        name = skill["name"]
        status = skill.get("status")
        
        # Lock applies to skills that are already promoted to high-trust levels
        if status not in ("stable", "certified"): 
            continue
        
        ref_dir = REPO_ROOT / "skills" / name / "references"
        record_path = ref_dir / "reference_record.json"
        
        if not record_path.exists():
            # ADR 0008: Stable skills SHOULD have reference evidence.
            # In Phase 3, we enforce this as a failure state.
            print(f"  [FAIL] Missing reference_record.json for {status} skill: {name}")
            missing_records.append(name)
            continue
            
        try:
            record = json.loads(record_path.read_text(encoding="utf-8"))
            
            # Support both NEW schema (nested metadata) and LEGACY schema (flat)
            stored_hash = None
            if "metadata" in record:
                stored_hash = record["metadata"].get("skill_hash")
            else:
                # In legacy schema, we don't have skill_hash, but we might have 
                # hashes for individual artifacts. For now, we skip if metadata is missing
                # but warn that the lock is incomplete.
                print(f"  [WARN] Legacy reference record for {name}: Missing SKILL.md hash.")
            
            skill_md = REPO_ROOT / "skills" / name / "SKILL.md"
            if skill_md.exists() and stored_hash:
                current_hash = get_content_hash(skill_md)
                if current_hash != stored_hash:
                    locked_skills.append(name)
        except Exception as e:
            print(f"  [ERROR] Failed to audit {name}: {e}")
            error_skills.append(name)

    if locked_skills or missing_records or error_skills:
        print("\n>>> [CRITICAL] REGISTRY PROMOTION LOCK ACTIVE")
        if locked_skills:
            print("The following skills have drifted from their certified gold-standard:")
            for name in locked_skills:
                print(f"  - {name} (Hash Mismatch)")
        if missing_records:
            print("The following stable/certified skills are missing mandatory reference records:")
            for name in missing_records:
                print(f"  - {name} (Missing Evidence)")
        if error_skills:
            print("The following skills could not be audited due to internal errors:")
            for name in error_skills:
                print(f"  - {name} (Audit Error)")
                
        print("\nRegistry status updates or metadata changes for these skills are BLOCKED.")
        print("To release the lock, you must:")
        print("1. Run the promotion harness and obtain human approval for the new state.")
        print("2. Run 'python scripts/sync_reference_evidence.py' to update the gold-standard record.")
        print("-" * 60)
        return False

    print(">>> Promotion lock verified: All stable skill evidence is current and synchronized.")
    return True

if __name__ == "__main__":
    if not check_promotion_lock():
        sys.exit(1)
    sys.exit(0)
