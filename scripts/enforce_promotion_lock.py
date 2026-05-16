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
            
        # External skills do not have promotion evidence or SKILL.md validation requirements in this repository
        if skill.get("workflow_position") == "external":
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
                # In Phase 3, we require the skill_hash for all stable/certified skills
                print(f"  [FAIL] Legacy reference record for {name}: Missing mandatory SKILL.md hash.")
                missing_records.append(name)
                continue
            
            skill_md = REPO_ROOT / "skills" / name / "SKILL.md"
            if skill_md.exists() and stored_hash:
                current_hash = get_content_hash(skill_md)
                if current_hash != stored_hash:
                    locked_skills.append(name)

            # Audit Validator Ecosystem (Certification Integrity Check)
            stored_v_hashes = record.get("metadata", {}).get("validator_hashes")
            if stored_v_hashes:
                validators_dir = REPO_ROOT / "scripts" / "validators"
                v_drift = []
                for v_name, s_hash in stored_v_hashes.items():
                    v_file = validators_dir / v_name
                    if v_file.exists():
                        c_hash = get_content_hash(v_file)
                        if c_hash != s_hash:
                            v_drift.append(v_name)
                if v_drift:
                    print(f"  [WARN] Certification Integrity Warning for {name}: Validators have drifted: {', '.join(v_drift)}")
        except Exception as e:
            print(f"  [ERROR] Failed to audit {name}: {e}")
            error_skills.append(name)

    # 2. Workflow Promotion Lock (ADR 0009)
    wf_registry_path = REPO_ROOT / "skills" / "workflow-orchestrator" / "references" / "workflow-registry.yaml"
    wf_record_path = REPO_ROOT / "skills" / "workflow-orchestrator" / "references" / "workflow_reference_record.json"
    
    if wf_registry_path.exists():
        if not wf_record_path.exists():
            print(f"  [FAIL] Missing workflow_reference_record.json for workflow registry.")
            missing_records.append("workflow-orchestrator")
        else:
            try:
                wf_record = json.loads(wf_record_path.read_text(encoding="utf-8"))
                stored_wf_hash = wf_record.get("metadata", {}).get("registry_hash")
                
                if stored_wf_hash:
                    current_wf_hash = get_content_hash(wf_registry_path)
                    if current_wf_hash != stored_wf_hash:
                        print(f"  [FAIL] Workflow Registry Drift: workflow-registry.yaml has changed since last certification.")
                        locked_skills.append("workflow-orchestrator")
                else:
                    print(f"  [FAIL] Workflow reference record missing mandatory registry_hash.")
                    missing_records.append("workflow-orchestrator")
            except Exception as e:
                print(f"  [ERROR] Failed to audit workflow registry: {e}")
                error_skills.append("workflow-orchestrator")

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
