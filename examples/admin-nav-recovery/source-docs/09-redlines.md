---
spec_type: redline
spec_id: admin-sidebar-nav-redline-1
based_on: none
  - 02-brief.md
  - 04-blueprint.md
  - 05-screen-spec.md
  - 06-component-spec-admin-sidebar.md
implementation_source: static source-code (portal-shell.tsx)
redline_mode: static partial
partial: true
created: 2025-05-22
status: draft
---

# Redline: Admin Sidebar Navigation<br>_(partial — static-code-assisted)_

## 0. Summary

| Severity | Count |
|---|---|
| Blocker | 2 |
| Major | 2 |
| Minor | 1 |
| Polish | 1 |

**Recommendation:** Block on fixes. The active-state logic for module tabs and the canonical finance path mismatch are critical blockers.

## 1. Mismatches

| # | Section | Spec says | Implementation does | Severity | Verification | Fix |
|---|---|---|---|---|---|---|
| 1 | brief §6 (Success Criteria) | Sidebar uses canonical `/admin/finance`. | Sidebar uses registry's `/admin/financeiro`. | **Blocker** | verified by static code | Update registry or add shim to map `financeiro` -> `finance`. |
| 2 | component §4 (AdminSidebar) | Module tabs have active state highlighting. | Code only has active class for "Painel de Gestão" link. | **Blocker** | verified by static code | Add `isActive` check inside `section.items.map` and apply `bg-[#28346c] text-white`. |
| 3 | component §7 (Accessibility) | Active links use `aria-current="page"`. | `aria-current` is missing. | **Major** | verified by static code | Add `aria-current={isActive ? "page" : undefined}` to all Nav/Module links. |
| 4 | component §7 (Accessibility) | Icons are marked `aria-hidden="true"`. | Icons are not marked. | **Major** | verified by static code | Add `aria-hidden="true"` to Lucide icon components in tabs. |
| 5 | calibration §2.2 (Shape) | Sidebar container uses `rounded-[28px]`. | Sidebar container uses `rounded-none` (default div behavior). | **Minor** | verified by static code | Add `rounded-[28px]` to the main `AdminSidebar` wrapper. |
| 6 | blueprint §4.2 (Hierarchy) | Brand and Panel links are redundant. | Both point to `/admin`. | **Polish** | verified by static code | Consolidate or differentiate Brand and Dashboard links. |

## 2. Fix order
1. **Blockers:** Active-state logic for module tabs; Finance path alignment.
2. **Majors:** ARIA attributes (current/hidden).
3. **Minors:** Container rounding.

## 3. Refactor prompt

````
Refactor the AdminSidebar in `portal-shell.tsx` to fix the following issues based on the spec package:

Blockers (must fix):
1. Implement active state logic for module tabs: inside the `navigationSections.map` loop, calculate `isActive` for each item (currentPath === item.href) and apply `bg-[#28346c] text-white` classes when true.
2. Align with the canonical Finance path: ensure the Finance tab highlights correctly for both `/admin/finance` and `/admin/financeiro`.

Majors (should fix):
3. Add `aria-current={isActive ? "page" : undefined}` to all navigation links (Dashboard and Module tabs).
4. Mark all Lucide icons in the sidebar as `aria-hidden="true"`.

Minors:
5. Apply `rounded-[28px]` to the main sidebar container div.
````

## 4. What I could not verify from this input
- Hover transitions and color accuracy (requires live browser).
- Screen reader prosody for uppercase section labels.
