---
spec_type: index
spec_id: kanban-recovery
status: current
agent_routing: wired
fixture_type: rubric
---

# Index: Kanban Recovery Fixture

This fixture captures a realistic retrospective-specification run for a `/kanban` surface. It is intentionally rich enough to exercise draft bridge skills and validator rules that toy examples miss.

## Contents and sign-off

| # | File | Skill / Role | Status |
|---|---|---|---|
| 1 | [input/00-index.md](input/00-index.md) | package map snapshot | current |
| 2 | [input/01-inspector-evidence.md](input/01-inspector-evidence.md) | ui-inspector evidence | approved |
| 3 | [input/02-brief.md](input/02-brief.md) | ui-brief snapshot | draft |
| 4 | [input/03-blueprint.md](input/03-blueprint.md) | ui-blueprint snapshot | draft |
| 5 | [input/04-screen-spec.md](input/04-screen-spec.md) | ui-screen-spec snapshot | draft |
| 6 | [input/05-microcopy.md](input/05-microcopy.md) | ui-microcopy snapshot | draft |
| 7 | [input/06-acceptance.md](input/06-acceptance.md) | ui-acceptance snapshot | current |
| 8 | [input/07-redline-audit.md](input/07-redline-audit.md) | ui-redline source items | complete |
| 9 | [reports/SPEC-LINT-REPORT.md](reports/SPEC-LINT-REPORT.md) | ui-spec-linter v1 | superseded |
| 10 | [reports/SPEC-LINT-REPORT-V2.md](reports/SPEC-LINT-REPORT-V2.md) | ui-spec-linter v2 | current |
| 11 | [reports/SPEC-RECONCILE-SUMMARY.md](reports/SPEC-RECONCILE-SUMMARY.md) | ui-spec-reconcile summary | current |
| 12 | [reports/DOCS-SYNC-REPORT.md](reports/DOCS-SYNC-REPORT.md) | ui-docs-sync result | current |
| 13 | [reports/UI-AGENT-ROUTING-SUMMARY.md](reports/UI-AGENT-ROUTING-SUMMARY.md) | ui-agent-routing result | approved |
| 14 | [reports/GITHUB-ISSUES-PLAN.md](reports/GITHUB-ISSUES-PLAN.md) | ui-to-issues output | current |
| 15 | [fixture.yaml](fixture.yaml) | reproducibility manifest | current |
| 16 | [input/source-snippets/README.md](input/source-snippets/README.md) | source excerpt map | current |
| 17 | [expected/rubric.md](expected/rubric.md) | scoring rubric | approved |
| 18 | [notes.md](notes.md) | human-review markers | current |

## Fixture layout contract

- `source-docs/`: frozen copy of selected source package documents from `ViralFactory` for provenance and offline review. These files are treated as snapshot inputs and are **not** considered generated current-state output by default.
- `input/`: normalized fixture inputs used to evaluate skills in this repository (stable, test-oriented representation).
- `reports/`: skill outputs captured for this fixture run (lint, reconcile, docs-sync, routing, issue plan).
- `expected/`: rubric-style expectations that define what a good output must contain.
- `fixture.yaml`: reproducibility manifest that pins origin (`source_repo`, `source_commit`), source paths, routing context, and tested skills.

Source document refresh is explicit: when `source-docs/` is intentionally refreshed, record it in `notes.md` with a `Source docs refresh marker:` line.

## How agents find this package

This fixture is the active `/kanban` recovery benchmark used to validate draft bridge skills.

Agent entry points expected to reference this fixture in test contexts:
- `AGENTS.md`
- `CLAUDE.md`
- `.github/copilot-instructions.md`

Before editing this fixture, agents must read:
1. `00-index.md`
2. `notes.md`
3. `expected/rubric.md`
