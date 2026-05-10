---
spec_type: redline
spec_id: kanban-redline-2026-05-10
created: 2026-05-10
status: current
sources:
  - 01-inspector-evidence.md
  - 02-brief.md
  - 03-visual-calibration.md
  - 04-blueprint.md
  - 05-screen-spec.md
  - 06-component-spec-kanban-card.md
  - 06-component-spec-post-detail-modal.md
  - 07-microcopy.md
  - 08-acceptance-checklist.md
  - saas_frontend/src/pages/KanbanPage.tsx
  - saas_frontend/src/components/kanban/KanbanCard.tsx
  - saas_frontend/src/components/kanban/PostDetailModal.tsx
---

# Redlines: /kanban

## Scope checks requested
- 4-column board layout vs blueprint: PASS (matches current contract on desktop).
- PostDetailModal centered/full-screen contract: PARTIAL (centered desktop is correct; mobile full-screen contract not implemented).
- Accessibility gaps from inspector vs acceptance: FAIL (critical gaps remain).
- Responsive breakpoint logic: PARTIAL (desktop threshold is consistent at 1024px, but tablet/mobile default-mode contract drift exists).
- Animation timing values: PARTIAL (stagger and card enter/exit match; hover and drag values drift from spec text in places).

## Findings

### K-001
- Category: Accessibility
- Severity: Critical
- Location: saas_frontend/src/components/kanban/KanbanCard.tsx:136
- Current behavior:
  - Card root is clickable motion.div with onClick but no keyboard semantics (no tabIndex, no role, no onKeyDown).
  - Evidence: motion.div and onClick at lines 136 and 152.
- Expected behavior:
  - Acceptance requires focusable cards and keyboard access (08-acceptance-checklist.md:118, 08-acceptance-checklist.md:119).
  - Component spec requires keyboard map and card semantics (06-component-spec-kanban-card.md, Accessibility section).
- Recommendation:
  - Add tabIndex={0}, role="button", onKeyDown for Enter/Space, and visible focus styling.
- Acceptance criteria:
  - Tab can focus each card.
  - Enter opens modal.
  - Focus ring is visible and remains AA compliant.

### K-002
- Category: Accessibility
- Severity: Critical
- Location: saas_frontend/src/components/kanban/KanbanCard.tsx:396
- Current behavior:
  - More-actions icon button is icon-only and lacks explicit aria-label.
- Expected behavior:
  - All icon-only action buttons must include meaningful aria-labels (08-acceptance-checklist.md:124).
- Recommendation:
  - Add aria-label="Menu de acoes do post" (or equivalent contextual label).
- Acceptance criteria:
  - Screen reader announces purpose of button before menu opens.
  - Axe has no button-name violation for this control.

### K-003
- Category: Accessibility
- Severity: Critical
- Location: saas_frontend/src/pages/KanbanPage.tsx:112
- Current behavior:
  - There is no aria-live region announcing status moves (only aria-label on stepper and close button).
- Expected behavior:
  - Status changes announced via aria-live (08-acceptance-checklist.md:127).
- Recommendation:
  - Add a polite live region and publish movement messages on approve/reject/drag transitions.
- Acceptance criteria:
  - Moving a card announces "Post movido para ..." once per change in screen readers.

### K-004
- Category: Interaction
- Severity: Critical
- Location: saas_frontend/src/components/kanban/KanbanCard.tsx:403
- Current behavior:
  - Board card menu offers Ver detalhes / Copiar legenda / published-only items, but no Regenerar entry.
  - Regenerate webhook path exists only in review-deck flow (KanbanPage.tsx:421), not in board card menu.
- Expected behavior:
  - Acceptance expects menu actions including Regenerar and regenerate webhook feedback (08-acceptance-checklist.md:60, 08-acceptance-checklist.md:61).
- Recommendation:
  - Add Regenerar action in board menu with same backend contract used by review deck.
- Acceptance criteria:
  - In board mode, menu contains Regenerar.
  - Action calls webhook and shows success/error toast path.

### K-005
- Category: Responsive
- Severity: Major
- Location: saas_frontend/src/pages/KanbanPage.tsx:206
- Current behavior:
  - Default review mode is selected by pointer coarse, not strictly by viewport width.
- Expected behavior:
  - Acceptance currently defines mobile review default as <768px (08-acceptance-checklist.md:27, 08-acceptance-checklist.md:64).
- Recommendation:
  - Reconcile contract to implementation truth: coarse-pointer-first default with manual toggle persistence.
- Acceptance criteria:
  - Checklist wording updated and validated across touch laptop, tablet, and phone.

### K-006
- Category: Layout
- Severity: Major
- Location: saas_frontend/src/components/kanban/PostDetailModal.tsx:204
- Current behavior:
  - Modal uses centered dialog with sm:max-w-lg and max-h 90vh; no mobile full-screen variant.
- Expected behavior:
  - Acceptance requires centered desktop and full-screen mobile (08-acceptance-checklist.md:33).
- Recommendation:
  - Either implement full-screen mobile modal, or reconcile checklist if centered 90vh is accepted product behavior.
- Acceptance criteria:
  - Mobile modal contract is explicit and tested on iOS/Android.

### K-007
- Category: Animation
- Severity: Major
- Location: saas_frontend/src/components/kanban/KanbanCard.tsx:156
- Current behavior:
  - Hover lift transition duration is 0.15s; y lift is -3.
- Expected behavior:
  - Visual calibration text describes hover lift and timing differently in places (03-visual-calibration.md:248).
- Recommendation:
  - Reconcile spec timing to actual values where behavior is already desirable and consistent.
- Acceptance criteria:
  - Blueprint and visual calibration show exact implemented hover timing/lift values.

### K-008
- Category: Animation
- Severity: Minor
- Location: saas_frontend/src/components/kanban/KanbanCard.tsx:145
- Current behavior:
  - Drag scale is 1.04.
- Expected behavior:
  - One spec section still references approx 1.05 (03-visual-calibration.md:249).
- Recommendation:
  - Update spec to 1.04 as canonical implementation truth.
- Acceptance criteria:
  - All kanban spec docs reference 1.04 consistently.

### K-009
- Category: Copy
- Severity: Minor
- Location: saas_frontend/src/pages/KanbanPage.tsx:98
- Current behavior:
  - Warm concierge tone is already present in key empty states and guidance copy.
- Expected behavior:
  - Tone should remain supportive and celebratory.
- Recommendation:
  - Mark current copy approved where it already matches voice instead of creating unnecessary rewrites.
- Acceptance criteria:
  - Microcopy doc includes explicit approved-as-is notes for existing compliant strings.

## Severity summary
- Critical: 4
- Major: 3
- Minor: 2

## Notes
- Desktop 4-column layout is aligned with blueprint and implementation.
- PostDetailModal is mostly aligned visually/functionally, with unresolved mobile full-screen contract ambiguity.
