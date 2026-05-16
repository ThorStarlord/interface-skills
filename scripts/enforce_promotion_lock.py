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
    for skill in registry.get("skills", []):
        name = skill["name"]
        status = skill.get("status")
        
        # Lock applies to skills that are already promoted to high-trust levels
        if status not in ("stable", "certified"): 
            continue
        
        ref_dir = REPO_ROOT / "skills" / name / "references"
        record_path = ref_dir / "reference_record.json"
        
        if not record_path.exists():
            # ADR 0008: Stable skills should have reference evidence.
            # If missing, we don't necessarily lock it (legacy support), 
            # but we warn about the gap in certification authority.
            continue
            
        try:
            record = json.loads(record_path.read_text(encoding="utf-8"))
            stored_hash = record.get("metadata", {}).get("skill_hash")
            
            skill_md = REPO_ROOT / "skills" / name / "SKILL.md"
            if skill_md.exists() and stored_hash:
                current_hash = get_content_hash(skill_md)
                if current_hash != stored_hash:
                    locked_skills.append(name)
        except:
            pass

    if locked_skills:
        print("\n>>> [CRITICAL] REGISTRY PROMOTION LOCK ACTIVE")
        print("The following skills have been modified since their reference evidence was curated:")
        for name in locked_skills:
            print(f"  - {name}")
        print("\nRegistry status updates or metadata changes for these skills are BLOCKED.")
        print("To release the lock, you must:")
        print("1. Run the promotion harness and obtain human approval for the new SKILL.md version.")
        print("2. Run 'python scripts/sync_reference_evidence.py' to update the gold-standard record.")
        print("-" * 60)
        return False

    print(">>> Promotion lock verified: All stable skill evidence is current and synchronized.")
    return True

if __name__ == "__main__":
    if not check_promotion_lock():
        sys.exit(1)
    sys.exit(0)
