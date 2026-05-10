---
tracker_mode: markdown
scope: /kanban
generated_from:
  - docs/saas-frontend/specs/kanban/09-redlines.md
  - docs/saas-frontend/specs/kanban/08-acceptance-checklist.md
  - docs/saas-frontend/specs/kanban/05-screen-spec.md
  - docs/saas-frontend/specs/kanban/06-component-spec-kanban-card.md
  - docs/saas-frontend/specs/kanban/06-component-spec-post-detail-modal.md
---

# UI to Issues Plan: /kanban

## Issue Index

| Issue ID | Tier | Title | Component | Est. Effort | Related Spec |
| --- | --- | --- | --- | --- | --- |
| kanban-a11y-keyboard | Tier 1 | Make kanban cards keyboard accessible with visible focus states | KanbanCard.tsx | 4-6h (3 SP) | 08-H / 09-K-001,K-002 |
| kanban-a11y-aria | Tier 1 | Add accessible labels to icon-only card menu trigger | KanbanCard.tsx | 2-3h (2 SP) | 08-H / 09-K-003 |
| kanban-regenerate | Tier 2 | Add Regenerar action to board card menu with feedback | KanbanCard.tsx, KanbanPage.tsx | 3-4h (2 SP) | 08-C,08-G / 09-K-004 |
| kanban-modal-mobile | Tier 3 | Make post detail modal robust on mobile keyboard open | PostDetailModal.tsx | 3-5h (2 SP) | 08-A,08-C / 09-K-006 |
| kanban-polish-motion-docs | Tier 3 | Normalize hover and drag motion values in code and specs | KanbanCard.tsx, 03-visual-calibration.md, 04-blueprint.md | 2-3h (1 SP) | 08-B,08-I / 09-K-007,K-008 |

---

## Tier 1: Accessibility (Critical) - Must ship

