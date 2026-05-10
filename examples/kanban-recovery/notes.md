---
spec_type: fixture-notes
spec_id: kanban
status: current
---

# Notes: Kanban Recovery Fixture

Fixture refresh marker: manual-freeze-2026-05-10
Source docs refresh marker: manual-refresh-2026-05-10

# Optional marker templates
# Fixture refresh marker: manual-freeze-YYYY-MM-DD
# Source docs refresh marker: manual-refresh-YYYY-MM-DD

## Human review

- Machine validation: pass
- Human review required: yes
- Human status: pending
- Reviewer:
- Review date:
- Notes:
  - Whether coarse-pointer-first default should be canonical.
  - Whether implementation drag scale should be accepted as target.
  - Whether review-vs-draft status semantics are product-correct.
  - Whether approved microcopy rows are final PT-BR.

## Downstream consumption

- `ui-redline` consumes:
  - `input/01-inspector-evidence.md`
  - `input/04-screen-spec.md`
  - `input/06-acceptance.md`
- `ui-spec-reconcile` consumes:
  - `input/07-redline-audit.md`
- `ui-docs-sync` consumes:
  - `00-index.md`
  - `reports/SPEC-RECONCILE-SUMMARY.md`
- `ui-agent-routing` consumes:
  - `reports/DOCS-SYNC-REPORT.md`
- `ui-to-issues` consumes:
  - `input/07-redline-audit.md`
  - `reports/SPEC-RECONCILE-SUMMARY.md`
