import subprocess
import sys
import os
import re
import json
import yaml
from pathlib import Path

def run_command(command):
    print(f"Running: {' '.join(command)}")
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"[FAIL] {result.stderr}")
        return False
    print(f"[PASS] {result.stdout.strip().splitlines()[-1] if result.stdout.strip() else 'Success'}")
    return True

def check_registry_consistency(skill_name):
    passed = True
    
    # Check SKILL.md
    skill_md_path = Path("skills") / skill_name / "SKILL.md"
    if not skill_md_path.exists():
        print(f"[FAIL] {skill_md_path} not found.")
        return False
    
    content = skill_md_path.read_text(encoding="utf-8")
    if "status: stable" not in content:
        print(f"[FAIL] SKILL.md does not have 'status: stable'")
        passed = False
    if "## Output template" not in content:
        print(f"[FAIL] SKILL.md is missing '## Output template'")
        passed = False
        
    # Check README.md
    readme_path = Path("README.md")
    if readme_path.exists():
        readme_lines = readme_path.read_text(encoding="utf-8").splitlines()
        for line in readme_lines:
            # Check if this line is the definition row for the skill
            # Format usually: | `skill-name` | ... or - `skill-name`: ... or 1. `skill-name`
            stripped = line.strip()
            if stripped.startswith(f"| `{skill_name}`") or stripped.startswith(f"- `{skill_name}`") or re.match(rf"^\d+\.\s+`{skill_name}`", stripped):
                if "⚠️" in line or "[DRAFT]" in line.upper() or "draft" in line.lower():
                    print(f"[FAIL] README.md has draft marker for {skill_name}")
                    passed = False
                    break
                
    # Check docs/skill-reference.md
    reference_path = Path("docs") / "skill-reference.md"
    if reference_path.exists():
        ref_lines = reference_path.read_text(encoding="utf-8").splitlines()
        for line in ref_lines:
            stripped = line.strip()
            if stripped.startswith(f"| `{skill_name}`") or stripped.startswith(f"- `{skill_name}`") or re.match(rf"^\d+\.\s+`{skill_name}`", stripped):
                if "⚠️" in line or "[DRAFT]" in line.upper() or "draft" in line.lower():
                    print(f"[FAIL] docs/skill-reference.md has draft marker for {skill_name}")
                    passed = False
                    break
                
    # Check promotion-plan.yaml
    plan_path = Path("promotion-plan.yaml")
    if plan_path.exists():
        with open(plan_path, "r", encoding="utf-8") as f:
            plan = yaml.safe_load(f)
            if skill_name not in plan.get("skills", {}):
                print(f"[FAIL] promotion-plan.yaml is missing {skill_name}")
                passed = False
                
    if passed:
        print(f"[PASS] Registry consistency valid for {skill_name}")
    return passed

def main():
    with open("skills.json", "r", encoding="utf-8") as f:
        registry = json.load(f)
        
    stable_skills = [s["name"] for s in registry.get("skills", []) if s.get("status") == "stable" and s.get("workflow_position") != "external" and Path("skills", s["name"], "SKILL.md").exists()]


    all_passed = True

    print("=== Stable Skill Regression Guard ===\n")

    for skill in stable_skills:
        print(f"Checking {skill}...")
        
        # 1. Structural validation
        if not run_command(["python", "scripts/validate-skill.py", "--skill", skill]):
            all_passed = False
            
        # 2. Registry Consistency
        if not check_registry_consistency(skill):
            all_passed = False
            
        # 2. Promotion suite pass (validation mode)
        if not run_command(["python", "scripts/run-promotion-suite.py", "--skill", skill]):
            all_passed = False
        
        print("-" * 40)

    if all_passed:
        print("\n[SUCCESS] All stable skills passed regression.")
        sys.exit(0)
    else:
        print("\n[FAIL] Some stable skills failed regression.")
        sys.exit(1)

if __name__ == "__main__":
    main()
