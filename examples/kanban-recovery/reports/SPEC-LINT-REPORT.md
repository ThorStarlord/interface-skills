---
spec_type: lint-report
spec_id: kanban-recovery-lint
created: 2026-05-14
status: draft
evidence_level: promotion_candidate_run
---

# Lint Report: kanban-recovery

## 1. Package Inventory
- [x] brief.md (Found as 02-brief.md)
- [x] blueprint.md (Found as 04-blueprint.md)
- [ ] system.md (**MISSING** - Found 03-visual-calibration.md instead)
- [ ] acceptance.md (**MISSING** - Found 08-acceptance-checklist.md instead)
- [ ] microcopy.md (**MISSING** - Found 07-microcopy.md instead)
- [x] component-specs/ (Found 06-component-spec-kanban-card.md and 06-component-spec-post-detail-modal.md)

**Critique:** Package uses non-standard numbering prefix (01-, 02-) and non-standard names. ADR 0001 requires strict naming.

## 2. Completeness Checks
- [x] Brief: Goals, User, Actions, Success Criteria, Constraints present.
- [/] Blueprint: Layout, Hierarchy present. **Lint Error:** Line 61 contains "TBD".
- [x] System: Palette, Typography, Spacing, Shape present (in visual-calibration.md).
- [x] Component Specs: Props, Anatomy, State Matrix present for KanbanCard.

## 3. Vocabulary Checks
- [x] No vague "intuitive" or "clean" used as primary descriptions.
- [x] Success criteria are measurable (80ms feedback, 2 min completion).

## 4. Consistency Checks
- [x] Blueprint spacing (gap-6/24px) matches Visual Calibration tokens.
- [x] Brief success criteria (80% first-time users) matches Acceptance checklist targets.

## 5. State Coverage
- [x] KanbanCard includes: Rest, Hover, Focus, Dragging, Loading, Error, Success, Exit.

## Summary: FAIL
- **Errors:** 3 naming violations (system.md, acceptance.md, microcopy.md), 1 TBD violation.
- **Recommendations:** Rename files to match ADR 0001. Resolve TBD in blueprint.md.
