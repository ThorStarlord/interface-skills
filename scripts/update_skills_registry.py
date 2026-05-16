import json
import os
from pathlib import Path

from scripts.enforce_promotion_lock import check_promotion_lock

REPO_ROOT = Path(__file__).resolve().parent.parent
SKILLS_DIR = REPO_ROOT / "skills"
SKILLS_JSON = REPO_ROOT / "skills.json"

def update_registry():
    # 0. Enforce Promotion Lock (ADR 0008)
    if not check_promotion_lock():
        print("Registry update ABORTED: Promotion Lock is active.")
        return

    with open(SKILLS_JSON, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    existing_skill_names = {s['name'] for s in data['skills']}
    
    new_skills = []
    for skill_dir in SKILLS_DIR.iterdir():
        if not skill_dir.is_dir():
            continue
        
        name = skill_dir.name
        if name in existing_skill_names:
            continue
            
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            continue
            
        # Basic entry for new skills
        description = f"External skill: {name}"
        if name.startswith("mp-"):
            description = f"Matt Pocock skill: {name[3:]}"
            
        new_skills.append({
            "name": name,
            "status": "stable",
            "description": description,
            "input": "N/A",
            "output": "N/A",
            "workflow_position": "external",
            "next": []
        })
    
    if new_skills:
        data['skills'].extend(new_skills)
        with open(SKILLS_JSON, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"Added {len(new_skills)} new skills to skills.json")
    else:
        print("No new skills to add to registry.")

if __name__ == "__main__":
    update_registry()
