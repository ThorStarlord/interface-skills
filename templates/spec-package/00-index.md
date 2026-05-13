---
spec_type: index
spec_id: <scope-id>
created: <YYYY-MM-DD>
status: draft
agent_routing: missing
---

# Spec Package: <Feature Name>

[Description of the feature and its goals.]

## Contents and sign-off

| # | File | Skill | Status | Last updated |
|---|------|-------|--------|--------------|
| 1 | [`01-inspector-evidence.md`](01-inspector-evidence.md) | `ui-inspector` | draft | <YYYY-MM-DD> |
| 2 | [`02-brief.md`](02-brief.md) | `ui-brief` | draft | <YYYY-MM-DD> |
| 3 | [`03-visual-calibration.md`](03-visual-calibration.md) | `ui-visual-calibration` | draft | <YYYY-MM-DD> |
| 4 | [`04-blueprint.md`](04-blueprint.md) | `ui-blueprint` | draft | <YYYY-MM-DD> |
| 5 | [`05-screen-spec.md`](05-screen-spec.md) | `ui-screen-spec` | draft | <YYYY-MM-DD> |
| 6 | [`08-acceptance-checklist.md`](08-acceptance-checklist.md) | `ui-acceptance` | draft | <YYYY-MM-DD> |
| 7 | [`09-redlines.md`](09-redlines.md) | `ui-redline` | draft | <YYYY-MM-DD> |
| 8 | [`RUN-MANIFEST.md`](RUN-MANIFEST.md) | (system) | draft | <YYYY-MM-DD> |

## Active reports

| Report type | Active file | Phase | Generated from |
|---|---|---|---|
| Redline | `09-redlines.md` | pre-fix | <commit> |
| Lint | `SPEC-LINT-REPORT.md` | current | <commit> |

## Historical reports

| File | Status | Superseded by |
|---|---|---|
| (none) | | |

## How agents find this package

This package is the active UI source of truth for `<scope>`.

**Agent entry points expected to point here:**
- `CLAUDE.md`
- `AGENTS.md`
- `GEMINI.md`
- `.github/copilot-instructions.md`
- Relevant `llm-docs/*` or folder context files

**Before editing this UI, agents must read:**
1. `00-index.md` (this file)
2. `02-brief.md`
3. `05-screen-spec.md`
4. `08-acceptance-checklist.md`
5. `06-component-spec-*.md` (when touching specific components)
6. Latest redline report (when fixing defects)

---

## Open questions

1. [List any unresolved product or technical questions.]

## Change log

| Date | Change |
|------|--------|
| <YYYY-MM-DD> | Initial draft created using Canonical Package Format. |
