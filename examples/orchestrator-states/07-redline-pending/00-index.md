---
spec_type: index
spec_id: orchestrator-07
created: 2026-05-08
status: current
intentionally_incomplete: true
---

# Spec Package Index: Orchestrator State 07 — Redline Pending

> **Fixture purpose:** Test that `ui-orchestrator` recognises that an inspector report is present but no redline audit exists, and recommends `ui-redline` with a specific note about using the inspector evidence.

This fixture is structurally identical to state 06 but is intended to test a subtler case: the inspector report is present but its findings have not yet been audited against the spec. The orchestrator should distinguish "inspector done, redline not started" from "inspector done, redline in progress" (the latter would have a draft redline file).

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

*(No redline audit file yet.)*

---

## Expected orchestrator output

- **State:** Inspector complete; no redline audit started.
- **Gap:** `redlines/redline-audit.md` does not exist.
- **Recommended next skill:** `ui-redline`
- **Suggested prompt:** "Your inspector report is ready. Run `ui-redline` now — feed it the inspector report alongside your spec files, and it will produce a ranked list of mismatches with prescribed fixes."
