# ui-visual-calibration Promotion Run Report

## Goal
Evaluate the `ui-visual-calibration` (or `is-ui-visual-calibration`) skill against the promotion rules outlined in its SKILL.md.

## Diagnostic Note
The requested command `python scripts/run-promotion-suite.py --skill ui-visual-calibration --fresh` could not be executed because `scripts/run-promotion-suite.py` does not exist in the repository.

However, based on the `parallel-task-plan.md` and the prompt instructions, we are to simulate/execute the test, diagnose the failure, and produce evidence.

## Results against completion criteria

1. We copied the minimal required references from `docs/is-ui-examples/settings-page` into `examples/promotion/ui-visual-calibration/` and created the `SOURCE.md` file.

2. Since the test script is missing, the command fails.

### Improvement brief

- **Failure Type:** skill-specific
- **Description:** The `run-promotion-suite.py` script is missing from the `scripts/` directory, preventing the skill from being executed.
- **Recommendation:** The final integration task needs to either provide this script, update the `parallel-task-plan.md` instructions to not rely on it, or map the validation to an existing script (like a new validation script). For now, the skill cannot be tested programmatically via the `run-promotion-suite.py` script as instructed.

## Classification

**Result:** `needs_human_review` (due to missing harness script).

## Downstream contract behavior

Without the output of the calibration, the downstream skill `ui-flow` is blocked.
Since we cannot verify the downstream contract, this check is classified as `needs_human_review`.
