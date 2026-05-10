---
spec_type: lint-report
spec_id: kanban-spec-package-lint
based_on:
  - docs/saas-frontend/specs/kanban/00-index.md
  - docs/saas-frontend/specs/kanban/01-inspector-evidence.md
  - docs/saas-frontend/specs/kanban/02-brief.md
  - docs/saas-frontend/specs/kanban/03-visual-calibration.md
  - docs/saas-frontend/specs/kanban/04-blueprint.md
  - docs/saas-frontend/specs/kanban/05-screen-spec.md
  - docs/saas-frontend/specs/kanban/06-component-spec-kanban-card.md
  - docs/saas-frontend/specs/kanban/06-component-spec-post-detail-modal.md
  - docs/saas-frontend/specs/kanban/07-microcopy.md
  - docs/saas-frontend/specs/kanban/08-acceptance-checklist.md
created: 2026-05-10
status: draft
---

# SPEC Lint Report: /kanban

## Findings Table

| Check category | Issue severity | Finding | Affected file | Recommendation |
|---|---|---|---|---|
| Completeness | ℹ️ Info | Missing package index was detected at lint start and has been created. | docs/saas-frontend/specs/kanban/00-index.md | Keep this file updated whenever package composition changes. |
| Completeness | ❌ Critical | Required metadata is inconsistent: 01-inspector-evidence has no frontmatter created/status and no explicit purpose statement section. | docs/saas-frontend/specs/kanban/01-inspector-evidence.md | Add frontmatter (spec_type, spec_id, created, status) and a dedicated Purpose section. |
| Completeness | ⚠️ Warning | Optional redline summary file is missing while a redlines folder exists. | docs/saas-frontend/specs/kanban/redlines | Add docs/saas-frontend/specs/kanban/09-redlines.md when first redline cycle is completed, or document explicitly as not yet run. |
| Completeness | ℹ️ Info | Acceptance checklist contains 106 items and includes severity levels, meeting the requested volume/priority requirement. | docs/saas-frontend/specs/kanban/08-acceptance-checklist.md | Keep totals synchronized if checklist items change. |
| Consistency | ❌ Critical | Kanban state model is inconsistent with requested canonical set (backlog, draft, scheduled, approved, published). Current specs use review and often omit draft/scheduled as kanban_status states. | docs/saas-frontend/specs/kanban/02-brief.md | Align all state contracts to one canonical status machine and update every file plus mapping table. |
| Consistency | ⚠️ Warning | Breakpoint contract is not fully aligned across files: some sections use mobile <1024, others use mobile <768 with tablet 768-1023. | docs/saas-frontend/specs/kanban/01-inspector-evidence.md | Standardize one breakpoint model (prefer explicit sm/md/lg contract) and update all references. |
| Consistency | ⚠️ Warning | Animation timing contract drifts between docs: component spec defines hover 100ms and drag 150ms while visual calibration includes different timings for hover overlay and drag behavior. | docs/saas-frontend/specs/kanban/03-visual-calibration.md | Add one canonical animation table and reference it from blueprint/screen/component specs. |
| Consistency | ⚠️ Warning | Border-radius values are contradictory in acceptance checklist (rounded-2xl described as 28px) versus other docs where rounded-2xl maps to smaller radius. | docs/saas-frontend/specs/kanban/08-acceptance-checklist.md | Correct the numeric mapping to match the design token system and implementation. |
| Consistency | ℹ️ Info | Component naming is consistent for primary card and modal components (KanbanCard and PostDetailModal) across files. | docs/saas-frontend/specs/kanban/05-screen-spec.md | Preserve naming consistency and avoid introducing aliases. |
| Consistency | ℹ️ Info | Column labels are largely consistent (Ideias salvas, Para decidir, Agendados, Publicados) across blueprint/screen/microcopy/checklist. | docs/saas-frontend/specs/kanban/04-blueprint.md | Keep this label set as single source for UI-facing names. |
| Vocabulary | ❌ Critical | PT-BR accent policy is violated in multiple user-facing strings inside microcopy and checklist examples (voce, nao, creditos, publicacao). | docs/saas-frontend/specs/kanban/07-microcopy.md | Replace all unaccented PT-BR forms and enforce an accent QA pass in checklist evidence. |
| Vocabulary | ❌ Critical | Forbidden internal terminology appears in user-facing copy examples and acceptance wording (automation_tier, kanban_status, tokens). | docs/saas-frontend/specs/kanban/07-microcopy.md | Keep internal terms only in technical mapping sections; never in approved user-visible strings. |
| Vocabulary | ⚠️ Warning | Warm concierge tone is strong in parts but inconsistent where technical/repo-facing wording appears in user-copy tables. | docs/saas-frontend/specs/kanban/07-microcopy.md | Split implementation-note language from approved customer copy; keep approved copy only in the master table. |
| Vocabulary | ⚠️ Warning | Section voice style is mixed (imperative vs descriptive) across files, reducing editorial consistency. | docs/saas-frontend/specs/kanban/04-blueprint.md | Choose one header style guide and normalize section titles across package docs. |
| Coverage | ℹ️ Info | Blueprint zones are fully mapped into screen-spec zones (Hero, Stepper, Content, Modals, Toasts). | docs/saas-frontend/specs/kanban/05-screen-spec.md | Keep zone IDs stable to maintain traceability. |
| Coverage | ⚠️ Warning | Not all interactive elements from screen-spec have dedicated component specs (e.g., PipelineStepper, EmptyColumnState, ProactiveCardStack). | docs/saas-frontend/specs/kanban/05-screen-spec.md | Add component specs or add explicit rationale that they are covered by screen-spec + acceptance only. |
| Coverage | ⚠️ Warning | Component states are not fully traceable into acceptance checklist (e.g., selected, transient success, disabled nuances). | docs/saas-frontend/specs/kanban/08-acceptance-checklist.md | Add explicit checklist items per component state matrix row. |
| Coverage | ⚠️ Warning | Screen-spec error states are broader than Section G in acceptance checklist; some cases are only partially covered (realtime loss, media-load fallback, safe-flow unload path). | docs/saas-frontend/specs/kanban/05-screen-spec.md | Add one-to-one mapping from each error state to an acceptance item ID. |
| Coverage | ⚠️ Warning | Edge-case coverage is incomplete: several edge cases from screen-spec Section G are not explicitly testable in checklist sections. | docs/saas-frontend/specs/kanban/08-acceptance-checklist.md | Introduce dedicated edge-case subsection with IDs mapping to screen-spec edge-case numbers. |
| Coverage | ⚠️ Warning | Accessibility requirements in component specs are only partially mirrored in acceptance Section H (missing explicit checks for aria-roledescription and nested discard-confirm focus behavior). | docs/saas-frontend/specs/kanban/06-component-spec-post-detail-modal.md | Expand Section H with explicit test cases for all component-level accessibility requirements. |
| Quality | ❌ Critical | Broken/placeholder cross-reference exists in inspector evidence ([02-redline.md](#)) and does not resolve to package files. | docs/saas-frontend/specs/kanban/01-inspector-evidence.md | Replace with valid link to 09-redlines.md (when created) or remove placeholder link. |
| Quality | ⚠️ Warning | Outdated future references in screen-spec point to non-existent consolidated file names (06-component-specs.md). | docs/saas-frontend/specs/kanban/05-screen-spec.md | Update links to actual split files (06-component-spec-kanban-card.md and 06-component-spec-post-detail-modal.md). |
| Quality | ⚠️ Warning | Multiple code blocks lack syntax highlighting language tags, reducing readability and review precision. | docs/saas-frontend/specs/kanban/01-inspector-evidence.md | Add explicit fence languages (ts, css, text, json) to all code snippets. |
| Quality | ℹ️ Info | Most tables are structurally valid and readable; no major markdown table corruption found. | docs/saas-frontend/specs/kanban/03-visual-calibration.md | Maintain current table formatting discipline and keep columns aligned. |

## Summary

- Total issues found: 24
- Critical issues count (must fix before shipping): 6
- Warnings count (should fix): 13
- Info items count (nice-to-have): 5
- Pass/fail verdict: FAIL

## Gate Decision

Result is FAIL because critical issues exist in completeness, consistency, vocabulary, and link quality. Resolve all critical items first, then rerun the lint pass to validate warnings cleanup.
