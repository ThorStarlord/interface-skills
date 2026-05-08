---
spec_type: index
spec_id: pulse-create
created: 2026-05-08
status: draft
recovery: true
---

# Spec Package: Pulse /create Route (Spec Recovery)

This package is a **Retrospective Specification Recovery** example. Pulse already ships a `/create` content creation screen with no prior specification. This package documents what was built, identifies the target design intent, and closes the gap between observed implementation and agreed product behaviour.

It demonstrates the full recovery workflow:
`ui-surface-inventory` → `ui-inspector` → `ui-brief` → `ui-visual-calibration` → `ui-blueprint` → `ui-screen-spec` → `ui-microcopy` → `ui-acceptance` → `ui-spec-linter`

## Contents and sign-off

| # | File | Skill | Status | Last updated |
|---|------|-------|--------|--------------|
| 1 | [`inventory.md`](inventory.md) | `ui-surface-inventory` | approved | 2026-05-08 |
| 2 | [`redlines/inspector-report.md`](redlines/inspector-report.md) | `ui-inspector` | approved | 2026-05-08 |
| 3 | [`brief.md`](brief.md) | `ui-brief` | approved | 2026-05-08 |
| 4 | [`visual-calibration.md`](visual-calibration.md) | `ui-visual-calibration` | approved | 2026-05-08 |
| 5 | [`blueprint.md`](blueprint.md) | `ui-blueprint` | approved | 2026-05-08 |
| 6 | [`screen-spec.md`](screen-spec.md) | `ui-screen-spec` | draft | 2026-05-08 |
| 7 | [`microcopy.md`](microcopy.md) | `ui-microcopy` | draft | 2026-05-08 |
| 8 | [`acceptance.md`](acceptance.md) | `ui-acceptance` | draft | 2026-05-08 |
| 9 | [`spec-linter-report.md`](spec-linter-report.md) | `ui-spec-linter` | draft | 2026-05-08 |

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
| 2026-05-08 | Initial recovery draft. All files created; screen-spec, microcopy, acceptance remain draft pending open question resolution. |
