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
| 1 | [`brief.md`](brief.md) | `ui-brief` | draft | <YYYY-MM-DD> |
| 2 | [`blueprint.md`](blueprint.md) | `ui-blueprint` | draft | <YYYY-MM-DD> |
| 3 | [`screen-spec.md`](screen-spec.md) | `ui-screen-spec` | draft | <YYYY-MM-DD> |
| 4 | [`acceptance.md`](acceptance.md) | `ui-acceptance` | draft | <YYYY-MM-DD> |

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
2. `brief.md`
3. `screen-spec.md`
4. `acceptance.md`
5. `component-specs/*` (when touching specific components)
6. Latest redline report (when fixing defects)

**Deprecated paths:**
- `<old path>` → `<new path>`

---

## Open questions

1. [List any unresolved product or technical questions.]

## Run history

| Date | Skill | Actor | Result | Artifacts |
|------|-------|-------|--------|-----------|
| <YYYY-MM-DD> | `ui-brief` | human | created | `02-brief.md` |

## Active reports

- [ ] None

## Historical reports

- [ ] None

## Superseded reports

- [ ] None

## Change log

| Date | Change |
|------|--------|
| <YYYY-MM-DD> | Initial draft created. |
