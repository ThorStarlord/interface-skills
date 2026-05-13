---
spec_type: lint-report
spec_id: kanban-spec-package-lint-v2
# based_on:
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

# Spec Lint Report

**Package:** kanban
**Date:** 2026-05-10
**Result:** PASS (11 issues found, 0 critical)

## Issues

| Severity | Category | File | Issue | Suggested Fix |
|---|---|---|---|---|
| major | Consistency | docs/saas-frontend/specs/kanban/02-brief.md | `kanban_status` model remains mixed (`review` and `draft` appear as approval-stage sources), creating cross-file ambiguity with the new correction note. | Pick one canonical `kanban_status` flow for the package and normalize all state-machine references in brief/screen/microcopy together. |
| major | Consistency | docs/saas-frontend/specs/kanban/03-visual-calibration.md | Breakpoint contract conflicts with acceptance checklist: visual calibration uses mobile `<1024`, while checklist enforces mobile `<768` and tablet `768-1023`. | Publish one canonical breakpoint table and reference it from blueprint, screen spec, and acceptance checklist. |
| major | Consistency | docs/saas-frontend/specs/kanban/04-blueprint.md | Motion/interaction scale drift: blueprint uses drag scale `1.05` while component spec and checklist use `1.04`. | Keep one source-of-truth animation table and align drag/hover values everywhere. |
| major | Consistency | docs/saas-frontend/specs/kanban/08-acceptance-checklist.md | Radius mapping conflict: checklist states `rounded-2xl = 28px`, while visual calibration maps `rounded-2xl = 16px`. | Correct checklist numeric mapping to match token definition and implementation contract. |
| minor | Completeness | docs/saas-frontend/specs/kanban/00-index.md | Index still reports `09-redlines.md` as not present and optional redline summary missing. | Either add `09-redlines.md` or explicitly document pending redline cycle with target owner/date. |
| minor | Quality | docs/saas-frontend/specs/kanban/01-inspector-evidence.md | Broken placeholder cross-reference still present: `[02-redline.md](#)`. | Replace with actual package path (for example `09-redlines.md` when created) or remove placeholder link. |
| minor | Quality | docs/saas-frontend/specs/kanban/02-brief.md | Stale downstream reference to `06-component-specs.md` (split file no longer exists). | Update references to `06-component-spec-kanban-card.md` and `06-component-spec-post-detail-modal.md`. |
| minor | Quality | docs/saas-frontend/specs/kanban/03-visual-calibration.md | Stale references to consolidated `06-component-specs.md` remain in downstream guidance. | Point guidance to the two existing component-spec files. |
| minor | Vocabulary | docs/saas-frontend/specs/kanban/07-microcopy.md | Vocabulary contract section is corrected, but many approved/current entries remain intentionally unaccented and include implementation-note wording, reducing canonical clarity. | Keep implementation audit notes in a separate subsection and ensure approved UI copy rows are accent-correct PT-BR only. |
| minor | Vocabulary | docs/saas-frontend/specs/kanban/08-acceptance-checklist.md | Microcopy checks still enumerate unaccented examples (`voce/nao/configuracao/creditos`) even after correction notice. | Update checklist examples to accent-correct forms while preserving leak-detection intent. |
| minor | Coverage | docs/saas-frontend/specs/kanban/08-acceptance-checklist.md | Coverage is broad, but not all component-state rows are explicitly trace-linked to checklist IDs (state-to-test traceability gap). | Add cross-reference IDs from component state matrices to acceptance items (especially transient/success and nested focus-trap cases). |

## Summary

- **Critical:** 0 (critical gate clear)
- **Major:** 4
- **Minor:** 7
- **Passed checks:** 24 criteria passed without issue

### Checks that passed in this second pass

- Package structure: core files `00` through `08` exist.
- Metadata completeness: all required files include frontmatter (`spec_type`, `spec_id`, `created`, `status`).
- Critical-fix verification: `01-inspector-evidence.md` now has frontmatter and explicit Purpose section.
- Critical-fix verification: `07-microcopy.md` now includes explicit correction notice for status mapping, automation vocabulary, billing term, and PT-BR accents.
- Accessibility documentation: component specs and screen spec contain explicit keyboard/focus/ARIA requirements.
- State coverage baseline: component specs include robust state matrices (default/rest, hover, focus/focus-visible, active/pressed, dragging, disabled, loading, error, transient success).
- Zone mapping baseline: blueprint and screen-spec zones are mapped and testable at section level.

## Next step

Critical gate is now clear for this package revision. Before promotion to a clean no-warning pass, resolve the 4 major consistency items first, then rerun lint to collapse remaining minor issues.
