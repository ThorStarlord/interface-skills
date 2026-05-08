---
spec_type: index
spec_id: orchestrator-06
created: 2026-05-08
status: current
intentionally_incomplete: true
---

# Spec Package Index: Orchestrator State 06 — Inspector Present

> **Fixture purpose:** Test that `ui-orchestrator` recognises a package with an approved inspector report and recommends `ui-redline` as the next step (not `ui-inspector` again).

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
| 8 | `redlines/inspector-report.md` | `ui-inspector` | approved |

---

## Expected orchestrator output

- **State:** Full spec package plus an approved inspector report. No redline audit yet.
- **Gap:** Inspector evidence has been gathered but not yet used to produce a redline audit.
- **Recommended next skill:** `ui-redline`
- **Suggested prompt:** "Inspector report is approved. Use `ui-redline` to compare the live implementation against the spec, using the inspector evidence as your source of truth."
