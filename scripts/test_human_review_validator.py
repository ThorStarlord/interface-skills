import unittest
import os
import tempfile
import sys
from pathlib import Path

# Add repo root to path
REPO_ROOT = Path(__file__).parent.parent
sys.path.append(str(REPO_ROOT))

from scripts.validators.human_review import validate_human_review
from scripts.validators.common import ValidatorResult

class TestHumanReviewValidator(unittest.TestCase):
    def test_valid_stable_promotion_authorized(self):
        """A human review with approved status, stable scope, sections, and Run ID should pass."""
        content = """# Human Review
        
**Decision:** approved
**Scope:** stable_promotion_authorized
**Reviewer:** Dimmi Andreus
**Date:** 2026-05-15
**Run ID:** 2026-05-15-1234-run

### Behavioral Review
Checklist passed.

### Continuity Review
Checklist passed.

The skill is ready for stable promotion.
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            review_path = os.path.join(tmpdir, "HUMAN-REVIEW.md")
            with open(review_path, "w") as f:
                f.write(content)
            
            result = validate_human_review(review_path, requested_scope="stable")
            
            self.assertEqual(result.status, "pass")
            self.assertEqual(result.validator_name, "human_review")
            self.assertTrue(any("authorized" in f for f in result.findings))

    def test_missing_mandatory_sections_fails(self):
        """A review missing Behavioral or Continuity sections should fail."""
        content = """# Human Review
**Decision:** approved
**Scope:** stable_promotion_authorized
**Reviewer:** Dimmi Andreus
**Date:** 2026-05-15
**Run ID:** 2026-05-15-run

### Some other section
Content.
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            review_path = os.path.join(tmpdir, "HUMAN-REVIEW.md")
            with open(review_path, "w") as f:
                f.write(content)
            
            result = validate_human_review(review_path, requested_scope="stable")
            
            self.assertEqual(result.status, "fail")
            self.assertIn("incomplete_template", result.failure_modes)

    def test_missing_traceability_fails(self):
        """A review missing Run ID should fail."""
        content = """# Human Review
**Decision:** approved
**Scope:** stable_promotion_authorized
**Reviewer:** Dimmi Andreus
**Date:** 2026-05-15

### Behavioral Review
Pass.

### Continuity Review
Pass.
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            review_path = os.path.join(tmpdir, "HUMAN-REVIEW.md")
            with open(review_path, "w") as f:
                f.write(content)
            
            result = validate_human_review(review_path, requested_scope="stable")
            
            self.assertEqual(result.status, "fail")
            self.assertIn("missing_traceability", result.failure_modes)

    def test_invalid_scope_restoration(self):
        """A restoration confirmation is NOT enough for stable promotion."""
        content = """# Human Review
**Decision:** approved
**Scope:** restoration_baseline_confirmation
**Reviewer:** Dimmi Andreus
**Date:** 2026-05-15
**Run ID:** 2026-05-15-run

### Behavioral Review
### Continuity Review
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            review_path = os.path.join(tmpdir, "HUMAN-REVIEW.md")
            with open(review_path, "w") as f:
                f.write(content)
            
            result = validate_human_review(review_path, requested_scope="stable")
            
            self.assertEqual(result.status, "fail")
            self.assertIn("scope_mismatch", result.failure_modes)

if __name__ == "__main__":
    unittest.main()
