# ADR 0005: Skill Promotion Automation

## Status
Accepted
Date: 2026-05-13

## Context
The `interface-skills` repository requires rigorous testing before promoting a skill from `draft` to `stable`. Currently, this process is manual and involves running skills against multiple fixtures, validating outputs, and collecting evidence. This manual process is slow and error-prone.

We want to automate the repeatable parts of this cycle — execution, structural validation, and rubric comparison — while maintaining human judgment as the final gate.

## Decision
We will implement a **Skill Promotion Harness** consisting of:
1.  **Promotion Plan (`promotion-plan.yaml`)**: A central configuration file defining the test matrix for every skill.
2.  **Runner Script (`scripts/run-promotion-suite.py`)**: An automated script that orchestrates the execution of skills against fixtures in isolated environments.
3.  **Result Artifacts (`promotion-runs/`)**: Immutable records of every test run, including structural validation results and rubric matches.
4.  **Improvement Briefs**: Automated failure analysis and suggested skill edits.

### Rules of Automation
- **Structural Validation is Mandatory**: Every run must pass `validate-skill.py` and `validate-spec-package.py`.
- **Rubrics are Source of Truth**: Success is measured against machine-readable or semi-structured rubrics in fixture directories.
- **No Silent Promotion**: The harness may mark a skill as `promotion_candidate`, but only a human may change the status to `stable`.
- **Immutability**: Previous run results must never be overwritten. They serve as audit evidence for promotion.
- **Safety Gates**: Automation is forbidden from rewriting promotion criteria or validator rules.

## Consequences
- **Faster Iteration**: Skills can be tested against the full suite of fixtures with a single command.
- **Consistent Evidence**: Every promoted skill will have a standardized trail of evidence.
- **Reduced Human Drudgery**: Humans focus on evaluating the *quality* of the judgment, not the *structure* of the files.
- **Risk of Overfitting**: Automated improvement proposals might overfit a skill to specific fixtures. Human review remains critical to ensure generalizability.
