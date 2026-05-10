---
report_type: ui-docs-sync
scope: kanban-spec-package
created: 2026-05-10
spec_package_index: docs/saas-frontend/specs/kanban/00-index.md
status_source: docs/saas-frontend/specs/kanban/SPEC-LINT-REPORT-V2.md
---

# UI Docs Sync Report - /kanban

## Scope

Checked cross-doc alignment for the /kanban spec package across:
- CLAUDE.md
- AGENTS.md
- .github/copilot-instructions.md
- docs/saas-frontend/README.md
- INTERFACE_SKILLS.md
- docs/PRODUCT-INTEGRITY-BACKLOG.md

Reference status used for accuracy checks:
- docs/saas-frontend/specs/kanban/00-index.md reports package status as current.
- docs/saas-frontend/specs/kanban/SPEC-LINT-REPORT-V2.md reports PASS (0 critical), with remaining major/minor cleanup items.

## Summary Verdict

- Agent files checked: 6
- Files that explicitly reference /kanban spec package: 4 of 6
- Link validity check (all valid): no
- Description accuracy vs current package status: partially accurate
- Overall sync state: needs updates

## Per-file Results

| File | References /kanban spec package? | Link valid? | Description accurate/current? | Notes |
|---|---|---|---|---|
| CLAUDE.md | yes | partial | no | Has /kanban row in Interface Skills routing, but points to folder path and marks it as (future). Should point to docs/saas-frontend/specs/kanban/00-index.md and mark current. |
| AGENTS.md | no (direct package pointer missing) | no (for package entry) | no | Has Interface Skills workflow and content-journey references including /kanban, but UI spec package list under Repo Anchors only lists /create and app shell. Missing /kanban package pointer. |
| .github/copilot-instructions.md | no (direct package pointer missing) | no (for package entry) | no | Has content-journey mention with /kanban but UI spec package list includes only /create and app shell. Missing /kanban routing pointer to package index. |
| docs/saas-frontend/README.md | no (in UI Spec Packages section) | no (for package entry) | no | /kanban route exists in page inventory, but UI Spec Packages table has no /kanban row. |
| INTERFACE_SKILLS.md | yes | partial | no | Route-to-folder mapping includes /kanban folder path but marked (future). Should reflect current and point to 00-index.md entrypoint. |
| docs/PRODUCT-INTEGRITY-BACKLOG.md | yes (kanban issues exist) | n/a | partial | Contains multiple Kanban-related issues and resolutions, but no explicit cross-reference to kanban redline file (docs/saas-frontend/specs/kanban/09-redlines.md). |

## Link Validity Check

Checked target existence in workspace:
- docs/saas-frontend/specs/kanban/00-index.md exists: yes
- docs/saas-frontend/specs/kanban/SPEC-LINT-REPORT-V2.md exists: yes
- docs/saas-frontend/specs/kanban/09-redlines.md exists: yes

Why overall link validity is "no":
- Several docs do not point to the /kanban package index at all.
- Some docs describe /kanban package as future, which is stale vs current status.

## Accuracy Review Against Current Package Status

Current package status evidence:
- 00-index.md frontmatter: status: current
- SPEC-LINT-REPORT-V2.md: PASS, zero critical issues

Stale/outdated statements detected:
- CLAUDE.md: /kanban shown as (future)
- INTERFACE_SKILLS.md: /kanban shown as (future)
- .github/copilot-instructions.md: no /kanban package entry
- docs/saas-frontend/README.md: no /kanban package status row
- AGENTS.md: no explicit /kanban package pointer in UI spec package references

## Recommended Patches

### 1) CLAUDE.md

Update Interface Skills Routing table entry:
- From: /kanban -> docs/saas-frontend/specs/kanban/ (future)
- To: /kanban -> docs/saas-frontend/specs/kanban/00-index.md (current - read before editing)

Also add /kanban to the earlier "UI spec packages (load when working on the relevant page)" list.

### 2) AGENTS.md

In Repo Anchors section under UI spec packages, add:
- /kanban -> docs/saas-frontend/specs/kanban/00-index.md (status: current)

This ensures Codex routing includes a direct package entrypoint, not only generic Interface Skills references.

### 3) .github/copilot-instructions.md

Under "For component-level contracts on specced pages", add:
- /kanban -> docs/saas-frontend/specs/kanban/00-index.md (status: current). Load at minimum: 05-screen-spec.md, 06-component-spec-*.md, 08-acceptance-checklist.md.

This aligns Copilot routing with the active package and prevents stale /create-only behavior.

### 4) docs/saas-frontend/README.md

Under "UI Spec Packages", add a row:
- /kanban | docs/saas-frontend/specs/kanban/00-index.md | current

This is required for frontend onboarding parity with /create.

### 5) INTERFACE_SKILLS.md

In Route-to-folder mapping, replace:
- /kanban -> docs/saas-frontend/specs/kanban/ -> (future)

With:
- /kanban -> docs/saas-frontend/specs/kanban/00-index.md -> current

Optionally keep folder-level path in notes, but entrypoint should be index file.

### 6) docs/PRODUCT-INTEGRITY-BACKLOG.md

Optional but recommended:
- Add explicit "Related redline" cross-reference in Kanban-related sections to docs/saas-frontend/specs/kanban/09-redlines.md for tighter traceability between integrity issues and redline findings.

## Final Routing Health Check

Goal: any agent landing on /kanban work should immediately know where the spec package lives.

Current state: not yet achieved consistently across all agent-facing docs.

After applying recommended patches above, routing should be fully aligned for Claude Code, Codex, and Copilot.
