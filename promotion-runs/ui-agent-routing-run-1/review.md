# Skill Promotion Review: ui-agent-routing

## Overview
- **Skill:** `ui-agent-routing`
- **Target Status:** Do not promote to stable (missing test harness).
- **Run ID:** ui-agent-routing-run-1
- **Downstream Skill:** `ui-to-issues`

## Findings
The requested command `python scripts/run-promotion-suite.py --skill ui-agent-routing --fresh` could not be executed because `scripts/run-promotion-suite.py` does not exist in the repository.

- **Description:** The test harness script is missing from the `scripts/` directory, preventing automated skill execution.
- **Downstream Verification:** Cannot verify downstream behavior against `ui-to-issues` because the skill test cannot be run. In addition, downstream dependencies may also be unstable (e.g. status: draft).
- **Recommendation:** Do NOT promote the skill to stable.

## Required Actions
- The final integration task must create/restore `scripts/run-promotion-suite.py` to enable automated execution of Interface Skills.
