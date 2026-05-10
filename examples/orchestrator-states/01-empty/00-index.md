---
spec_type: index
spec_id: orchestrator-01-empty
created: 2026-05-08
status: draft
intentionally_incomplete: true
---

# Spec Package Index: Orchestrator State 01 — Empty

> **Fixture purpose:** Test that `ui-orchestrator` correctly identifies an empty package and recommends `ui-brief` as the first step.

## Files

*(None — this package contains no spec files.)*

---

## Expected orchestrator output

- **State:** No spec files present.
- **Gap:** Brief has not been started.
- **Recommended next skill:** `ui-brief`
- **Suggested prompt:** "You have no spec files yet. Start by running `ui-brief` to define the product goal, primary user, and success criteria for your feature."
