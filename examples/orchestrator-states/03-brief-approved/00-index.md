---
spec_type: index
spec_id: orchestrator-03
created: 2026-05-08
status: draft
intentionally_incomplete: true
---

# Spec Package Index: Orchestrator State 03 — Brief Approved

> **Fixture purpose:** Test that `ui-orchestrator` recognises an approved brief with no further artifacts and recommends `ui-visual-calibration` as the next step.

## Files

| # | File | Skill | Status |
|---|---|---|---|
| 1 | `brief.md` | `ui-brief` | approved |

---

## Expected orchestrator output

- **State:** Brief approved; no layout or visual direction established.
- **Gap:** Visual calibration and layout have not been started.
- **Recommended next skill:** `ui-visual-calibration`
- **Suggested prompt:** "Brief is approved. Before designing the layout, establish the visual language with `ui-visual-calibration` — density, shape, surface style, and palette — so that `ui-blueprint` has a concrete foundation to work from."
