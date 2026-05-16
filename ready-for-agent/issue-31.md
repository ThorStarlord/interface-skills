## Agent Brief

**Category:** enhancement
**Summary:** Extract `promotion_plan.py` as the Configuration Authority.

**Current behavior:**
The Promotion Harness (`run_promotion_suite.py`) reads `promotion-plan.yaml` but performs minimal validation of the plan's integrity before execution. Missing skills, invalid fixture paths, or inconsistent handoff configurations are often caught mid-run, leading to "junk" evidence or untraceable failures.

**Desired behavior:**
Implement `scripts/validators/promotion_plan.py` to act as a pre-flight "Configuration Authority." It must ensure the promotion contract is structurally valid and semantically coherent (e.g., skill exists, fixtures exist, handoff mode is defined) before the harness begins generating behavioral evidence.

**Key interfaces:**
- `ValidatorResult` — Use the standard contract established in Issue #30.
- `validate_promotion_plan(plan_path)` — Entrypoint for the validator.

**Acceptance criteria:**
- [ ] Validates that all skills cited in the plan exist in the master `skills.json`.
- [ ] Validates that all required fixture paths for each skill exist on disk.
- [ ] Validates that the handoff mode (simulated/real) is explicitly defined where required.
- [ ] The Promotion Harness invokes this as a mandatory first step and halts on failure.

**Out of scope:**
- Modifying the YAML schema of `promotion-plan.yaml`.
- Judging whether the promotion criteria in the plan are "good enough" (governance policy).
