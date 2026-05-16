## Agent Brief

**Category:** enhancement
**Summary:** Extract `human_review.py` and establish the `ValidatorResult` contract.

**Current behavior:**
Promotion scripts (`run_promotion_suite.py`) perform ad-hoc checks for human review artifacts (e.g., `HUMAN-REVIEW.md`) and print results directly to stdout or simple strings. There is no unified, machine-readable data structure for validation findings, and governance logic is mixed with orchestration.

**Desired behavior:**
Establish a core `ValidatorResult` structured Python contract (dataclass) that all future validators will follow. Extract the human review governance logic into a modular `scripts/validators/human_review.py` that returns this contract. The validator must specifically enforce that `stable_promotion_authorized` is required for stable status and that `restoration_baseline_confirmation` is insufficient for promotion.

**Key interfaces:**
- `ValidatorResult` (dataclass) — Fields: `status` (pass/fail/error), `findings` (list), `failure_modes` (list), `artifact_path`, `validator_name`, `checked_scope`.
- `validate_human_review(review_path, scope)` — The primary entrypoint for the validator.

**Acceptance criteria:**
- [ ] `ValidatorResult` is defined in a shared location (e.g., `scripts/validators/common.py`).
- [ ] `human_review.py` extracts existing logic and correctly identifies authorization scopes.
- [ ] `run_promotion_suite.py` delegates to the validator and uses the result object for reporting.
- [ ] Test fixtures confirm that a "rejected" or "pending" review fails validation.

**Out of scope:**
- Modifying the `HUMAN-REVIEW.md` markdown template.
- Implementing other validators beyond `human_review.py`.