### Issue: kanban-a11y-keyboard
- Title: Make kanban cards keyboard accessible with visible focus states
- Redline traceability: K-001, K-002
- Description:
  - Card interaction currently depends on pointer/click behavior. Keyboard users cannot reliably focus or operate card actions, and focus visibility is not explicitly guaranteed for the card root.
  - Implement full keyboard semantics for the card root and visible focus treatment aligned with the component/accessibility contract.
  - Primary spec package references:
    - [Redline K-001](09-redlines.md#k-001)
    - [Redline K-002](09-redlines.md#k-002)
    - [Acceptance H. Accessibility](08-acceptance-checklist.md#h-accessibility)
    - [Kanban Card accessibility contract](06-component-spec-kanban-card.md#8-accessibility-requirements)
- Acceptance criteria (verbatim from 08-acceptance-checklist.md):
  - [ ] H-02 | Severity: Critical | Method: Inspector + Keyboard | Cards are focusable (tabindex=0 or equivalent interactive semantics). | Notes/Evidence:
  - [ ] H-03 | Severity: Critical | Method: Keyboard + Visual | Focus indicator is visible on focused cards (outline not removed). | Notes/Evidence:
  - [ ] H-04 | Severity: High | Method: Keyboard | Enter on focused card opens modal. | Notes/Evidence:
  - [ ] H-05 | Severity: High | Method: Keyboard | Space key approval/primary action mapping works as documented. | Notes/Evidence:
- Implementation notes:
  - File/component:
    - saas_frontend/src/components/kanban/KanbanCard.tsx (card root motion.div and click handlers)
  - Hook/state touchpoints:
    - Local hover state in KanbanCard (isHovered)
    - Parent callback path in saas_frontend/src/pages/KanbanPage.tsx (selectedPost, setSelectedPost)
  - Expected changes:
    - Add keyboard semantics (role, tabIndex, keydown handlers)
    - Ensure focus ring/focus-visible styles on card root
    - Prevent key handling conflicts with drag/gesture paths
- How to verify:
  - Tab reaches each card in board mode.
  - Enter and Space activate expected card behavior.
  - Focus indicator is always visible in keyboard navigation flow.

### Issue: kanban-a11y-aria
- Title: Add accessible labels to icon-only card menu trigger
- Redline traceability: K-003
- Description:
  - The card dropdown trigger is icon-only and needs an explicit accessible name so screen readers announce intent before opening the menu.
  - Add/validate aria-label coverage for this control in board cards.
  - Primary spec package references:
    - [Redline K-003](09-redlines.md#k-003)
    - [Acceptance H. Accessibility](08-acceptance-checklist.md#h-accessibility)
    - [Kanban Card accessibility contract](06-component-spec-kanban-card.md#8-accessibility-requirements)
- Acceptance criteria (verbatim from 08-acceptance-checklist.md):
  - [ ] H-08 | Severity: Critical | Method: Inspector + Screen reader | All icon-only/action buttons include meaningful aria-label values. | Notes/Evidence:
- Implementation notes:
  - File/component:
    - saas_frontend/src/components/kanban/KanbanCard.tsx (DropdownMenuTrigger button with MoreHorizontal)
  - Expected changes:
    - Add contextual aria-label (for example: Menu de ações do post)
    - Keep aria semantics compatible with existing DropdownMenu behavior
- How to verify:
  - Screen reader announces the button purpose before menu open.
  - Axe or equivalent check reports no button-name violation.

---

## Tier 2: Feature Parity (Major) - Should ship soon

### Issue: kanban-regenerate
- Title: Add Regenerar action to board card menu with feedback
- Redline traceability: K-004
- Description:
  - Regenerar exists in review-deck flow but is missing in board card menu. This creates capability mismatch across kanban surfaces.
  - Add Regenerar in board mode menu and reuse the same webhook/toast behavior contract already used in review flow.
  - Primary spec package references:
    - [Redline K-004](09-redlines.md#k-004)
    - [Acceptance C. Interactions](08-acceptance-checklist.md#c-interactions--gestures)
    - [Acceptance G. Error States](08-acceptance-checklist.md#g-error-states)
    - [Screen spec dropdown/menu notes](05-screen-spec.md#zone-4-modals--overlays)
- Acceptance criteria (verbatim from 08-acceptance-checklist.md):
  - [ ] C-08 | Severity: High | Method: Click + Visual | Three-dot menu opens with Editar, Regenerar, Deletar options. | Notes/Evidence:
  - [ ] C-09 | Severity: High | Method: Click + Network spy | Regenerar triggers webhook and shows toast "Procurando nova ideia...". | Notes/Evidence:
  - [ ] G-03 | Severity: High | Method: Failure simulation | Regenerate no-credit failure shows "Limite de creditos atingido" (with proper accent in UI text implementation). | Notes/Evidence:
- Implementation notes:
  - File/component:
    - saas_frontend/src/components/kanban/KanbanCard.tsx (DropdownMenuContent items)
    - saas_frontend/src/pages/KanbanPage.tsx (regenerate function and toast/error path wiring)
  - Hook/state touchpoints:
    - useKanban refreshPosts flow
    - Local regeneratingDeckIds/reviewDeckHiddenIds behavior (adapt for board action if needed)
  - Expected changes:
    - Add Regenerar menu item in board card menu
    - Wire callback from card to page-level regenerate handler
    - Preserve success and error feedback parity with review mode
- How to verify:
  - Board menu includes Regenerar for eligible cards.
  - Clicking action calls webhook and shows progress/success feedback.
  - Simulated failure shows actionable error toast.

---

## Tier 3: Polish & Documentation (Minor) - Can defer

### Issue: kanban-modal-mobile
- Title: Make post detail modal robust on mobile keyboard open
- Redline traceability: K-006
- Description:
  - Modal behavior on mobile keyboard open needs explicit contract enforcement and test evidence.
  - Ensure mobile interaction remains usable when text inputs focus and virtual keyboard resizes viewport.
  - Primary spec package references:
    - [Redline K-006](09-redlines.md#k-006)
    - [Acceptance A. Layout & Responsive](08-acceptance-checklist.md#a-layout--responsive)
    - [Acceptance C. Interactions](08-acceptance-checklist.md#c-interactions--gestures)
    - [Post Detail Modal layout/accessibility contract](06-component-spec-post-detail-modal.md#4-layout-and-responsive-contract)
- Acceptance criteria (verbatim from 08-acceptance-checklist.md):
  - [ ] A-09 | Severity: Critical | Method: Visual + Inspector | Modal is centered on desktop and full-screen on mobile (<768px). | Notes/Evidence:
  - [ ] A-10 | Severity: High | Method: Gesture + Visual | Modal remains usable when mobile keyboard opens; body scroll/viewport behavior keeps focused field visible. | Notes/Evidence:
  - [ ] C-13 | Severity: Critical | Method: Tap + Visual | Tap card opens PostDetailModal full-screen on mobile. | Notes/Evidence:
- Implementation notes:
  - File/component:
    - saas_frontend/src/components/kanban/PostDetailModal.tsx (DialogContent sizing, overflow, keyboard-safe layout)
  - Supporting integration:
    - saas_frontend/src/pages/KanbanPage.tsx (selectedPost open/close behavior)
  - Expected changes:
    - Mobile full-screen dialog contract and keyboard-safe scrolling
    - Preserve desktop centered behavior
- How to verify:
  - On iOS Safari and Android Chrome, focused fields remain visible with keyboard open.
  - Modal opens full-screen on mobile breakpoint and centered on desktop.

### Issue: kanban-polish-motion-docs
- Title: Normalize hover and drag motion values in code and specs
- Redline traceability: K-007, K-008
- Description:
  - Hover and drag animation values are close but drift between implementation and documented contract.
  - Align code and docs to one canonical set of values and keep reduced-motion behavior explicit.
  - Primary spec package references:
    - [Redline K-007](09-redlines.md#k-007)
    - [Redline K-008](09-redlines.md#k-008)
    - [Acceptance B. Visual & Design System](08-acceptance-checklist.md#b-visual--design-system)
    - [Acceptance I. Performance](08-acceptance-checklist.md#i-performance)
    - [Visual calibration](03-visual-calibration.md)
    - [Blueprint](04-blueprint.md)
- Acceptance criteria (verbatim from 08-acceptance-checklist.md):
  - [ ] B-04 | Severity: High | Method: Visual + Inspector | Card hover state uses shadow lift + scale 1.01. | Notes/Evidence:
  - [ ] B-05 | Severity: High | Method: Visual + Inspector | Dragging state uses scale 1.04 + elevated shadow. | Notes/Evidence:
  - [ ] I-04 | Severity: High | Method: Visual + reduced-motion setting | Animations are smooth and respect prefers-reduced-motion. | Notes/Evidence:
- Implementation notes:
  - File/component:
    - saas_frontend/src/components/kanban/KanbanCard.tsx (hover transition, whileDrag scale)
  - Spec updates:
    - docs/saas-frontend/specs/kanban/03-visual-calibration.md
    - docs/saas-frontend/specs/kanban/04-blueprint.md (if motion values referenced)
    - docs/saas-frontend/specs/kanban/09-redlines.md (close-out or reconciliation note after merge)
  - Expected changes:
    - Pick canonical values and enforce consistently in code/spec text
    - Confirm reduced-motion path remains intact
- How to verify:
  - Inspector confirms canonical scale values in hover and drag states.
  - Docs and implementation use the same motion numbers.

---

## Summary

- Total issues: 5
- Tier 1 (critical): 2 items
- Tier 2 (should): 1 item
- Tier 3 (can defer): 2 items
- Total estimate: 14-21 hours
- Story points total: 10 SP
- Recommended sequencing:
  1. Tier 1 first: kanban-a11y-keyboard, kanban-a11y-aria
  2. Tier 2 next: kanban-regenerate
  3. Tier 3 last: kanban-modal-mobile, kanban-polish-motion-docs

## Dependency notes

- kanban-a11y-keyboard should ship before kanban-a11y-aria verification pass to avoid duplicate QA cycles on keyboard/screen-reader checks.
- kanban-regenerate can run in parallel with Tier 3 work if Tier 1 is already in review.
- kanban-polish-motion-docs should be finalized after any motion changes introduced by accessibility focus treatments.
