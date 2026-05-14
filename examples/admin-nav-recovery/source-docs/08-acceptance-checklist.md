---
spec_type: acceptance
spec_id: admin-sidebar-nav
based_on: none
  - 02-brief.md
  - 04-blueprint.md
  - 05-screen-spec.md
  - 06-component-spec-admin-sidebar.md
  - 07-microcopy.md
created: 2025-05-22
status: draft
---

# Acceptance checklist: Admin Sidebar Navigation

## How to use this checklist

- Each item has a severity: **blocker** (must fix before ship), **major** (should fix before ship), **minor** (fix before next milestone), **polish** (fix when time permits).
- Each item is marked with an explicit automation source: **[A:playwright]**, **[A:axe]**, **[A:lint]**, **[A:unit]**, or **[M]**.
- Where a criterion traces back to a specific spec section, the source is noted in `[source]`.

## 1. Layout

| | Severity | Criterion | Source |
|---|---|---|---|
| ☐ | blocker | [M] Visual layout matches the wireframe (Sidebar at left, 420px width). | blueprint §4 |
| ☐ | blocker | [M] Sidebar background color is `#111944`. | calibration §2.2 |
| ☐ | major | [M] Whitespace: `space-y-9` between sections, `space-y-2` between tabs. | blueprint §4.2 |

## 2. Responsive

| | Severity | Criterion | Source |
|---|---|---|---|
| ☐ | blocker | [M] Below 1024px, sidebar is hidden and only reachable via burger menu. | blueprint §5 |
| ☐ | blocker | [M] Burger menu triggers a full-height drawer containing the sidebar. | screen-spec §5 |

## 3. States (AdminSidebar / ModuleTab)

| | Severity | Criterion | Source |
|---|---|---|---|
| ☐ | blocker | [M] Active tab highlight: `bg-[#28346c]` and white text. | blueprint §4 |
| ☐ | blocker | [A:unit] Active state maps to `/admin/finance` even when on legacy `/admin/financeiro`. | brief §6 |
| ☐ | blocker | [M] Deep-link: Correct parent section expands automatically based on path. | screen-spec §2 |
| ☐ | major | [A:unit] `aria-expanded` correctly reflects expansion state on toggles. | component §7 |

## 4. Behavior

| | Severity | Criterion | Source |
|---|---|---|---|
| ☐ | blocker | [A:playwright] Clicking a ModuleTab navigates immediately. | screen-spec §2 |
| ☐ | blocker | [A:playwright] Clicking the Brand Link navigates to `/admin`. | brief §4 |

## 5. Accessibility

| | Severity | Criterion | Source |
|---|---|---|---|
| ☐ | blocker | [A:playwright] All links and toggles are keyboard reachable (Tab). | component §7 |
| ☐ | blocker | [A:lint] Active links use `aria-current="page"`. | component §7 |
| ☐ | major | [A:lint] Icons are marked `aria-hidden="true"`. | component §7 |

## 6. Microcopy

| | Severity | Criterion | Source |
|---|---|---|---|
| ☐ | blocker | [M] Section labels are uppercase (SECRETARIA, etc.). | microcopy §3 |
| ☐ | major | [M] "Em breve" and "Demo" badges appear on appropriate routes. | microcopy §2 |

## 7. Open questions
- Confirmation of final sidebar width.
