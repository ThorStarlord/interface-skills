---
spec_type: index
spec_id: failing-package
created: 2026-05-08
status: draft
intentionally_incomplete: true
---

# Spec Package Index: Failing Package (ui-spec-linter Test Fixture)

> **This package is intentionally broken.** It exists as a test fixture for `ui-spec-linter`. Every file in this package contains deliberate defects — vague language, missing sections, untraced criteria, and incomplete tokens. Do not use this as a template.

---

## Files

| # | File | Skill | Status | Notes |
|---|---|---|---|---|
| 1 | `brief.md` | `ui-brief` | approved | Missing §8 Non-goals; §10 Assumptions is empty |
| 2 | `blueprint.md` | `ui-blueprint` | approved | Contains banned vague terms |
| 3 | `system.md` | `ui-system` | approved | Missing `space.*` token category |
| 4 | `component-specs/post-button.md` | `ui-component-spec` | approved | Missing `loading` and `focus-visible` states |
| 5 | `acceptance.md` | `ui-acceptance` | approved | Criteria not traceable to brief §6 success criteria |

---

## Known Defects (by file)

These defects are intentional and should all be caught by `ui-spec-linter`:

| ID | File | Defect | Expected severity |
|---|---|---|---|
| FD-01 | `brief.md` | §8 Non-goals section is absent | Blocker |
| FD-02 | `brief.md` | §10 Assumptions is present but empty | Warning |
| FD-03 | `blueprint.md` | Contains "clean layout" (vague) | Warning |
| FD-04 | `blueprint.md` | Contains "modern feel" (vague) | Warning |
| FD-05 | `system.md` | No `space.*` tokens defined | Blocker |
| FD-06 | `component-specs/post-button.md` | `loading` state not defined (async button) | Blocker |
| FD-07 | `component-specs/post-button.md` | `focus-visible` state not defined | Major |
| FD-08 | `acceptance.md` | AC-01 references a metric not in brief §6 | Warning |
| FD-09 | `acceptance.md` | No criteria for error state from brief §7 constraint | Blocker |
