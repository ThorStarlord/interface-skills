# UI Spec Lint Report: failing-spec-package

## Summary
- Status: FAILED
- **Total Issues:** 5

## Issues

### 1. Missing Non-goals [High]
- **File:** `brief.md`
- **Defect:** Section 8 (Non-goals) is present but empty.
- **Fix:** List at least one explicit non-goal.

### 2. Missing Tokens [High]
- **File:** `system.md`
- **Defect:** No `space.*` tokens defined.
- **Fix:** Add spacing tokens according to the token schema.

### 3. Missing Loading State [Medium]
- **File:** `component-specs/01-main.md`
- **Defect:** Component defines interactions but no loading state.
- **Fix:** Add `state.loading` definition.

### 4. Vague Language [Medium]
- **File:** `brief.md`
- **Defect:** Used banned words: "clean", "modern", "intuitive".
- **Fix:** Use concrete visual vocabulary.

### 5. Uncovered Success Criterion [Medium]
- **File:** `acceptance.md`
- **Defect:** Success criterion "User completes action" is not covered by any flow step.
- **Fix:** Add a flow step to `blueprint.md` or `ui-flow.md` that maps to this criterion.
