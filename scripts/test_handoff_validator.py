import unittest
import os
import tempfile
from scripts.validators.handoff_verification import validate_handoff
from scripts.validators.common import ValidatorResult

class TestHandoffValidator(unittest.TestCase):
    def test_missing_consumption_marker(self):
        """A handoff where the next skill ignores the input should fail."""
        next_skill_content = "# Next Skill Output\nSome other content."
        
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = os.path.join(tmpdir, "test-run")
            os.makedirs(run_dir)
            
            # The harness stores downstream results in run_dir/downstream_<skill>.md
            # Or in this case, we'll check the logic in run_promotion_suite.py
            # Actually, let's see how the harness stores it.
            # In run_promotion_suite.py: 
            #   with open(run_dir / f"downstream_{next_skill}.md", "w") as f:
            
            next_skill_file = os.path.join(run_dir, "downstream_ui-inspector.md")
            # Provide upstream artifact to trigger consumption check
            upstream_file = os.path.join(run_dir, "ui-surface-inventory-report.md")
            with open(upstream_file, "w") as f:
                f.write("# Surface Inventory")

            with open(next_skill_file, "w") as f:
                f.write(next_skill_content)
            
            result = validate_handoff(run_dir, "ui-surface-inventory", "ui-inspector", 
                                     upstream_artifact=upstream_file,
                                     downstream_artifact=next_skill_file)
            
            self.assertEqual(result.status, "fail")
            self.assertIn("Consumption Contract Violation", result.findings[0])
            self.assertIn("consumption_contract_violation", result.failure_modes)

    def test_valid_handoff(self):
        """A valid handoff should pass."""
        next_skill_content = "# Next Skill Output\n## Input Evidence\n- ui-surface-inventory-report.md\nConsumed inventory."
        
        with tempfile.TemporaryDirectory() as tmpdir:
            run_dir = os.path.join(tmpdir, "test-run")
            os.makedirs(run_dir)
            
            next_skill_file = os.path.join(run_dir, "downstream_ui-inspector.md")
            # Create a mock upstream artifact for the density/citation checks
            upstream_file = os.path.join(run_dir, "ui-surface-inventory-report.md")
            with open(upstream_file, "w") as f:
                f.write("# Surface Inventory\n- SURF-001\n- SURF-002\n- SURF-003")

            with open(next_skill_file, "w") as f:
                f.write(next_skill_content + "\n- SURF-001\n- SURF-002\n- SURF-003")
            
            result = validate_handoff(run_dir, "ui-surface-inventory", "ui-inspector", 
                                     upstream_artifact=upstream_file,
                                     downstream_artifact=next_skill_file)
            
            self.assertEqual(result.status, "pass")

if __name__ == "__main__":
    unittest.main()
