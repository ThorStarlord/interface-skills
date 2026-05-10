---
spec_type: index
spec_id: orchestrator-02
created: 2026-05-08
status: draft
intentionally_incomplete: true
---

# Spec Package Index: Orchestrator State 02 — Brief Draft

> **Fixture purpose:** Test that `ui-orchestrator` recognises a brief with `status: draft` as a gap — not a completed step — and prompts the user to finish and approve the brief before proceeding.
intentionally_incomplete: true

## Files

| # | File | Skill | Status |
|---|---|---|---|
| 1 | `brief.md` | `ui-brief` | draft |

---

## Expected orchestrator output

- **State:** Brief exists but is not approved.
- **Gap:** Brief is in draft — it has not been reviewed and approved.
- **Recommended next skill:** Continue with `ui-brief` (revise and approve the existing brief)
- **Suggested prompt:** "Your brief is drafted but not yet approved. Review and finalise it before starting layout work — an unapproved brief will cause misalignment downstream."
