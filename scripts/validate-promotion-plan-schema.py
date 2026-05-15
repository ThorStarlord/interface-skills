import yaml
import os
import sys

# Repo-relative path
PLAN_PATH = "promotion-plan.yaml"

def validate_schema():
    if not os.path.exists(PLAN_PATH):
        print(f"Error: {PLAN_PATH} not found.")
        sys.exit(1)

    with open(PLAN_PATH, "r") as f:
        plan = yaml.safe_load(f)
    
    skills = plan.get("skills", {})
    
    errors = []

    # Candidate skills MUST have behavioral_criteria
    candidates = ["ui-surface-inventory", "ui-to-issues"]
    for skill_name in candidates:
        if skill_name not in skills:
            errors.append(f"Skill '{skill_name}' missing from promotion-plan.yaml")
            continue
        
        skill = skills[skill_name]
        if "behavioral_criteria" not in skill:
            errors.append(f"Skill '{skill_name}' missing 'behavioral_criteria' block")
            continue
        
        criteria = skill["behavioral_criteria"]
        required_fields = ["fixture_family", "minimum_behavioral_complexity", "blocking_failure_modes"]
        for field in required_fields:
            if field not in criteria:
                errors.append(f"Skill '{skill_name}' criteria missing '{field}'")

    if errors:
        for error in errors:
            print(f"Schema Error: {error}")
        sys.exit(1)
    else:
        print("Promotion Plan schema validation passed for candidate skills.")

if __name__ == "__main__":
    validate_schema()
