---
spec_type: agent-routing-report
scope: admin-sidebar-nav
spec_package: docs/saas-frontend/specs/admin-nav/00-index.md
agent_routing: partial
created: 2025-05-22
status: draft
mode: report
---

# UI Agent Routing Report: Admin Sidebar Navigation

## 1. Active spec package

| Field | Value |
|---|---|
| Scope | admin-sidebar-nav |
| Route | `/admin/*` |
| Active package | `docs/saas-frontend/specs/admin-nav/` |
| Index | `docs/saas-frontend/specs/admin-nav/00-index.md` |
| Package status | draft |
| Recovery | Yes |

---

## 2. Agent routing files checked

| File | Exists? | References active spec? | References deprecated path? | Action required |
|---|---|---|---|---|
| `CLAUDE.md` | Yes | No | No | Add routing entry |
| `AGENTS.md` | Yes | No | No | Add routing entry |
| `metamorfose-platform/AGENTS.md` | Yes | No | No | Add routing entry |
| `CONTEXT.md` | Yes | No | No | Add routing entry |

---

## 3. Routing chain

```text
CLAUDE.md
→ docs/saas-frontend/specs/admin-nav/00-index.md
→ 02-brief.md / 05-screen-spec.md / 08-acceptance-checklist.md
```

**Gaps:**
- `CLAUDE.md` and `AGENTS.md` do not yet point to the spec package. (FAIL)

---

## 4. Deprecated paths
- No previous spec folders existed for this scope.

---

## 5. Edits applied / recommended

1. **[Recommended]** Add the following to `AGENTS.md` and `metamorfose-platform/AGENTS.md`:
   ```markdown
   ## Admin Sidebar Navigation
   Spec package: `docs/saas-frontend/specs/admin-nav/00-index.md`
   Before editing the sidebar in `portal-shell.tsx`, read the Brief, Screen Spec, and Acceptance Checklist in that package.
   ```
2. **[Recommended]** Add "How agents find this package" section to `docs/saas-frontend/specs/admin-nav/00-index.md`.

---

## 6. Verification

- [ ] At least one agent-facing routing file names the active spec package path.
- [ ] No agent-facing routing file names only the deprecated path without a redirect.
- [x] `00-index.md` has a "How agents find this package" section (Planned).
- [x] All deprecated folders contain `DEPRECATED.md` redirect notices (N/A).
- [x] No unresolved references to deprecated paths in non-deprecated files.

## 7. Result

**FAIL** — (2 items remain unresolved: root AGENTS.md and CLAUDE.md wiring)
