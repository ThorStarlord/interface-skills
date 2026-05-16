import unittest
import os
import yaml
import tempfile
import json
from scripts.validators.promotion_plan import validate_promotion_plan
from scripts.validators.common import ValidatorResult

class TestPromotionPlanValidator(unittest.TestCase):
    def test_missing_skill_in_registry(self):
        """A plan with a skill not in skills.json should fail."""
        plan_data = {
            "skills": {
                "non-existent-skill": {
                    "fixtures": ["some/fixture"]
                }
            }
        }
        registry_data = {
            "skills": [
                {"name": "existing-skill"}
            ]
        }
        
        with tempfile.TemporaryDirectory() as tmpdir:
            plan_path = os.path.join(tmpdir, "promotion-plan.yaml")
            registry_path = os.path.join(tmpdir, "skills.json")
            
            with open(plan_path, "w") as f:
                yaml.dump(plan_data, f)
            with open(registry_path, "w") as f:
                json.dump(registry_data, f)
            
            result = validate_promotion_plan(plan_path, registry_path=registry_path)
            
            self.assertEqual(result.status, "fail")
            self.assertIn("non-existent-skill", result.findings[0])
            self.assertIn("missing_skill", result.failure_modes)

    def test_missing_fixture_on_disk(self):
        """A plan with missing fixture paths should fail."""
        plan_data = {
            "skills": {
                "existing-skill": {
                    "fixtures": ["missing/path/fixture"]
                }
            }
        }
        registry_data = {
            "skills": [
                {"name": "existing-skill"}
            ]
        }
        
        with tempfile.TemporaryDirectory() as tmpdir:
            plan_path = os.path.join(tmpdir, "promotion-plan.yaml")
            registry_path = os.path.join(tmpdir, "skills.json")
            
            with open(plan_path, "w") as f:
                yaml.dump(plan_data, f)
            with open(registry_path, "w") as f:
                json.dump(registry_data, f)
            
            # repo_root is tmpdir for this test
            result = validate_promotion_plan(plan_path, registry_path=registry_path, repo_root=tmpdir)
            
            self.assertEqual(result.status, "fail")
            self.assertIn("missing/path/fixture", result.findings[0])
            self.assertIn("missing_fixture", result.failure_modes)

    def test_valid_plan(self):
        """A valid plan should pass."""
        plan_data = {
            "skills": {
                "existing-skill": {
                    "fixtures": ["valid/fixture"],
                    "behavioral_criteria": {
                        "fixture_family": "inventory",
                        "minimum_behavioral_complexity": {"min_surfaces": 1},
                        "blocking_failure_modes": ["hallucination"]
                    }
                }
            }
        }
        registry_data = {
            "skills": [
                {"name": "existing-skill"}
            ]
        }
        
        with tempfile.TemporaryDirectory() as tmpdir:
            plan_path = os.path.join(tmpdir, "promotion-plan.yaml")
            registry_path = os.path.join(tmpdir, "skills.json")
            fixture_path = os.path.join(tmpdir, "valid/fixture")
            os.makedirs(os.path.dirname(fixture_path), exist_ok=True)
            os.makedirs(fixture_path, exist_ok=True) # Fixtures are dirs
            
            with open(plan_path, "w") as f:
                yaml.dump(plan_data, f)
            with open(registry_path, "w") as f:
                json.dump(registry_data, f)
            
            result = validate_promotion_plan(plan_path, registry_path=registry_path, repo_root=tmpdir)
            
            self.assertEqual(result.status, "pass")
            self.assertIn("semantically complete", result.findings[0])

    def test_missing_behavioral_criteria_fails(self):
        """A plan missing behavioral_criteria should fail."""
        plan_data = {
            "skills": {
                "existing-skill": {
                    "fixtures": ["valid/fixture"]
                }
            }
        }
        registry_data = {"skills": [{"name": "existing-skill"}]}
        
        with tempfile.TemporaryDirectory() as tmpdir:
            plan_path = os.path.join(tmpdir, "promotion-plan.yaml")
            registry_path = os.path.join(tmpdir, "skills.json")
            os.makedirs(os.path.join(tmpdir, "valid/fixture"), exist_ok=True)
            
            with open(plan_path, "w") as f: yaml.dump(plan_data, f)
            with open(registry_path, "w") as f: json.dump(registry_data, f)
            
            result = validate_promotion_plan(plan_path, registry_path=registry_path, repo_root=tmpdir)
            self.assertEqual(result.status, "fail")
            self.assertIn("missing_behavioral_criteria", result.failure_modes)

    def test_missing_blocking_failure_modes_fails(self):
        """A plan missing blocking_failure_modes should fail."""
        plan_data = {
            "skills": {
                "existing-skill": {
                    "fixtures": ["valid/fixture"],
                    "behavioral_criteria": {
                        "fixture_family": "inventory",
                        "minimum_behavioral_complexity": {"min_surfaces": 1}
                    }
                }
            }
        }
        registry_data = {"skills": [{"name": "existing-skill"}]}
        
        with tempfile.TemporaryDirectory() as tmpdir:
            plan_path = os.path.join(tmpdir, "promotion-plan.yaml")
            registry_path = os.path.join(tmpdir, "skills.json")
            os.makedirs(os.path.join(tmpdir, "valid/fixture"), exist_ok=True)
            
            with open(plan_path, "w") as f: yaml.dump(plan_data, f)
            with open(registry_path, "w") as f: json.dump(registry_data, f)
            
            result = validate_promotion_plan(plan_path, registry_path=registry_path, repo_root=tmpdir)
            self.assertEqual(result.status, "fail")
            self.assertIn("missing_blocking_failure_modes", result.failure_modes)

    def test_invalid_downstream_config_fails(self):
        """If require_downstream is true, missing downstream block should fail."""
        plan_data = {
            "skills": {
                "existing-skill": {
                    "fixtures": ["valid/fixture"],
                    "promotion_criteria": {"require_downstream": True},
                    "behavioral_criteria": {
                        "fixture_family": "inventory",
                        "minimum_behavioral_complexity": {"min_surfaces": 1},
                        "blocking_failure_modes": ["hallucination"]
                    }
                }
            }
        }
        registry_data = {"skills": [{"name": "existing-skill"}]}
        
        with tempfile.TemporaryDirectory() as tmpdir:
            plan_path = os.path.join(tmpdir, "promotion-plan.yaml")
            registry_path = os.path.join(tmpdir, "skills.json")
            os.makedirs(os.path.join(tmpdir, "valid/fixture"), exist_ok=True)
            
            with open(plan_path, "w") as f: yaml.dump(plan_data, f)
            with open(registry_path, "w") as f: json.dump(registry_data, f)
            
            result = validate_promotion_plan(plan_path, registry_path=registry_path, repo_root=tmpdir)
            self.assertEqual(result.status, "fail")
            self.assertIn("incomplete_downstream_config", result.failure_modes)

if __name__ == "__main__":
    unittest.main()
