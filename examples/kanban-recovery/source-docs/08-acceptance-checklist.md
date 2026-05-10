---
spec_type: acceptance-checklist
spec_id: kanban-acceptance
created: 2026-05-10
status: current
based_on:
  - 03-visual-calibration.md
  - 04-blueprint.md
  - 05-screen-spec.md
  - 06-component-spec-kanban-card.md
  - 06-component-spec-post-detail-modal.md
  - 07-microcopy.md
---

# Acceptance Checklist: /kanban

Use this as the release gate for the kanban surface. Every item must include evidence in the Notes field (screenshot, inspector capture, devtools trace, network log, or test video).

Legend:
- Severity: Critical | High | Nice-to-have
- Methods: Visual | Inspector | Keyboard | Screen reader | Gesture | Network spy | Realtime multi-tab | Lighthouse | Profiler | Cross-browser

## A. Layout & Responsive

- [ ] A-01 | Severity: Critical | Method: Visual + Inspector | Desktop (>=1024px): 4-column grid visible; each column approx 288px wide; column gap 24px. | Notes/Evidence:
- [ ] A-02 | Severity: High | Method: Visual + Inspector | Tablet (768-1023px): single-column board with tabs is consistent and there are no hybrid layout glitches. | Notes/Evidence:
- [ ] A-03 | Severity: Critical | Method: Visual | Coarse-pointer devices default to Review deck on first load; Board toggle remains secondary and functional. | Notes/Evidence:
- [ ] A-04 | Severity: High | Method: Visual + Inspector | Hero section spans full width and respects mobile safe-area padding. | Notes/Evidence:
- [ ] A-05 | Severity: High | Method: Visual + Inspector | Stepper (4 dots + connectors) fits in one row across all breakpoints without clipping. | Notes/Evidence:
- [ ] A-06 | Severity: High | Method: Visual + Inspector | Column headers remain sticky while cards scroll. | Notes/Evidence:
- [ ] A-07 | Severity: Critical | Method: Visual + Inspector | Cards never overflow container; max width/clamp behavior prevents horizontal spill. | Notes/Evidence:
- [ ] A-08 | Severity: High | Method: Visual | Toast placement: bottom-right on desktop; bottom-center on mobile. | Notes/Evidence:
- [ ] A-09 | Severity: Critical | Method: Visual + Inspector | Modal is centered on desktop and full-screen on mobile (<768px). | Notes/Evidence:
- [ ] A-10 | Severity: High | Method: Gesture + Visual | Modal remains usable when mobile keyboard opens; body scroll/viewport behavior keeps focused field visible. | Notes/Evidence:

## B. Visual & Design System

