---
spec_type: acceptance
spec_id: admin-sidebar-nav
based_on:
  - 02-brief.md
  - 04-blueprint.md
  - 05-screen-spec.md
  - 06-component-spec-admin-sidebar.md
  - 07-microcopy.md
created: 2025-05-22
status: draft
---

# Acceptance checklist: Admin Sidebar Navigation

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
| ☐ | blocker | [A] Active state maps to `/admin/finance` even when on legacy `/admin/financeiro`. | brief §6 |
| ☐ | blocker | [M] Deep-link: Correct parent section expands automatically based on path. | screen-spec §2 |
| ☐ | major | [A] `aria-expanded` correctly reflects expansion state on toggles. | component §7 |

## 4. Behavior

| | Severity | Criterion | Source |
|---|---|---|---|
| ☐ | blocker | [A] Clicking a ModuleTab navigates immediately. | screen-spec §2 |
| ☐ | blocker | [A] Clicking the Brand Link navigates to `/admin`. | brief §4 |

## 5. Accessibility

| | Severity | Criterion | Source |
|---|---|---|---|
| ☐ | blocker | [A] All links and toggles are keyboard reachable (Tab). | component §7 |
| ☐ | blocker | [A] Active links use `aria-current="page"`. | component §7 |
| ☐ | major | [A] Icons are marked `aria-hidden="true"`. | component §7 |

## 6. Microcopy

| | Severity | Criterion | Source |
|---|---|---|---|
| ☐ | blocker | [M] Section labels are uppercase (SECRETARIA, etc.). | microcopy §3 |
| ☐ | major | [M] "Em breve" and "Demo" badges appear on appropriate routes. | microcopy §2 |

## 7. Open questions
- Confirmation of final sidebar width.
