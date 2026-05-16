import unittest
import os
import tempfile
from scripts.validators.fixture_integrity import validate_fixture_integrity
from scripts.validators.common import ValidatorResult

class TestFixtureIntegrityValidator(unittest.TestCase):
    def test_missing_rubric(self):
        """A fixture without a rubric.md should fail integrity check."""
        with tempfile.TemporaryDirectory() as tmpdir:
            # Create a fixture dir but no expected/rubric.md
            fixture_dir = os.path.join(tmpdir, "test-fixture")
            os.makedirs(fixture_dir)
            
            result = validate_fixture_integrity(fixture_dir)
            
            self.assertEqual(result.status, "fail")
            self.assertIn("missing expected/rubric.md", result.findings[0])
            self.assertIn("missing_rubric", result.failure_modes)

    def test_valid_fixture(self):
        """A valid fixture should pass."""
        with tempfile.TemporaryDirectory() as tmpdir:
            fixture_dir = os.path.join(tmpdir, "test-fixture")
            rubric_dir = os.path.join(fixture_dir, "expected")
            os.makedirs(rubric_dir)
            with open(os.path.join(rubric_dir, "rubric.md"), "w") as f:
                f.write("# Rubric")
            
            result = validate_fixture_integrity(fixture_dir)
            
            self.assertEqual(result.status, "pass")
            self.assertIn("integrity verified", result.findings[0])

if __name__ == "__main__":
    unittest.main()
