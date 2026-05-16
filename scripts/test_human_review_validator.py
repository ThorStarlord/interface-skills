import unittest
import os
import tempfile
from scripts.validators.human_review import validate_human_review
from scripts.validators.common import ValidatorResult

class TestHumanReviewValidator(unittest.TestCase):
    def test_valid_stable_promotion_authorized(self):
        """A human review with approved status and stable scope should pass."""
        content = """# Human Review
        
**Status:** approved
**Scope:** stable_promotion_authorized
**Reviewer:** Dimmi Andreus
**Date:** 2026-05-15

The skill is ready for stable promotion.
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            review_path = os.path.join(tmpdir, "HUMAN-REVIEW.md")
            with open(review_path, "w") as f:
                f.write(content)
            
            result = validate_human_review(review_path, requested_scope="stable")
            
            self.assertEqual(result.status, "pass")
            self.assertEqual(result.validator_name, "human_review")
            self.assertIn("authorized", result.findings[0])

    def test_invalid_scope_restoration(self):
        """A restoration confirmation is NOT enough for stable promotion."""
        content = """# Human Review
        
**Status:** approved
**Scope:** restoration_baseline_confirmation
**Reviewer:** Dimmi Andreus
**Date:** 2026-05-15
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            review_path = os.path.join(tmpdir, "HUMAN-REVIEW.md")
            with open(review_path, "w") as f:
                f.write(content)
            
            result = validate_human_review(review_path, requested_scope="stable")
            
            self.assertEqual(result.status, "fail")
            self.assertIn("scope_mismatch", result.failure_modes)

    def test_status_not_approved(self):
        """A pending review should fail."""
        content = """# Human Review
        
**Status:** pending
**Scope:** stable_promotion_authorized
**Reviewer:** Dimmi Andreus
**Date:** 2026-05-15
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            review_path = os.path.join(tmpdir, "HUMAN-REVIEW.md")
            with open(review_path, "w") as f:
                f.write(content)
            
            result = validate_human_review(review_path, requested_scope="stable")
            
            self.assertEqual(result.status, "fail")
            self.assertIn("review_not_approved", result.failure_modes)

    def test_missing_reviewer_fails(self):
        """A review missing the reviewer field should fail."""
        content = """# Human Review
**Status:** approved
**Decision:** APPROVED FOR STABLE PROMOTION
**Scope:** stable_promotion_authorized
**Date:** 2026-05-15
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            review_path = os.path.join(tmpdir, "HUMAN-REVIEW.md")
            with open(review_path, "w") as f:
                f.write(content)
            
            result = validate_human_review(review_path, requested_scope="stable")
            
            self.assertEqual(result.status, "fail")
            self.assertIn("missing_reviewer", result.failure_modes)

    def test_missing_date_fails(self):
        """A review missing the date field should fail."""
        content = """# Human Review
**Status:** approved
**Decision:** APPROVED FOR STABLE PROMOTION
**Scope:** stable_promotion_authorized
**Reviewer:** Dimmi Andreus
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            review_path = os.path.join(tmpdir, "HUMAN-REVIEW.md")
            with open(review_path, "w") as f:
                f.write(content)
            
            result = validate_human_review(review_path, requested_scope="stable")
            
            self.assertEqual(result.status, "fail")
            self.assertIn("missing_date", result.failure_modes)

    def test_explicit_rejection_fails(self):
        """An explicit rejection in the decision field should fail even if status is approved."""
        content = """# Human Review
**Status:** approved
**Decision:** REJECTED
**Scope:** stable_promotion_authorized
**Reviewer:** Dimmi Andreus
**Date:** 2026-05-15
"""
        with tempfile.TemporaryDirectory() as tmpdir:
            review_path = os.path.join(tmpdir, "HUMAN-REVIEW.md")
            with open(review_path, "w") as f:
                f.write(content)
            
            result = validate_human_review(review_path, requested_scope="stable")
            
            self.assertEqual(result.status, "fail")
            self.assertIn("review_not_approved", result.failure_modes)

if __name__ == "__main__":
    unittest.main()
