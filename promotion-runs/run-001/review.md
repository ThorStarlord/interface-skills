# Improvement Brief

## Diagnosis
The command `python scripts/run-promotion-suite.py --skill ui-flow --fresh` failed because the script `scripts/run-promotion-suite.py` does not exist in the codebase.
This is a **global/infrastructure failure**, not specific to the `ui-flow` skill, its fixtures, or its rubric.

## Downstream Contract Verification
Cannot verify the expected downstream contract behavior against `ui-blueprint` because the test runner is missing. Therefore, the downstream check is classified as `needs_human_review` as per instructions.

## Recommendation
- The global registry and catalogs were not updated.
- The missing `scripts/run-promotion-suite.py` test harness needs to be created or restored by the integration/coordinator task.
- Once the script is available, the promotion suite should be re-run for `ui-flow` to produce actual evidence.
# Promotion Review: ui-system

## Run Context
- Skill: `ui-system`
- Risk Rating: Medium (judgment-heavy)
- Downstream Skill: `ui-screen-spec` (draft status)

## Results Summary
- Command execution: FAILED (`python scripts/run-promotion-suite.py --skill ui-system --fresh` returned "No such file or directory")
- Downstream Verification: `needs_human_review` (Downstream skill `ui-screen-spec` is not stable)
- Recommendation: **Do not promote to stable.**

## Failure Diagnosis & Improvement Brief
The `run-promotion-suite.py` script specified in the commands is missing from the `scripts/` directory.
The skill cannot be fully automatically verified until the testing infrastructure is restored.

**Action Required (Integration Team):**
- Restore or implement `scripts/run-promotion-suite.py` to support automated testing of interface skills.
- The downstream skill `ui-screen-spec` must also be stabilized before `ui-system` can be safely promoted without human review.
