---
spec_type: issues-plan
tracker_mode: markdown
scope: admin-sidebar-nav
created: 2025-05-22
status: draft
---

# UI Implementation Plan: Admin Sidebar Navigation

## Issue 1: Implement Active State Logic for Module Tabs
- **Labels:** `ui`, `frontend`, `blocker`
- **Spec:** `docs/saas-frontend/specs/admin-nav/06-component-spec-module-tab.md#4-state-matrix`
- **Description:** Currently, only the top-level "Painel de Gestão" highlights when active. This task implements the `isActive` state for all module-level tabs within the `AdminSidebar`.
- **Task List:**
  - [ ] Calculate `isActive` for each item in the `navigationSections` loop in `portal-shell.tsx`.
  - [ ] Apply `bg-[#28346c] text-white` classes to the `Link` when `isActive` is true.
  - [ ] Ensure the parent section is expanded on mount if a child is active.
- **Acceptance Criteria:**
  - [ ] Target `/admin/finance` shows high-contrast background and white text when the URL matches.
- **Verification:** Navigate to `/admin/financeiro` and verify the "Financeiro" tab is highlighted and the section is expanded.

---

## Issue 2: Align Finance Module with Canonical Path
- **Labels:** `ui`, `frontend`, `blocker`
- **Spec:** `docs/saas-frontend/specs/admin-nav/02-brief.md#6-success-criteria`
- **Description:** Migrate the Finance module navigation to the target canonical path `/admin/finance` and handle redirection from legacy `/admin/financeiro`.
- **Task List:**
  - [ ] Update `lib/admin-product-surface.ts` to set `/admin/finance` as the primary `href` for the Finance dashboard.
  - [ ] Implement a redirect shim from `/admin/financeiro` to `/admin/finance`.
- **Acceptance Criteria:**
  - [ ] Sidebar uses `/admin/finance` as the link destination.
- **Verification:** Clicking the Finance tab leads to `/admin/finance`.

---

## Issue 3: Implement Accessibility Landmark and State Attributes
- **Labels:** `ui`, `accessibility`, `major`
- **Spec:** `docs/saas-frontend/specs/admin-nav/08-acceptance-checklist.md#5-accessibility`
- **Description:** Enhance the sidebar's accessibility by adding standard ARIA attributes.
- **Task List:**
  - [ ] Add `aria-current="page"` to active navigation links.
  - [ ] Add `aria-hidden="true"` to all decorative Lucide icons.
- **Acceptance Criteria:**
  - [ ] Screen readers correctly identify the current page and skip decorative icons.
- **Verification:** Inspect the DOM and verify `aria-current` is present on active tabs.

---

## Issue 4: Polish Sidebar Visuals (Rounded Corners)
- **Labels:** `ui`, `polish`, `minor`
- **Spec:** `docs/saas-frontend/specs/admin-nav/03-visual-calibration.md#concrete-visual-decisions`
- **Description:** Align the sidebar container with the "Warm Concierge" shape language.
- **Task List:**
  - [ ] Apply `rounded-[28px]` to the main `AdminSidebar` container in `portal-shell.tsx`.
- **Acceptance Criteria:**
  - [ ] Sidebar has large rounded corners matching the design tokens.
- **Verification:** Visual check of the sidebar container edges.
