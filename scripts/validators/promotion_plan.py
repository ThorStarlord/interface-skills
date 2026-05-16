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
            
        skill_entry = next(s for s in reg_skills_list if s["name"] == skill)
        current_status = skill_entry.get("status", "experimental")
        
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
            family = beh_crit.get("fixture_family")
            if not family:
                findings.append(f"Skill '{skill}' is missing 'fixture_family' in behavioral_criteria")
                failure_modes.append("missing_fixture_family")
            else:
                # Family Validation: Support flexible layouts (ADR 0008)
                family_candidates = [
                    Path("fixtures") / family,
                    Path(family),
                    Path("examples/fixtures") / family
                ]
                if repo_root:
                    root = Path(repo_root)
                    family_candidates = [root / "fixtures" / family, root / family, root / "examples/fixtures" / family]
                
                found_family_path = next((p for p in family_candidates if p.exists() and p.is_dir()), None)
                if not found_family_path:
                    findings.append(f"Skill '{skill}' fixture_family '{family}' not found in candidates: {[str(p) for p in family_candidates]}")
                    failure_modes.append("invalid_fixture_family")
                else:
                    # Verify all fixtures belong to this family (ADR 0008 convention)
                    for fixture_rel in fixtures:
                        f_path = (Path(repo_root) / fixture_rel) if repo_root else Path(fixture_rel)
                        try:
                            f_path.relative_to(found_family_path)
                        except ValueError:
                            findings.append(f"Fixture convention violation: Fixture '{fixture_rel}' is outside its declared family '{family}'")
                            failure_modes.append("fixture_convention_violation")
            
            if not beh_crit.get("minimum_behavioral_complexity"):
                findings.append(f"Skill '{skill}' is missing 'minimum_behavioral_complexity' in behavioral_criteria")
                failure_modes.append("missing_complexity_metrics")
                
            blocking = beh_crit.get("blocking_failure_modes")
            if not blocking or not isinstance(blocking, list):
                findings.append(f"Skill '{skill}' is missing or has invalid 'blocking_failure_modes'")
                failure_modes.append("missing_blocking_failure_modes")

        # 4. Validate downstream coherence & Boundary Rules (ADR 0006/0007)
        prom_crit = skill_cfg.get("promotion_criteria", {})
        requested_scope = prom_crit.get("scope", "stable")
        
        downstream = skill_cfg.get("downstream")
        # Workflow scope OR explicit require_downstream MUST have downstream verification
        require_downstream = prom_crit.get("require_downstream", False)
        
        # ADR 0008: Stable promotion cannot bypass downstream expectations if require_downstream is True
        if require_downstream and not downstream:
            findings.append(f"Skill '{skill}' has require_downstream=True but is missing 'downstream' configuration.")
            failure_modes.append("missing_downstream_proof")

        if requested_scope == "workflow" or require_downstream:
            if requested_scope == "workflow" and not require_downstream:
                findings.append(f"Skill '{skill}' has 'workflow' scope but 'require_downstream' is false (ADR 0007 violation)")
                failure_modes.append("boundary_violation")
            
            if not downstream:
                findings.append(f"Skill '{skill}' requires downstream verification but is missing 'downstream' configuration")
                failure_modes.append("incomplete_downstream_config")
        
        if downstream:
            next_skill = downstream.get("next_skill")
            if not next_skill:
                findings.append(f"Skill '{skill}' downstream config is missing 'next_skill'")
                failure_modes.append("incomplete_downstream_config")
            elif next_skill not in reg_skills:
                findings.append(f"Skill '{skill}' downstream 'next_skill' '{next_skill}' not found in registry")
                failure_modes.append("missing_skill")
            
            ds_fixture = downstream.get("fixture")
            if not ds_fixture:
                findings.append(f"Skill '{skill}' downstream config is missing 'fixture'")
                failure_modes.append("incomplete_downstream_config")
            elif ds_fixture not in fixtures:
                findings.append(f"Skill '{skill}' downstream fixture '{ds_fixture}' is not in the skill's primary fixture list.")
                failure_modes.append("invalid_downstream_fixture")
            
            # Validate handoff_mode (Mandatory for workflow/required, optional but validated for stable)
            mode = downstream.get("handoff_mode")
            if (requested_scope == "workflow" or require_downstream) and not mode:
                findings.append(f"Skill '{skill}' requires downstream verification but 'handoff_mode' is missing")
                failure_modes.append("missing_handoff_mode")
            if mode and mode not in ["real", "simulated"]:
                findings.append(f"Skill '{skill}' has invalid 'handoff_mode' '{mode}' (Expected: 'real' or 'simulated')")
                failure_modes.append("invalid_config_value")

        # 5. Evidence Shape Requirements (ADR 0008)
        shape = skill_cfg.get("evidence_shape")
        if shape:
            required_artifacts = shape.get("required_artifacts", [])
            if not isinstance(required_artifacts, list):
                findings.append(f"Skill '{skill}' has invalid 'evidence_shape.required_artifacts' (Expected list)")
                failure_modes.append("invalid_config")
            elif (requested_scope == "workflow" or current_status == "stable") and not required_artifacts:
                findings.append(f"Skill '{skill}' target scope/status requires evidence but 'evidence_shape.required_artifacts' is empty")
                failure_modes.append("missing_required_artifacts")

            
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
