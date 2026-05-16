import unittest
import os
import tempfile
from scripts.validators.reference_evidence import validate_reference_evidence
from scripts.validators.common import ValidatorResult

class TestReferenceValidator(unittest.TestCase):
    def test_missing_reference_dir(self):
        """A missing reference directory should fail."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ref_dir = os.path.join(tmpdir, "non-existent")
            result = validate_reference_evidence("ui-surface-inventory", ref_dir)
            
            self.assertEqual(result.status, "fail")
            self.assertIn("not found", result.findings[0])
            self.assertIn("missing_reference_dir", result.failure_modes)

    def test_valid_reference(self):
        """A valid reference directory should pass."""
        with tempfile.TemporaryDirectory() as tmpdir:
            ref_dir = os.path.join(tmpdir, "reference")
            rubric_dir = os.path.join(ref_dir, "expected")
            os.makedirs(rubric_dir)
            with open(os.path.join(rubric_dir, "rubric.md"), "w") as f:
                f.write("# Rubric")
            
            result = validate_reference_evidence("ui-surface-inventory", ref_dir)
            
            self.assertEqual(result.status, "pass")
            self.assertIn("verified", result.findings[0])

if __name__ == "__main__":
    unittest.main()
