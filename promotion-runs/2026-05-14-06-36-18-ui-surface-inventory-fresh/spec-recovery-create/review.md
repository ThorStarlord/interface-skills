# Review: ui-surface-inventory on spec-recovery-create

- **Classification:** `fail`
- **Message:** Clean fixture failed unexpectedly
- **Evidence Level:** `promotion_candidate_run`
- **Skill Valid:** ✅
- **Package Valid:** ✅
- **Rubric Pass:** False

## Human Review Checklist

- [ ] The clean fixtures are not incorrectly classified as failures.
- [ ] The messy fixture is correctly classified as `expected_fail`.
- [ ] The lint report catches the expected defects.
- [ ] The lint report does not invent major false positives.
- [ ] The severity levels are useful.
- [ ] The output format remained stable.
- [ ] A downstream skill can consume the output.
- [ ] The reviewer agrees the output is useful and not misleading.

Decision: approved | rejected | needs_revision
Reviewer:
Review date:

## Rubric Details

- [ ] Correctly identifies App Shell, Journey, Route, and Sub-surface layers. (pending_manual)
- [ ] Prioritizes `/create` as primary recovery target. (pending_manual)
- [ ] Identifies the primary create flow. (pending_manual)
- [ ] Identifies form/input surfaces. (pending_manual)
- [ ] Identifies preview or generated-output surfaces if present. (pending_manual)
- [ ] Identifies loading, empty, and error states where evidence supports them. (pending_manual)
- [ ] Separates confirmed surfaces from inferred/recommended surfaces. (pending_manual)
