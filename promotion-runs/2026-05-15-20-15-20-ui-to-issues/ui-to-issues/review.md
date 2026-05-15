# Review: ui-to-issues on ui-to-issues

- **Classification:** `needs_human_review`
- **Message:** No rubric found for evaluation
- **Evidence Level:** `harness_validation`
- **Skill Valid:** ✅
- **Package Valid:** ✅
- **Rubric Pass:** N/A

> [!IMPORTANT]
> **Human Review Required:** This result needs manual verification to confirm the skill's judgment matches reality.

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

## Behavioral Scrutiny

Verify that none of the following blocking failure modes occurred:

- [ ] hallucination
- [ ] scope_drift
- [ ] label_friction
- [ ] incomplete_context
- [ ] handoff_failure
- [ ] evidence_gap

## Judgment Fidelity Assessment

- [ ] Judgment matches ground truth exactly.
- [ ] Ambiguous boundaries handled with correct trade-offs.
- [ ] No hallucination of artifacts or attributes.
- [ ] Scope correctly bounded to the fixture domain.

## Rubric Details

No rubric items found.
