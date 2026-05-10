# Skill Promotion Tracking

This document tracks the evidence required to promote Interface Skills from `draft` to `stable`.

## Promotion Criteria

A draft skill is ready for stable when:
1. It has **3–5 real approved fixtures** across different UI types.
2. It has **1 intentionally messy/failing fixture** testing its failure modes.
3. It has **1 documented downstream consumption test**.
4. It has **Human Approval** recorded in the evidence table.
5. The last 3 realistic runs produce useful outputs without changing the skill’s output format.

## Promotion Evidence Table

| Skill | Fixture Evidence | Messy/Fail Fixture | Downstream Test | Human Approval | Status |
|---|---|---|---|---|---|
| `ui-surface-inventory` | `/kanban`, `admin-nav`, `/create` | `missing-source` (TBD) | `/create` -> `ui-inspector` | Pending | Draft |
| `ui-screen-spec` | `/kanban`, `admin-nav`, `/create` | `failing-spec-package` | `/create` -> `ui-acceptance` | Pending | Draft |
| `ui-spec-linter` | `/kanban`, `admin-nav`, `/create` | `failing-spec-package` | `/kanban` (V1->V2) | Pending | Draft |
| `ui-inspector` | `/kanban`, `admin-nav`, `/create` | `no-source` (TBD) | `/kanban` -> `ui-redline` | Pending | Draft |
| `setup-interface-skills` | `setup-interface-skills-example` | `unsafe-overwrite` (TBD) | `clean-repo` -> `ui-brief` | Pending | Draft |
| `ui-spec-reconcile` | `/kanban`, `admin-nav`, `/create` | `drift-not-canonized` (TBD) | `/kanban` -> `ui-docs-sync` | Pending | Draft |
| `ui-to-issues` | `/kanban`, `admin-nav`, `/create` | `coverage-gap` (TBD) | `admin-nav` -> implementation | Pending | Draft |
| `ui-visual-calibration`| `/create`, `settings-page` | `vague-ref` (TBD) | `/create` -> `ui-blueprint` | Pending | Draft |
| `ui-orchestrator` | `orchestrator-states/` | `incomplete-pkg` | `orchestrator` -> `ui-brief` | Pending | Draft |
| `ui-agent-routing` | `/kanban`, `admin-nav`, `/create` | `admin-nav` (report fail) | `/kanban` -> reports | Pending | **Stable** |
| `ui-docs-sync` | `/kanban`, `admin-nav`, `/create` | `admin-nav` (fail) | `/kanban` -> routing | Pending | **Stable** |

## Detailed Evidence Logs

### `ui-surface-inventory`
- **2026-05-10**: Renamed to `surface-inventory.md`. Added canonical sections.
- **Fixtures**: `/kanban`, `admin-nav`, `/create`.
- **Status**: Ready for final human review.

### `ui-screen-spec`
- **Fixtures**: `/kanban`, `admin-nav`, `/create`.
- **Status**: Ready for final human review.

### `ui-spec-linter`
- **Fixtures**: `/kanban`, `admin-nav`, `/create`, `failing-spec-package`.
- **Status**: Ready for final human review.

### `ui-inspector`
- **Fixtures**: `/kanban`, `admin-nav`, `/create`.
- **Status**: Needs dedicated failure fixture (e.g. invalid URL or missing permissions).

### `ui-spec-reconcile`
- **Fixtures**: `/kanban`, `admin-nav`, `/create`.
- **Status**: Ready for final human review.

### `ui-to-issues`
- **Fixtures**: `/kanban`, `admin-nav`, `/create`.
- **Status**: Ready for final human review.

### `setup-interface-skills`
- **Fixtures**: `setup-interface-skills-example`.
- **Status**: Needs more variety (monorepo, nested AGENTS.md).
