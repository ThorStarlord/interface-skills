---
fixture_type: rubric
spec_id: kanban
status: approved
---

# Rubric: Kanban Recovery Fixture

## What this fixture tests

- Spec Recovery on an existing complex UI surface.
- Linter ability to catch state, breakpoint, token, and copy drift.
- Reconcile ability to distinguish spec-wrong vs implementation-wrong.
- Docs sync ability to detect missing package routing.
- Agent routing ability to repair direct index links.
- Issue slicing ability to cover critical redlines.

## ui-surface-inventory
- [ ] Identifies approval queue surface.
- [ ] Identifies review/deck mode toggle.
- [ ] Identifies kanban status columns.
- [ ] Identifies post detail modal.
- [ ] Identifies empty queue state.
- [ ] Does not collapse modal, list, and column surfaces into one vague page.
- [ ] Does not invent unrelated surfaces.
