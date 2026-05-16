import unittest
import sys
from pathlib import Path

# Add repo root to path
REPO_ROOT = Path(__file__).parent.parent
sys.path.append(str(REPO_ROOT))

from scripts.validators.behavioral_result import validate_behavioral_result

class TestBehavioralResultValidator(unittest.TestCase):
    def test_trivial_placeholders_fail(self):
        content = "# Title\nTODO: Implement this section."
        result = validate_behavioral_result(content, "ui-brief")
        self.assertEqual(result.status, "fail")
        self.assertIn("trivial_placeholders", result.failure_modes)

    def test_traceability_pass(self):
        input_text = "Surface ID: SURF-001\nFinding ID: FIND-123"
        output_text = "Analysis for SURF-001 shows that FIND-123 is valid."
        result = validate_behavioral_result(output_text, "ui-brief", input_content=input_text)
        self.assertEqual(result.status, "pass")
        self.assertTrue(any("Propagated 2/2 IDs" in f for f in result.findings))

    def test_traceability_failure(self):
        input_text = "Surface ID: SURF-001"
        output_text = "Analysis complete." # Lost the ID
        result = validate_behavioral_result(output_text, "ui-brief", input_content=input_text)
        self.assertEqual(result.status, "fail")
        self.assertIn("traceability_loss", result.failure_modes)

    def test_hallucination_detected(self):
        input_text = "Surface ID: SURF-001"
        output_text = "Analysis for SURF-001 and SURF-999." # SURF-999 is new
        result = validate_behavioral_result(output_text, "ui-brief", input_content=input_text)
        self.assertEqual(result.status, "fail")
        self.assertIn("hallucination_detected", result.failure_modes)

    def test_complexity_threshold_ui_surface_inventory(self):
        content = "## Surface 1\n## Surface 2"
        thresholds = {"min_surface_candidates": 3}
        result = validate_behavioral_result(content, "ui-surface-inventory", thresholds=thresholds)
        self.assertEqual(result.status, "fail")
        self.assertIn("low_complexity", result.failure_modes)

    def test_generic_complexity_threshold(self):
        content = "- Finding 1\n- Finding 2"
        thresholds = {"min_findings": 3}
        result = validate_behavioral_result(content, "ui-to-issues", thresholds=thresholds)
        self.assertEqual(result.status, "fail")
        self.assertIn("low_complexity", result.failure_modes)

if __name__ == "__main__":
    unittest.main()
