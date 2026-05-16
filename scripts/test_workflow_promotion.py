import unittest
import sys
from pathlib import Path
import json
import yaml

# Add scripts to path
REPO_ROOT = Path(__file__).parent.parent
sys.path.append(str(REPO_ROOT / "scripts"))

import run_promotion_suite

class TestWorkflowPromotion(unittest.TestCase):
    def setUp(self):
        self.registry_path = REPO_ROOT / "skills" / "workflow-orchestrator" / "references" / "workflow-registry.yaml"
        with open(self.registry_path, "r", encoding="utf-8") as f:
            self.registry = yaml.safe_load(f)
        
        with open(REPO_ROOT / "promotion-plan.yaml", "r", encoding="utf-8") as f:
            self.plan = yaml.safe_load(f)

    def test_registry_resolution(self):
        """Verify that the harness can resolve workflows from the registry."""
        workflow_id = "spec-recovery"
        workflow = next((w for w in self.registry.get("workflows", []) if w["id"] == workflow_id), None)
        self.assertIsNotNone(workflow)
        self.assertEqual(workflow["display_name"], "Spec Recovery")

    def test_positive_workflow_run(self):
        """Verify that a valid workflow run returns success."""
        # Note: We use dry_run=True to avoid creating directories, 
        # but the logic should still pass if artifacts exist.
        success = run_promotion_suite.run_promotion_for_workflow(
            "spec-recovery", 
            self.plan, 
            self.registry_path, 
            dry_run=True
        )
        self.assertTrue(success)

    def test_negative_workflow_run_missing_artifacts(self):
        """Verify that a workflow with missing artifacts returns failure."""
        success = run_promotion_suite.run_promotion_for_workflow(
            "spec-recovery-negative-missing-handoff", 
            self.plan, 
            self.registry_path, 
            dry_run=True
        )
        self.assertFalse(success)

if __name__ == "__main__":
    unittest.main()
