import unittest
import os
import tempfile
import json
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
            os.makedirs(ref_dir)
            
            record = {
                "artifacts": {
                    "art.md": {"source_run": "2026-05-15-run-001"}
                },
                "approval_metadata": {
                    "authorizing_run_id": "2026-05-15-run-001"
                }
            }
            with open(os.path.join(ref_dir, "reference_record.json"), "w") as f:
                f.write(json.dumps(record))
            with open(os.path.join(ref_dir, "art.md"), "w") as f:
                f.write("content")
                
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
            with open(os.path.join(ref_dir, "HUMAN-REVIEW.md"), "w") as f:
                f.write(content)
            
            result = validate_reference_evidence("ui-surface-inventory", ref_dir)
            
            self.assertEqual(result.status, "pass")

if __name__ == "__main__":
    unittest.main()
