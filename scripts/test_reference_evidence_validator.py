import unittest
import tempfile
import shutil
from pathlib import Path
import sys
import json

# Add repo root to path
REPO_ROOT = Path(__file__).parent.parent
sys.path.append(str(REPO_ROOT))

from scripts.validators.reference_evidence import validate_reference_evidence

class TestReferenceEvidenceValidator(unittest.TestCase):
    def setUp(self):
        self.test_dir = Path(tempfile.mkdtemp())

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_missing_record_fails(self):
        ref_dir = self.test_dir / "my-ref"
        ref_dir.mkdir()
        
        result = validate_reference_evidence("test-skill", ref_dir)
        self.assertEqual(result.status, "fail")
        self.assertIn("missing_reference_record", result.failure_modes)

    def test_incomplete_artifacts_fails(self):
        ref_dir = self.test_dir / "incomplete-ref"
        ref_dir.mkdir()
        record = {
            "missing-art.md": {"source_run": "run-001"}
        }
        (ref_dir / "reference_record.json").write_text(json.dumps(record))
        (ref_dir / "HUMAN-REVIEW.md").write_text("# Review")
        
        result = validate_reference_evidence("test-skill", ref_dir)
        self.assertEqual(result.status, "fail")
        self.assertIn("incomplete_reference", result.failure_modes)

    def test_missing_human_review_fails(self):
        ref_dir = self.test_dir / "no-review-ref"
        ref_dir.mkdir()
        record = {
            "art.md": {"source_run": "run-001"}
        }
        (ref_dir / "reference_record.json").write_text(json.dumps(record))
        (ref_dir / "art.md").write_text("content")
        
        result = validate_reference_evidence("test-skill", ref_dir)
        self.assertEqual(result.status, "fail")
        self.assertIn("missing_governance_evidence", result.failure_modes)

    def test_dirty_directory_fails(self):
        ref_dir = self.test_dir / "dirty-ref"
        ref_dir.mkdir()
        record = {}
        (ref_dir / "reference_record.json").write_text(json.dumps(record))
        (ref_dir / "HUMAN-REVIEW.md").write_text("# Review")
        (ref_dir / "junk.exe").write_text("junk")
        
        result = validate_reference_evidence("test-skill", ref_dir)
        self.assertEqual(result.status, "fail")
        self.assertIn("dirty_reference", result.failure_modes)

    def test_valid_reference_passes(self):
        ref_dir = self.test_dir / "good-ref"
        ref_dir.mkdir()
        record = {
            "artifacts": {
                "art.md": {"source_run": "2026-05-15-run-001"}
            },
            "approval_metadata": {
                "authorizing_run_id": "2026-05-15-run-001"
            }
        }
        (ref_dir / "reference_record.json").write_text(json.dumps(record))
        (ref_dir / "art.md").write_text("content")
        
        content = """# Human Review
**Decision:** approved
**Scope:** stable_promotion_authorized
**Reviewer:** Dimmi Andreus
**Date:** 2026-05-15
**Run ID:** 2026-05-15-run-001

### Behavioral Review
Pass.

### Continuity Review
Pass.
"""
        (ref_dir / "HUMAN-REVIEW.md").write_text(content)
        
        result = validate_reference_evidence("test-skill", ref_dir)
        self.assertEqual(result.status, "pass")
        self.assertTrue(any("Artifact 'art.md' verified" in f for f in result.findings))

if __name__ == "__main__":
    unittest.main()
