import unittest
import os
import tempfile
import shutil
from pathlib import Path
from scripts.validators.handoff_verification import validate_handoff

class TestADRBoundaries(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = Path(tempfile.mkdtemp())
        self.run_dir = self.tmp_dir / "test-run"
        self.run_dir.mkdir()
        self.next_skill_file = self.run_dir / "downstream_ui-inspector.md"

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_adr_0006_individual_stable_allows_simulated(self):
        """
        ADR 0006: Individual Stable Promotion allows simulated handoff.
        The validator should PASS with 'stable' scope even if only simulated handoff is detected.
        """
        # Simulated handoff: has the marker but no artifact keywords
        content = "# Output\n## Input Evidence\nAcknowledged input."
        self.next_skill_file.write_text(content)
        
        result = validate_handoff(self.run_dir, "ui-surface-inventory", "ui-inspector", requested_scope="stable", downstream_artifact=self.next_skill_file)
        
        self.assertEqual(result.status, "pass")
        self.assertTrue(any("simulated" in f.lower() for f in result.findings))
        self.assertNotIn("real_handoff_required", result.failure_modes)

    def test_adr_0007_workflow_requires_real_handoff(self):
        """
        ADR 0007: Workflow Promotion REQUIRES real handoff.
        The validator should FAIL with 'workflow' scope if only simulated handoff is detected.
        """
        # Simulated handoff
        content = "# Output\n## Input Evidence\nAcknowledged input."
        self.next_skill_file.write_text(content)
        
        result = validate_handoff(self.run_dir, "ui-surface-inventory", "ui-inspector", requested_scope="workflow", downstream_artifact=self.next_skill_file)
        
        self.assertEqual(result.status, "fail")
        self.assertIn("real_handoff_required", result.failure_modes)
        self.assertTrue(any("expected 'real' handoff" in f.lower() for f in result.findings))

    def test_adr_0007_workflow_passes_with_real_handoff(self):
        """
        Workflow Promotion should PASS if real handoff is detected.
        """
        upstream_file = self.run_dir / "ui-surface-inventory-report.md"
        upstream_file.write_text("# Surface Inventory")
        
        # Real handoff: has artifact keywords
        content = "# Output\n## Input Evidence\nConsumed inventory report from ui-surface-inventory-report.md"
        self.next_skill_file.write_text(content)
        
        result = validate_handoff(self.run_dir, "ui-surface-inventory", "ui-inspector", 
                                 requested_scope="workflow", 
                                 upstream_artifact=upstream_file,
                                 downstream_artifact=self.next_skill_file)
        
        self.assertEqual(result.status, "pass")
        self.assertTrue(any("exact citation" in f.lower() for f in result.findings))

if __name__ == "__main__":
    unittest.main()
