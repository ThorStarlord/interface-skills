## Agent Brief

**Category:** enhancement
**Summary:** Extract `behavioral_result.py` for artifact shape validation.

**Current behavior:**
Behavioral results are collected by the Promotion Harness and recorded in `result.json`. However, there is no modular validation of the **shape** of this evidence (completeness, traceability, bounding) independent of the human reviewer's judgment.

**Desired behavior:**
Implement `scripts/validators/behavioral_result.py` to ensure that produced behavioral artifacts are well-formed and match the expected skill contract shape. It verifies that the evidence is "traceable and bounded" so that the human reviewer can perform their job without encountering technical formatting defects.

**Key interfaces:**
- `ValidatorResult` — Use the standard contract.
- `validate_behavioral_result(result_path, skill_name)` — Entrypoint.

**Acceptance criteria:**
- [ ] Validates that all expected artifacts for a given skill run were produced.
- [ ] Validates that the `classification` (pass/fail/etc.) is present and follows the taxonomy in `CONTEXT.md`.
- [ ] Verifies that evidence excerpts in the result trace correctly to the source fixture artifacts.

**Out of scope:**
- Judging the "correctness" of the skill's logic (this is Human Review).
- Modifying the `result.json` master schema.
