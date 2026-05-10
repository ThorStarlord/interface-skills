---
spec_type: fixture-notes
spec_id: spec-recovery-create
status: current
---

# Notes: Pulse /create Recovery Fixture

## Human review

- Machine validation: pass
- Human review required: yes
- Human status: pending
- Reviewer:
- Review date:
- Notes:
  - Recovery of an existing /create route with undocumented AI behaviors.

## Downstream consumption

- `ui-inspector` consumes:
  - `surface-inventory.md`
- `ui-brief` consumes:
  - `redlines/inspector-report.md`
- `ui-visual-calibration` consumes:
  - `brief.md`
- `ui-blueprint` consumes:
  - `brief.md`
  - `visual-calibration.md`
- `ui-screen-spec` consumes:
  - `blueprint.md`
- `ui-acceptance` consumes:
  - `screen-spec.md`
  - `microcopy.md`
- `ui-spec-linter` consumes:
  - `acceptance.md`
- `ui-agent-routing` consumes:
  - `00-index.md`
