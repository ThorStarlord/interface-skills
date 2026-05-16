import unittest
import sys
import os
import tempfile
import shutil
from pathlib import Path

# Add REPO_ROOT to sys.path
REPO_ROOT = Path(__file__).parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.append(str(REPO_ROOT))

from scripts.validators.workflow_link import validate_workflow_link

class TestWorkflowLinkValidator(unittest.TestCase):
    def setUp(self):
        self.tmp_dir = Path(tempfile.mkdtemp())
        # Mock run_dir structure
        self.run_dir = self.tmp_dir / "promotion-runs" / "test-run"
        self.run_dir.mkdir(parents=True)
        
        # Mock artifacts
        self.brief_path = self.tmp_dir / "specs" / "02-brief.md"
        self.brief_path.parent.mkdir(parents=True)
        self.brief_path.write_text("---\nspec_id: brief-001\n---\n# Brief", encoding="utf-8")
        
        self.blueprint_path = self.tmp_dir / "specs" / "04-blueprint.md"
        self.blueprint_path.write_text("---\nspec_id: blueprint-001\nbased_on: brief-001\n---\n# Blueprint", encoding="utf-8")

    def tearDown(self):
        shutil.rmtree(self.tmp_dir)

    def test_positive_link(self):
        """Test a valid semantic and physical link."""
        prev_step = {
            "skill": "ui-brief",
            "artifact": "specs/02-brief.md"
        }
        curr_step = {
            "skill": "ui-blueprint",
            "artifact": "specs/04-blueprint.md",
            "input_artifact": "specs/02-brief.md"
        }
        
        # We need to set REPO_ROOT for the validator to find artifacts relative to it
        # In the validator, I used Path(run_dir).parent.parent / curr_artifact_rel
        # So we should mock that structure.
        
        result = validate_workflow_link(self.run_dir, curr_step, prev_step)
        self.assertEqual(result.status, "pass")
        self.assertIn("Semantic Link found in frontmatter", result.findings[0])

    def test_missing_semantic_link(self):
        """Test failure when based_on is missing or mismatched."""
        self.blueprint_path.write_text("---\nspec_id: blueprint-001\n---\n# Blueprint", encoding="utf-8")
        
        prev_step = {
            "skill": "ui-brief",
            "artifact": "specs/02-brief.md"
        }
        curr_step = {
            "skill": "ui-blueprint",
            "artifact": "specs/04-blueprint.md",
            "input_artifact": "specs/02-brief.md"
        }
        
        result = validate_workflow_link(self.run_dir, curr_step, prev_step)
        self.assertEqual(result.status, "fail")
        self.assertIn("missing_semantic_link", result.failure_modes)

    def test_physical_link_break(self):
        """Test failure when input_artifact doesn't match previous output."""
        prev_step = {
            "skill": "ui-brief",
            "artifact": "specs/02-brief.md"
        }
        curr_step = {
            "skill": "ui-blueprint",
            "artifact": "specs/04-blueprint.md",
            "input_artifact": "specs/wrong-brief.md"
        }
        
        result = validate_workflow_link(self.run_dir, curr_step, prev_step)
        self.assertEqual(result.status, "fail")
        self.assertIn("mismatched_paths", result.failure_modes)

if __name__ == "__main__":
    unittest.main()
