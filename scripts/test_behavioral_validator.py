import unittest
from scripts.validators.behavioral_result import validate_behavioral_result
from scripts.validators.common import ValidatorResult

class TestBehavioralValidator(unittest.TestCase):
    def test_placeholders_found(self):
        """Output with placeholders should fail."""
        content = "# Report\nThis is a TBD section."
        result = validate_behavioral_result(content, "ui-surface-inventory", {})
        
        self.assertEqual(result.status, "fail")
        self.assertIn("placeholders", result.findings[0])
        self.assertIn("trivial_placeholders", result.failure_modes)

    def test_low_complexity(self):
        """Output with low complexity should fail."""
        content = "## Surface 1\nSome content."
        thresholds = {"min_surface_candidates": 2}
        result = validate_behavioral_result(content, "ui-surface-inventory", thresholds)
        
        self.assertEqual(result.status, "fail")
        self.assertIn("Low complexity", result.findings[0])
        self.assertIn("low_complexity", result.failure_modes)

if __name__ == "__main__":
    unittest.main()
