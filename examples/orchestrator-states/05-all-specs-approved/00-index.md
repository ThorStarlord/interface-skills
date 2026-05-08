---
spec_type: index
spec_id: orchestrator-05
created: 2026-05-08
status: draft
intentionally_incomplete: true
---

# Spec Package Index: Orchestrator State 05 — All Specs Approved, No Implementation

> **Fixture purpose:** Test that `ui-orchestrator` recognises a fully-specced package with no implementation artifacts and recommends `ui-spec-linter` before handing off to `ui-generate-code`.

## Files

| # | File | Skill | Status |
|---|---|---|---|
| 1 | `brief.md` | `ui-brief` | approved |
| 2 | `visual-calibration.md` | `ui-visual-calibration` | approved |
| 3 | `blueprint.md` | `ui-blueprint` | approved |
| 4 | `system.md` | `ui-system` | approved |
| 5 | `screen-spec.md` | `ui-screen-spec` | approved |
| 6 | `microcopy.md` | `ui-microcopy` | approved |
| 7 | `acceptance.md` | `ui-acceptance` | approved |

---

## Expected orchestrator output

- **State:** Full spec package present and approved; no implementation or inspection artifacts.
- **Gap:** Spec has not been linted; no code has been generated.
- **Recommended next skill:** `ui-spec-linter`
- **Suggested prompt:** "All spec files are approved. Run `ui-spec-linter` to validate consistency and completeness before handing off to `ui-generate-code`. A clean lint report is the green light for implementation."
