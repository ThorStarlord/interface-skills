import unittest
import yaml
import json
import tempfile
import shutil
from pathlib import Path
import sys

# Add repo root to path
REPO_ROOT = Path(__file__).parent.parent
sys.path.append(str(REPO_ROOT))

from scripts.validators.promotion_plan import validate_promotion_plan

class TestPromotionPlanValidator(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())
        self.reg_path = self.test_dir / "skills.json"
        self.plan_path = self.test_dir / "promotion-plan.yaml"
        
        registry = {"skills": [{"name": "test-skill"}]}
        self.reg_path.write_text(json.dumps(registry))

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_invalid_fixture_family_fails(self):
        plan = {
            "skills": {
                "test-skill": {
                    "behavioral_criteria": {
                        "fixture_family": "non-existent-family",
                        "minimum_behavioral_complexity": {"m": 1},
                        "blocking_failure_modes": ["err"]
                    }
                }
            }
        }
        self.plan_path.write_text(yaml.dump(plan))
        
        result = validate_promotion_plan(self.plan_path, self.reg_path, repo_root=self.test_dir)
        self.assertEqual(result.status, "fail")
        self.assertIn("invalid_fixture_family", result.failure_modes)

    def test_workflow_boundary_violation_fails(self):
        # Workflow scope requires require_downstream: true
        plan = {
            "skills": {
                "test-skill": {
                    "promotion_criteria": {
                        "scope": "workflow",
                        "require_downstream": False
                    },
                    "behavioral_criteria": {
                        "fixture_family": "fixtures/test",
                        "minimum_behavioral_complexity": {"m": 1},
                        "blocking_failure_modes": ["err"]
                    }
                }
            }
        }
        # Create family dir
        (self.test_dir / "fixtures" / "test").mkdir(parents=True)
        
        self.plan_path.write_text(yaml.dump(plan))
        
        result = validate_promotion_plan(self.plan_path, self.reg_path, repo_root=self.test_dir)
        self.assertEqual(result.status, "fail")
        self.assertIn("boundary_violation", result.failure_modes)

    def test_valid_plan_passes(self):
        plan = {
            "skills": {
                "test-skill": {
                    "promotion_criteria": {
                        "scope": "stable"
                    },
                    "behavioral_criteria": {
                        "fixture_family": "fixtures/test",
                        "minimum_behavioral_complexity": {"m": 1},
                        "blocking_failure_modes": ["hallucination", "scope_drift"]
                    }
                }
            }
        }
        (self.test_dir / "fixtures" / "test").mkdir(parents=True)
        self.plan_path.write_text(yaml.dump(plan))
        
        result = validate_promotion_plan(self.plan_path, self.reg_path, repo_root=self.test_dir)
        self.assertEqual(result.status, "pass")

if __name__ == "__main__":
    unittest.main()
