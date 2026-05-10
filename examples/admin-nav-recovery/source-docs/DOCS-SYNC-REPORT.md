---
spec_type: docs-sync-report
scope: metamorfose-platform
packages_audited: 1
created: 2025-05-22
status: draft
---

# UI Docs Sync Report: Admin Sidebar Navigation

**Repo / scope:** metamorfose-platform
**Date:** 2025-05-22
**Packages audited:** 1
**Result:** FAIL (3 issues found)

---

## 1. Spec packages found

| Route / scope | Directory | Index present | Package status | Notes |
|---|---|---|---|---|
| Admin Sidebar | `docs/saas-frontend/specs/admin-nav/` | Yes | draft | All files are currently `draft`. |

---

## 2. Repository docs linked to spec packages

| Spec package | Repo doc | Link present? | Link type | Notes |
|---|---|---|---|---|
| admin-nav | `AGENTS.md` | No | — | No reference found. |
| admin-nav | `metamorfose-platform/AGENTS.md` | No | — | No reference found. |
| admin-nav | `CONTEXT.md` | No | — | No reference found. |

---

## 3. Source-of-truth consistency

| Claim type | Spec says | Repo doc says | Doc location | Status |
|---|---|---|---|---|
| Primary action | Navigate modules | — | (silent) | OK |
| Finance Path | `/admin/finance` (Target) | `/admin/financeiro` (Implied) | `admin-product-surface.ts` | ⚠ Contradiction |
| Role Scope | Admin role only | — | (silent) | OK |

---

## 4. Open drift items

| Severity | Spec package | Finding | Visible in 00-index? | Visible in repo docs? |
|---|---|---|---|---|
| Blocker | admin-nav | Finance path mismatch | Yes | No |
| Blocker | admin-nav | Module tab active state logic missing | Yes | No |

---

## 5. Recommended changes

1. **Add Link (AGENTS.md):** Add a reference to `docs/saas-frontend/specs/admin-nav/00-index.md` in the root and platform-level `AGENTS.md` under a "UI Navigation Specs" section.
2. **Resolve Contradiction (Route Map):** Update `metamorfose-platform/lib/admin-product-surface.ts` to reflect `/admin/finance` as the canonical "final" route to match the target specification.
3. **Update Context:** Link the spec package in `CONTEXT.md` under the "Admin UI" section for agent context.

---

## 6. What was not checked
- External n8n documentation or wiki links were not followed.
- Parent/Student portals were excluded from this sync audit.