- [ ] B-01 | Severity: High | Method: Inspector | Cards use rounded-2xl (28px as approved token for this surface). | Notes/Evidence:
- [ ] B-02 | Severity: High | Method: Inspector | Buttons use rounded-md (6px). | Notes/Evidence:
- [ ] B-03 | Severity: Critical | Method: Visual + Inspector | Primary CTA is orange (#F97316) with white text and acceptable contrast. | Notes/Evidence:
- [ ] B-04 | Severity: High | Method: Visual + Inspector | Card hover state uses shadow lift + scale 1.01. | Notes/Evidence:
- [ ] B-05 | Severity: High | Method: Visual + Inspector | Dragging state uses scale 1.04 + elevated shadow. | Notes/Evidence:
- [ ] B-06 | Severity: Critical | Method: Inspector | All interactive controls are >=44px target height (or equivalent tappable area). | Notes/Evidence:
- [ ] B-07 | Severity: Critical | Method: Inspector + Contrast tool | Body text contrast ratio >=4.5:1 (WCAG AA). | Notes/Evidence:
- [ ] B-08 | Severity: High | Method: Visual + Inspector | Status badge colors follow semantic tokens (warning=amber, info=blue/cyan, success=green). | Notes/Evidence:
- [ ] B-09 | Severity: Nice-to-have | Method: Visual | Format badges display correct iconography for Carrossel, Reel, Post, Stories. | Notes/Evidence:
- [ ] B-10 | Severity: High | Method: Inspector | Typography uses Inter sans-serif; titles bold; body regular. | Notes/Evidence:
- [ ] B-11 | Severity: High | Method: Visual + Inspector | Line clamp: title max 2 lines; description max 1 line. | Notes/Evidence:

## C. Interactions & Gestures

### Desktop
- [ ] C-01 | Severity: Critical | Method: Gesture + Network spy | Drag card to adjacent column moves card and updates column counts. | Notes/Evidence:
- [ ] C-02 | Severity: High | Method: Gesture + Network spy | Drag card within same column reorders only; no status-transition API call. | Notes/Evidence:
- [ ] C-03 | Severity: High | Method: Gesture | Drop outside valid column snaps card back to origin. | Notes/Evidence:
- [ ] C-04 | Severity: High | Method: Visual | Hover card reveals action controls (Aprovar, Nao quero este, Mais). | Notes/Evidence:
- [ ] C-05 | Severity: Critical | Method: Click + Visual | Click card opens PostDetailModal. | Notes/Evidence:
- [ ] C-06 | Severity: Critical | Method: Click + Network spy | Click Aprovar: card transitions correctly (Publicados if flow publishes now OR approved pipeline step if manual path). | Notes/Evidence:
- [ ] C-07 | Severity: Critical | Method: Click + Network spy | Click Nao quero este: card moves to Ideias salvas. | Notes/Evidence:
- [ ] C-08 | Severity: High | Method: Click + Visual | Three-dot menu opens with Editar, Regenerar, Deletar options. | Notes/Evidence:
- [ ] C-09 | Severity: High | Method: Click + Network spy | Regenerar triggers webhook and shows toast "Procurando nova ideia...". | Notes/Evidence:

### Mobile
- [ ] C-10 | Severity: Critical | Method: Visual | Review deck appears by default on coarse-pointer devices; fine-pointer devices can default to board mode. | Notes/Evidence:
- [ ] C-11 | Severity: Critical | Method: Gesture | Swipe right over threshold (>110px) advances card to next step (ex.: Para decidir -> Agendados). | Notes/Evidence:
- [ ] C-12 | Severity: Critical | Method: Gesture | Swipe left over threshold (>110px) sends card to previous step/backlog path (ex.: Para decidir -> Ideias salvas). | Notes/Evidence:
- [ ] C-13 | Severity: Critical | Method: Tap + Visual | Tap card opens PostDetailModal full-screen on mobile. | Notes/Evidence:
- [ ] C-14 | Severity: High | Method: Tap + Network spy | Tap Aprovar in modal closes modal and removes/relocates card from deck immediately (optimistic behavior). | Notes/Evidence:
- [ ] C-15 | Severity: High | Method: Tap + Visual | Tap Board toggle switches from deck to board/tab view. | Notes/Evidence:
- [ ] C-16 | Severity: High | Method: Tap + Visual | Tap column tab shows only active column; others hidden. | Notes/Evidence:

## D. Modals & Overlays

- [ ] D-01 | Severity: Critical | Method: Keyboard | PostDetailModal traps focus while open. | Notes/Evidence:
- [ ] D-02 | Severity: High | Method: Keyboard | Escape closes modal when there are no unsaved changes and no submit lock. | Notes/Evidence:
- [ ] D-03 | Severity: High | Method: Click | Close button (X) closes modal. | Notes/Evidence:
- [ ] D-04 | Severity: High | Method: Visual | Phone preview panel matches Instagram-style mockup contract. | Notes/Evidence:
- [ ] D-05 | Severity: Critical | Method: Input + Validation | Caption field editable with live character count (max 2200). | Notes/Evidence:
- [ ] D-06 | Severity: High | Method: Input + Validation | Title field editable with live character count (max 50 per current product contract for this flow). | Notes/Evidence:
- [ ] D-07 | Severity: High | Method: Input | Hashtags field editable and persists edits. | Notes/Evidence:
- [ ] D-08 | Severity: High | Method: Input + Visual | Format selector shows current format and allows change (Carrossel/Reel/Post/Stories). | Notes/Evidence:
- [ ] D-09 | Severity: Critical | Method: Visual + Keyboard | Approval button label is explicit and action-oriented (Aprovar/Aprovado contract respected). | Notes/Evidence:
- [ ] D-10 | Severity: High | Method: Input + Close attempt | Dirty-state detection activates when fields are modified. | Notes/Evidence:
- [ ] D-11 | Severity: Critical | Method: Close attempt + Visual | Unsaved changes trigger confirmation dialog before dismissing modal. | Notes/Evidence:
- [ ] D-12 | Severity: High | Method: Network slow/spy | Submit action disables button and shows loading indicator/spinner until resolve. | Notes/Evidence:

## E. Data & Real-time

- [ ] E-01 | Severity: Critical | Method: Network spy + DB check | Cards load from content_calendar excluding kanban_status=archived. | Notes/Evidence:
- [ ] E-02 | Severity: Critical | Method: Visual + query parity check | Column counts equal filtered row counts per status. | Notes/Evidence:
- [ ] E-03 | Severity: Critical | Method: Realtime multi-tab | Realtime subscription active for current project/channel. | Notes/Evidence:
- [ ] E-04 | Severity: Critical | Method: Network spy + DB check | Approve action updates status draft/review path to approved state contract. | Notes/Evidence:
- [ ] E-05 | Severity: Critical | Method: Realtime multi-tab | Approval in tab 1 appears in tab 2 without refresh. | Notes/Evidence:
- [ ] E-06 | Severity: High | Method: Network spy + n8n logs | Kanban trigger webhook emits on approval transition. | Notes/Evidence:
- [ ] E-07 | Severity: High | Method: Stopwatch + network | full_auto flow reaches published view target within 5s under normal conditions. | Notes/Evidence:
- [ ] E-08 | Severity: Critical | Method: Network spy + visual | manual tier keeps card in Agendados/approved state without auto-publish. | Notes/Evidence:
- [ ] E-09 | Severity: Critical | Method: Failure simulation | API/network/rate-limit failures surface actionable toast errors. | Notes/Evidence:
- [ ] E-10 | Severity: High | Method: Network throttling + visual | Optimistic update happens before server confirmation and reconciles on response. | Notes/Evidence:

## F. Empty States

- [ ] F-01 | Severity: High | Method: Visual (seeded data) | Global empty board shows celebratory "Missao cumprida!" messaging with emoji. | Notes/Evidence:
- [ ] F-02 | Severity: High | Method: Visual (seeded data) | Single empty column shows context-specific empty state plus relevant CTA. | Notes/Evidence:
- [ ] F-03 | Severity: Critical | Method: Visual + route test | First-generation empty state includes "Hora de criar!" style CTA linking to /create. | Notes/Evidence:
- [ ] F-04 | Severity: High | Method: Visual (seeded data) | All-published scenario shows populated Publicados and empty remaining columns with correct messaging. | Notes/Evidence:

## G. Error States

- [ ] G-01 | Severity: Critical | Method: Failure simulation + network | Approval rate-limit failure keeps card in source column, shows error toast, offers retry. | Notes/Evidence:
- [ ] G-02 | Severity: Critical | Method: Failure simulation + gesture | Drag mutation failure snaps card back and shows retry-capable error feedback. | Notes/Evidence:
- [ ] G-03 | Severity: High | Method: Failure simulation | Regenerate no-credit failure shows "Limite de creditos atingido" (with proper accent in UI text implementation). | Notes/Evidence:
- [ ] G-04 | Severity: High | Method: Failure simulation | Instagram publish/API failure marks card with error badge and retry action. | Notes/Evidence:
- [ ] G-05 | Severity: Critical | Method: Validation failure | Modal save validation error keeps modal open and binds error message to field. | Notes/Evidence:

## H. Accessibility

- [ ] H-01 | Severity: Critical | Method: Keyboard | Full page is keyboard navigable in logical order. | Notes/Evidence:
- [ ] H-02 | Severity: Critical | Method: Inspector + Keyboard | Cards are focusable (tabindex=0 or equivalent interactive semantics). | Notes/Evidence:
- [ ] H-03 | Severity: Critical | Method: Keyboard + Visual | Focus indicator is visible on focused cards (outline not removed). | Notes/Evidence:
- [ ] H-04 | Severity: High | Method: Keyboard | Enter on focused card opens modal. | Notes/Evidence:
- [ ] H-05 | Severity: High | Method: Keyboard | Space key approval/primary action mapping works as documented. | Notes/Evidence:
- [ ] H-06 | Severity: Nice-to-have | Method: Keyboard | Arrow-key drag alternative works (keyboard move/reorder fallback). | Notes/Evidence:
- [ ] H-07 | Severity: High | Method: Keyboard | Escape closes modal and/or exits active keyboard-drag/menu modes safely. | Notes/Evidence:
- [ ] H-08 | Severity: Critical | Method: Inspector + Screen reader | All icon-only/action buttons include meaningful aria-label values. | Notes/Evidence:
- [ ] H-09 | Severity: High | Method: Screen reader | Column headers expose contextual aria-label including count (ex.: "Coluna: Ideias salvas, 5 posts"). | Notes/Evidence:
- [ ] H-10 | Severity: High | Method: Inspector | Cards use list/listitem/article semantics consistently. | Notes/Evidence:
- [ ] H-11 | Severity: Critical | Method: Screen reader | Status changes are announced via aria-live region. | Notes/Evidence:
- [ ] H-12 | Severity: Critical | Method: Inspector + Screen reader | Modal uses role=dialog, aria-modal=true, and aria-labelledby points to title. | Notes/Evidence:
- [ ] H-13 | Severity: High | Method: Keyboard | Focus returns to invoking card after modal closes. | Notes/Evidence:
- [ ] H-14 | Severity: Critical | Method: Visual + screen reader | Status meaning is not color-only (icon/text + color). | Notes/Evidence:
- [ ] H-15 | Severity: Nice-to-have | Method: Mobile screen reader (VoiceOver/TalkBack) | Swipe/gesture flow remains operable with mobile screen reader enabled. | Notes/Evidence:

## I. Performance

- [ ] I-01 | Severity: Critical | Method: Lighthouse (mobile 4G throttle) | Initial page load <=2s target on mobile profile. | Notes/Evidence:
- [ ] I-02 | Severity: High | Method: Lighthouse + Performance panel | No meaningful CLS during initial load and core interactions. | Notes/Evidence:
- [ ] I-03 | Severity: High | Method: Performance profiler | Drag/drop interaction sustains near 60fps without jank spikes. | Notes/Evidence:
- [ ] I-04 | Severity: High | Method: Visual + reduced-motion setting | Animations are smooth and respect prefers-reduced-motion. | Notes/Evidence:
- [ ] I-05 | Severity: High | Method: Network waterfall | Media thumbnails lazy-load and do not block first meaningful paint. | Notes/Evidence:
- [ ] I-06 | Severity: Nice-to-have | Method: Memory profiler | No modal open/close memory leak trend over repeated cycles. | Notes/Evidence:
- [ ] I-07 | Severity: Nice-to-have | Method: Realtime load test | Realtime subscription remains responsive with 100+ cards. | Notes/Evidence:

## J. Browser & Device Support

- [ ] J-01 | Severity: Critical | Method: Cross-browser | Desktop Chrome (latest 2 versions) passes core flows. | Notes/Evidence:
- [ ] J-02 | Severity: High | Method: Cross-browser | Desktop Safari (latest 2 versions) passes core flows. | Notes/Evidence:
- [ ] J-03 | Severity: High | Method: Cross-browser | Desktop Firefox (latest 2 versions) passes core flows. | Notes/Evidence:
- [ ] J-04 | Severity: Critical | Method: Device test | Mobile iOS Safari (latest 2 versions) passes gesture + modal + approve flows. | Notes/Evidence:
- [ ] J-05 | Severity: Critical | Method: Device test | Mobile Android Chrome (latest 2 versions) passes gesture + modal + approve flows. | Notes/Evidence:
- [ ] J-06 | Severity: Nice-to-have | Method: Device test | Mobile Android Firefox passes key interactions. | Notes/Evidence:
- [ ] J-07 | Severity: High | Method: Cross-device | Desktop Windows pointer/drag behavior is stable and gesture alternatives still usable. | Notes/Evidence:
- [ ] J-08 | Severity: High | Method: Device test | iPad/tablet layout behaves as specified (2-column or approved tab strategy). | Notes/Evidence:
- [ ] J-09 | Severity: Critical | Method: DevTools console | No runtime console errors/warnings during primary journeys. | Notes/Evidence:

## K. Microcopy

- [ ] K-01 | Severity: Critical | Method: Visual copy pass | PT-BR accents are correct in all user-facing strings (voce/nao/configuracao/creditos not leaked). | Notes/Evidence:
- [ ] K-02 | Severity: Critical | Method: Visual copy pass | No internal terms leak to UI (no automation_tier, kanban_status, tokens). | Notes/Evidence:
- [ ] K-03 | Severity: High | Method: Visual review | Warm concierge tone is consistent (supportive, confident, celebratory). | Notes/Evidence:
- [ ] K-04 | Severity: High | Method: Visual review | Empty states are celebratory ("Missao cumprida!" style) rather than technical. | Notes/Evidence:
- [ ] K-05 | Severity: Critical | Method: Failure simulation + copy review | Error messages are actionable and human-readable (never opaque like "Error 500"). | Notes/Evidence:
- [ ] K-06 | Severity: High | Method: Visual review | Buttons use action-oriented verbs (Aprovar, Nao quero este, etc.). | Notes/Evidence:
- [ ] K-07 | Severity: Nice-to-have | Method: Timer + visual | Non-error toasts auto-dismiss around 3 seconds; error toasts persist or require explicit dismissal/retry. | Notes/Evidence:

## Checklist Summary

- Total items: 106
- Category totals:
  - A Layout & Responsive: 10
  - B Visual & Design System: 11
  - C Interactions & Gestures: 16
  - D Modals & Overlays: 12
  - E Data & Real-time: 10
  - F Empty States: 4
  - G Error States: 5
  - H Accessibility: 15
  - I Performance: 7
  - J Browser & Device Support: 9
  - K Microcopy: 7
- Severity totals:
  - Critical: 45
  - High: 54
  - Nice-to-have: 7
