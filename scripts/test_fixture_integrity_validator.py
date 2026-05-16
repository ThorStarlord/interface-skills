import unittest
import tempfile
import shutil
from pathlib import Path
import sys
import os

# Add repo root to path
REPO_ROOT = Path(__file__).parent.parent
sys.path.append(str(REPO_ROOT))

from scripts.validators.fixture_integrity import validate_fixture_integrity

class TestFixtureIntegrityValidator(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_missing_directory_fails(self):
        result = validate_fixture_integrity(self.test_dir / "nonexistent")
        self.assertEqual(result.status, "fail")
        self.assertIn("missing_fixture", result.failure_modes)

    def test_missing_rubric_fails(self):
        # Create empty dir
        fixture = self.test_dir / "my-fixture"
        fixture.mkdir()
        (fixture / "input.md").write_text("# Input\nSome substantial content here to pass triviality.")
        
        result = validate_fixture_integrity(fixture)
        self.assertEqual(result.status, "fail")
        self.assertIn("missing_rubric", result.failure_modes)

    def test_trivial_content_fails(self):
        fixture = self.test_dir / "thin-fixture"
        fixture.mkdir()
        (fixture / "expected").mkdir()
        (fixture / "expected" / "rubric.md").write_text("# Rubric")
        (fixture / "input.md").write_text("too thin")
        
        result = validate_fixture_integrity(fixture)
        self.assertEqual(result.status, "fail")
        self.assertIn("trivial_content", result.failure_modes)

    def test_no_content_files_fails(self):
        fixture = self.test_dir / "no-files"
        fixture.mkdir()
        (fixture / "expected").mkdir()
        (fixture / "expected" / "rubric.md").write_text("# Rubric")
        
        result = validate_fixture_integrity(fixture)
        self.assertEqual(result.status, "fail")
        self.assertIn("trivial_fixture", result.failure_modes)

    def test_valid_fixture_passes(self):
        fixture = self.test_dir / "good-fixture"
        fixture.mkdir()
        (fixture / "expected").mkdir()
        (fixture / "expected" / "rubric.md").write_text("# Rubric")
        (fixture / "input.md").write_text("# Substantial Content\n" + "A" * 600)
        
        result = validate_fixture_integrity(fixture)
        self.assertEqual(result.status, "pass")
        self.assertIn("Fixture depth verified", result.findings[1])

    def test_adversarial_tagging(self):
        fixture = self.test_dir / "messy-fixture"
        fixture.mkdir()
        (fixture / "expected").mkdir()
        (fixture / "expected" / "rubric.md").write_text("# Rubric")
        (fixture / "input.md").write_text("# Messy Content\n" + "B" * 600)
        
        result = validate_fixture_integrity(fixture)
        self.assertEqual(result.status, "pass")
        self.assertTrue(any("Adversarial intent" in f for f in result.findings))

if __name__ == "__main__":
    unittest.main()
