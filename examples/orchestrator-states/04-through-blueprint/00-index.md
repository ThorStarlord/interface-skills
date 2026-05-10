---
spec_type: index
spec_id: orchestrator-04
created: 2026-05-08
status: draft
intentionally_incomplete: true
---

# Spec Package Index: Orchestrator State 04 — Through Blueprint

> **Fixture purpose:** Test that `ui-orchestrator` recognises a package with brief, visual-calibration, and blueprint all approved, and recommends `ui-system` as the next step.

## Files

| # | File | Skill | Status |
|---|---|---|---|
| 1 | `brief.md` | `ui-brief` | approved |
| 2 | `visual-calibration.md` | `ui-visual-calibration` | approved |
| 3 | `blueprint.md` | `ui-blueprint` | approved |

---

## Expected orchestrator output

- **State:** Brief, visual calibration, and layout blueprint are approved.
- **Gap:** No design system / token definitions; no screen-level data mapping.
- **Recommended next skill:** `ui-system`
- **Suggested prompt:** "Blueprint is approved. Before writing screen or component specs, define the design tokens with `ui-system` — the token names will be referenced in all downstream specs."
