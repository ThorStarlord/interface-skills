import yaml
import json
from pathlib import Path
from .common import ValidatorResult

def validate_promotion_plan(plan_path, registry_path, repo_root=None):
    """
    Validates a promotion plan against the skill registry and filesystem.
    """
    path = Path(plan_path)
    reg_path = Path(registry_path)
    
    if not path.exists():
        return ValidatorResult(
            status="fail",
            validator_name="promotion_plan",
            findings=["promotion-plan.yaml not found"],
            failure_modes=["missing_config"]
        )
        
    if not reg_path.exists():
        return ValidatorResult(
            status="error",
            validator_name="promotion_plan",
            findings=["skills.json registry not found"],
            failure_modes=["registry_error"]
        )

    try:
        with open(path, "r") as f:
            plan = yaml.safe_load(f)
        with open(reg_path, "r") as f:
            registry = json.load(f)
    except Exception as e:
        return ValidatorResult(
            status="error",
            validator_name="promotion_plan",
            findings=[f"Failed to parse config: {str(e)}"],
            failure_modes=["parse_error"]
        )

    findings = []
    failure_modes = []
    
    # 1. Validate skills exist in registry
    plan_skills = plan.get("skills", {}).keys()
    
    # skills.json has a 'skills' key which is a list of dicts with 'name'
    reg_skills_list = registry.get("skills", [])
    reg_skills = {s["name"] for s in reg_skills_list if "name" in s}
    
    for skill in plan_skills:
        if skill not in reg_skills:
            findings.append(f"Skill '{skill}' in plan is missing from skills.json")
            failure_modes.append("missing_skill")
            continue
            
        # 2. Validate fixtures exist on disk
        skill_cfg = plan["skills"][skill]
        fixtures = list(skill_cfg.get("fixtures", []))
        messy = skill_cfg.get("messy_fixture")
        if messy:
            fixtures.append(messy)
            
        for fixture_rel in fixtures:
            # Resolve relative to repo_root if provided, otherwise assume current dir
            if repo_root:
                fixture_path = Path(repo_root) / fixture_rel
            else:
                fixture_path = Path(fixture_rel)
                
            if not fixture_path.exists():
                findings.append(f"Fixture path '{fixture_rel}' for skill '{skill}' not found on disk")
                failure_modes.append("missing_fixture")

        # 3. Validate behavioral_criteria (Mandatory for stable promotion)
        beh_crit = skill_cfg.get("behavioral_criteria")
        if not beh_crit:
            findings.append(f"Skill '{skill}' is missing 'behavioral_criteria'")
            failure_modes.append("missing_behavioral_criteria")
        else:
            if not beh_crit.get("fixture_family"):
                findings.append(f"Skill '{skill}' is missing 'fixture_family' in behavioral_criteria")
                failure_modes.append("missing_fixture_family")
            
            if not beh_crit.get("minimum_behavioral_complexity"):
                findings.append(f"Skill '{skill}' is missing 'minimum_behavioral_complexity' in behavioral_criteria")
                failure_modes.append("missing_complexity_metrics")
                
            blocking = beh_crit.get("blocking_failure_modes")
            if not blocking or not isinstance(blocking, list):
                findings.append(f"Skill '{skill}' is missing or has invalid 'blocking_failure_modes'")
                failure_modes.append("missing_blocking_failure_modes")

        # 4. Validate downstream coherence
        prom_crit = skill_cfg.get("promotion_criteria", {})
        if prom_crit.get("require_downstream"):
            downstream = skill_cfg.get("downstream")
            if not downstream or not downstream.get("fixture") or not downstream.get("next_skill"):
                findings.append(f"Skill '{skill}' requires downstream but has incomplete 'downstream' config")
                failure_modes.append("incomplete_downstream_config")
            
    if not findings:
        return ValidatorResult(
            status="pass",
            validator_name="promotion_plan",
            findings=["Promotion plan is semantically complete and coherent"]
        )
    else:
        return ValidatorResult(
            status="fail",
            validator_name="promotion_plan",
            findings=findings,
            failure_modes=failure_modes
        )
