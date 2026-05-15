# Improvement Brief: Missing Promotion Suite Script

## Issue
The promotion workflow instructs the isolated worker task to run the command:
`python scripts/run-promotion-suite.py --skill ui-blueprint --fresh`

However, the file `scripts/run-promotion-suite.py` does not exist in the repository.

## Impact
Isolated worker tasks cannot run the automated test suite for skill promotion, forcing manual evaluation of fixtures and downstream contracts against the skill definition. This increases the risk of human error and slows down the promotion process.

## Recommendation
Implement the `scripts/run-promotion-suite.py` script. The script should:
1. Accept the `--skill` and `--fresh` arguments.
2. Load the target skill's `SKILL.md` file.
3. Automatically evaluate isolated fixtures in `examples/promotion/<skill>/` against the acceptance criteria defined in the skill.
4. Output the results (pass/fail/needs_human_review) and generate the `review.md` and `result.json` automatically.
