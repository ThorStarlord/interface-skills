# Review: ui-brief on admin-nav-recovery

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

- [ ] Identifies app-shell/navigation-map as the UI Scope. (pending_manual)
- [ ] Captures route registry contradiction risk. (pending_manual)
- [ ] Mentions nested or monorepo agent documentation as relevant context. (pending_manual)
- [x] Does not reduce the scope to a single page. (keyword_match)
- [ ] Separates confirmed evidence from assumptions. (pending_manual)
