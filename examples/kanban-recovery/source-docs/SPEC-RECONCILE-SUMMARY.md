---
spec_type: reconcile-summary
spec_id: kanban-reconcile-2026-05-10
created: 2026-05-10
status: current
inputs:
  - 09-redlines.md
  - saas_frontend/src/pages/KanbanPage.tsx
  - saas_frontend/src/components/kanban/KanbanCard.tsx
  - saas_frontend/src/components/kanban/PostDetailModal.tsx
updated_specs:
  - 00-index.md
  - 04-blueprint.md
  - 07-microcopy.md
  - 08-acceptance-checklist.md
---

# Spec Reconcile Summary: /kanban

## 1) Spec wrong, keep implementation (spec updated)

### R-001: Drag scale contract
- Decision: Keep implementation.
- Reason: Code uses drag scale 1.04 and behavior is stable.
- Evidence:
  - Implementation: saas_frontend/src/components/kanban/KanbanCard.tsx:145
  - Old spec wording: docs/saas-frontend/specs/kanban/04-blueprint.md:356
- Spec change applied:
  - docs/saas-frontend/specs/kanban/04-blueprint.md updated from 1.05 to 1.04 in gesture contract.

### R-002: Tablet/mobile default-mode contract
- Decision: Keep implementation.
- Reason: Actual default mode logic is coarse-pointer-first, not purely width-first.
- Evidence:
  - Implementation: saas_frontend/src/pages/KanbanPage.tsx:206
  - Previous acceptance wording: docs/saas-frontend/specs/kanban/08-acceptance-checklist.md:27 and docs/saas-frontend/specs/kanban/08-acceptance-checklist.md:64
- Spec change applied:
  - docs/saas-frontend/specs/kanban/04-blueprint.md responsive/default-mode table reconciled.
  - docs/saas-frontend/specs/kanban/08-acceptance-checklist.md A-02, A-03, C-10 reconciled.

### R-003: Copy tone already compliant
- Decision: Keep implementation.
- Reason: Core hero/CTA/empty-state copy already matches warm concierge direction.
- Evidence:
  - Implementation examples: saas_frontend/src/pages/KanbanPage.tsx:98
- Spec change applied:
  - docs/saas-frontend/specs/kanban/07-microcopy.md new reconciliation notes section added.

## 2) Implementation needs fix (promote to ui-to-issues)

### R-004: Card keyboard accessibility
- Severity: Critical
- Gap:
  - Clickable card root lacks keyboard semantics/focus.
- Evidence:
  - saas_frontend/src/components/kanban/KanbanCard.tsx:136
  - saas_frontend/src/components/kanban/KanbanCard.tsx:152
- Target acceptance:
  - docs/saas-frontend/specs/kanban/08-acceptance-checklist.md:118
  - docs/saas-frontend/specs/kanban/08-acceptance-checklist.md:119

### R-005: Icon-only menu button missing explicit aria label
- Severity: Critical
- Evidence:
  - saas_frontend/src/components/kanban/KanbanCard.tsx:396
- Target acceptance:
  - docs/saas-frontend/specs/kanban/08-acceptance-checklist.md:124

### R-006: Missing aria-live status announcements
- Severity: Critical
- Evidence:
  - saas_frontend/src/pages/KanbanPage.tsx:112
- Target acceptance:
  - docs/saas-frontend/specs/kanban/08-acceptance-checklist.md:127

### R-007: Regenerate path missing from board card actions
- Severity: Critical
- Evidence:
  - Board menu currently lacks regenerate entry: saas_frontend/src/components/kanban/KanbanCard.tsx:403
  - Regenerate webhook path exists only in review flow: saas_frontend/src/pages/KanbanPage.tsx:421
- Target acceptance:
  - docs/saas-frontend/specs/kanban/08-acceptance-checklist.md:60
  - docs/saas-frontend/specs/kanban/08-acceptance-checklist.md:61

### R-008: Mobile modal sizing contract not met
- Severity: Major
- Evidence:
  - saas_frontend/src/components/kanban/PostDetailModal.tsx:204
- Target acceptance:
  - docs/saas-frontend/specs/kanban/08-acceptance-checklist.md:33

## 3) No change needed (spec and code already agree)

### R-009: 4-column desktop board
- Status: Resolved, no action.
- Evidence:
  - saas_frontend/src/pages/KanbanPage.tsx:719
  - docs/saas-frontend/specs/kanban/04-blueprint.md:57

### R-010: Card stagger and entry/exit motion
- Status: Resolved, no action.
- Evidence:
  - Stagger: saas_frontend/src/pages/KanbanPage.tsx:48
  - Entry/exit: saas_frontend/src/components/kanban/KanbanCard.tsx:62 and saas_frontend/src/components/kanban/KanbanCard.tsx:66

## 4) Package bookkeeping
- docs/saas-frontend/specs/kanban/00-index.md updated to mark 09-redlines.md as present/current.
