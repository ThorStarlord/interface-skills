---
spec_type: index
spec_id: pulse-create
created: 2026-05-08
status: draft
recovery: true
agent_routing: wired
---

# Spec Package: Pulse /create Route (Spec Recovery)

This package is a **Retrospective Specification Recovery** example. Pulse already ships a `/create` content creation screen with no prior specification. This package documents what was built, identifies the target design intent, and closes the gap between observed implementation and agreed product behaviour.

It demonstrates the full recovery workflow:
`ui-surface-inventory` → `ui-inspector` → `ui-brief` → `ui-visual-calibration` → `ui-blueprint` → `ui-screen-spec` → `ui-microcopy` → `ui-acceptance` → `ui-spec-linter`

## Contents and sign-off

| # | File | Skill | Status | Last updated |
|---|------|-------|--------|--------------|
| 1 | [`surface-inventory.md`](surface-inventory.md) | `ui-surface-inventory` | approved | 2026-05-08 |
| 2 | [`redlines/inspector-report.md`](redlines/inspector-report.md) | `ui-inspector` | approved | 2026-05-08 |
| 3 | [`brief.md`](brief.md) | `ui-brief` | approved | 2026-05-08 |
| 4 | [`visual-calibration.md`](visual-calibration.md) | `ui-visual-calibration` | approved | 2026-05-08 |
| 5 | [`blueprint.md`](blueprint.md) | `ui-blueprint` | approved | 2026-05-08 |
| 6 | [`screen-spec.md`](screen-spec.md) | `ui-screen-spec` | draft | 2026-05-08 |
| 7 | [`microcopy.md`](microcopy.md) | `ui-microcopy` | draft | 2026-05-08 |
| 8 | [`acceptance.md`](acceptance.md) | `ui-acceptance` | draft | 2026-05-08 |
| 9 | [`spec-linter-report.md`](spec-linter-report.md) | `ui-spec-linter` | draft | 2026-05-08 |
| 10 | [`agent-routing-report.md`](agent-routing-report.md) | `ui-agent-routing` | current | 2026-05-09 |
| 11 | [`fixture.yaml`](fixture.yaml) | reproducibility manifest | current | 2026-05-10 |
| 12 | [`notes.md`](notes.md) | human-review markers | current | 2026-05-10 |
| 13 | [`expected/rubric.md`](expected/rubric.md) | scoring rubric | current | 2026-05-10 |

## How agents find this package

This package is the active target specification for the Pulse `/create` UI.

**Routing files that point here:**
- `CLAUDE.md` — §/create — Content Creation Route
- `AGENTS.md` — §/create — Content Creation Route
- `llm-docs/CONTENT-JOURNEY-UX-CONTRACT.md` — §Content Creation / /create

See `agent-routing-report.md` for the full routing chain and verification status.

**Required first read:**
1. `00-index.md` (this file) — scope, status, open questions
2. `brief.md` — goals, primary user, constraints, non-goals
3. `screen-spec.md` — regions, states, behaviour
4. `acceptance.md` — done criteria
5. `redlines/inspector-report.md` — if modifying areas flagged in the redline report

**Deprecated paths — do not use:**
- `docs/saas-frontend/specs/content-journey/create/` → superseded by this recovery package. See `agent-routing-report.md` §6 item 2 for the exact `DEPRECATED.md` content to create in that folder.

---

## Recovery context

**What we found:** The `/create` page was built iteratively over 8 months with no spec. The codebase contains three different caption input implementations; the AI draft panel behaves differently on mobile vs desktop with no documented reason. Several UI decisions were made by individual developers without product review.

**What this package does:** Reconstructs the intended product behaviour by distinguishing *Observed* (what the code does today) from *Target* (what it should do once approved).

## Open questions

1. **AI generation timeout:** Inspector found `setTimeout(3000)` in `AiDraftButton.tsx`. Is 3 seconds the agreed UX threshold? Product must confirm before acceptance criteria can be finalised.
2. **Channel selector ordering:** Observed order is alphabetical; three separate tickets request "most-used first." Target spec assumes most-used-first — needs product sign-off.
3. **Mobile create flow:** Observed implementation redirects to a stripped mobile form. Target spec assumes one responsive layout. Architecture decision required before `screen-spec.md` can be promoted to approved.

## Change log

| Date | Change |
|------|--------|
| 2026-05-09 | Agent routing pass (Patch mode). "How agents find this package" section updated; `agent-routing-report.md` promoted to current. 4 routing edits remain pending on the Pulse codebase (see report §6 items 2–5). |
| 2026-05-08 | Initial recovery draft. All files created; screen-spec, microcopy, acceptance remain draft pending open question resolution. |
