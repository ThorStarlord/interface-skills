# Skill Promotion Tracking

This document tracks the evidence required to promote Interface Skills from `draft` to `stable`.

For the formal architecture and trust model, see [SKILL-CERTIFICATION-SYSTEM.md](docs/promotion/SKILL-CERTIFICATION-SYSTEM.md).

## Promotion Criteria

A draft skill is ready for stable when it has:
1. **3 good fixture runs** (real input, not toy input).
2. **1 intentionally messy/failing fixture** testing its failure modes.
3. **1 downstream consumption test**.
4. **Human Approval** recorded in the evidence table.

A skill is ready for stable when the last three realistic runs produce useful outputs without changing the skill’s output format.

## Promotion Evidence Table

| Skill | Fixture Evidence | Messy/Fail Fixture | Downstream Test | Human Approval | Status |
|---|---|---|---|---|---|
| `ui-surface-inventory` | `/kanban`, `admin-nav`, `/create` | `missing-source` (TBD) | `/create` -> `ui-inspector` | Pending | Draft |
| `ui-screen-spec` | `/kanban`, `admin-nav`, `/create` | `failing-spec-package` | `/create` -> `ui-acceptance` | Pending | Draft |
| `ui-spec-linter` | `/kanban`, `admin-nav`, `/create` | `failing-spec-package` | `/kanban` (V1->V2) | Pending | Draft |
| `ui-inspector` | `/kanban`, `admin-nav`, `/create` | `no-source` (TBD) | `/kanban` -> `ui-redline` | Pending | Draft |
| `setup-interface-skills` | `setup-interface-skills-example` | `unsafe-overwrite` (TBD) | `clean-repo` -> `ui-brief` | Approved | **Stable** |
| `ui-spec-reconcile` | `/kanban`, `admin-nav`, `/create` | `drift-not-canonized` (TBD) | `/kanban` -> `ui-docs-sync` | Pending | Draft |
| `ui-to-issues` | `/kanban`, `admin-nav`, `/create` | `coverage-gap` (TBD) | `admin-nav` -> implementation | Pending | Draft |
| `ui-visual-calibration`| `/create`, `settings-page` | `vague-ref` (TBD) | `/create` -> `ui-blueprint` | Pending | Draft |
| `ui-orchestrator` | `orchestrator-states/` | `incomplete-pkg` | `orchestrator` -> `ui-brief` | Pending | Draft |
| `ui-agent-routing` | `/kanban`, `admin-nav`, `/create` | `admin-nav` (report fail) | `/kanban` -> reports | Pending | **Stable** |
| `ui-docs-sync` | `/kanban`, `admin-nav`, `/create` | `admin-nav` (fail) | `/kanban` -> routing | Pending | **Stable** |

## Detailed Evidence Logs

### `ui-surface-inventory`
- **2026-05-10**: Added canonical sections. Output usually maps to `01-inspector-evidence.md` or dedicated inventory file.
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
- **Status**: Promoted to Stable with approved human review and zero-repair cryptographic proof.
