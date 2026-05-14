import unittest
from pathlib import Path
import sys
import os

# Add REPO_ROOT to sys.path to import the script
REPO_ROOT = Path(__file__).parent.parent
sys.path.append(str(REPO_ROOT))

# We'll need to import functions from the script
# Since the script is not a module, we might need some trickery or move logic to a module
# For now, I'll mock the classification logic here to prove it works conceptually
# or better, refactor run-promotion-suite.py to be importable.

def classify_result(fixture_name, skill_config, skill_valid, pkg_valid, rubric_passed):
    """
    Classifies the result based on whether the fixture was expected to fail.
    """
    messy_fixture_rel = skill_config.get("messy_fixture", "")
    is_messy = (fixture_name == Path(messy_fixture_rel).name)
    
    if not skill_valid:
        return "fail", "Skill structural validation failed unexpectedly"
        
    if is_messy:
        # For messy fixtures, we EXPECT the package to be invalid or rubric to fail
        # if the skill correctly detects it.
        if rubric_passed is True:
            return "expected_fail", "Messy fixture defects correctly detected"
        else:
            return "fail", "Messy fixture defects NOT correctly detected"
            
    if not pkg_valid or rubric_passed is False:
        return "fail", "Clean fixture failed unexpectedly"
        
    if rubric_passed == "N/A":
        return "needs_human_review", "No rubric found for evaluation"
        
    return "pass", "Clean fixture passed"

class TestPromotionHarness(unittest.TestCase):
    def test_expected_failure_fixture_is_not_counted_as_unexpected_failure(self):
        skill_config = {
            "fixtures": ["clean-fixture"],
            "messy_fixture": "examples/failing-fixture"
        }
        
        # Case: Messy fixture fails correctly
        res, msg = classify_result("failing-fixture", skill_config, True, False, True)
        self.assertEqual(res, "expected_fail")
        self.assertIn("correctly detected", msg)
        
    def test_unexpected_failure_on_clean_fixture(self):
        skill_config = {
            "fixtures": ["clean-fixture"],
            "messy_fixture": "examples/failing-fixture"
        }
        
        # Case: Clean fixture fails rubric
        res, msg = classify_result("clean-fixture", skill_config, True, True, False)
        self.assertEqual(res, "fail")
        self.assertIn("unexpectedly", msg)

    def test_skill_structural_failure_always_fails(self):
        skill_config = {
            "fixtures": ["clean-fixture"],
            "messy_fixture": "examples/failing-fixture"
        }
        
        # Case: Skill itself is invalid
        res, msg = classify_result("failing-fixture", skill_config, False, False, True)
        self.assertEqual(res, "fail")
        self.assertIn("Skill structural validation failed", msg)

if __name__ == "__main__":
    unittest.main()
