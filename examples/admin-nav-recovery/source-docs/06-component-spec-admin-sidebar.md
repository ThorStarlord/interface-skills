---
spec_type: component
spec_id: admin-sidebar
based_on: none
created: 2025-05-22
status: draft
---

# Component spec: AdminSidebar

## 1. Context
- **Lives on screen(s):** All Admin Portal pages (`/admin/*`).
- **Role on those screens:** Primary navigation shell.
- **Data it consumes:** `navigationSections` (Registry), `currentPath` (URL), `currentRole` (Auth).

## 2. Anatomy

```
AdminSidebar
├── BrandHeader
│   └── BrandLink (Link to /admin)
├── NavigationContainer (nav)
│   ├── TopLinks
│   │   ├── PortalReturnLink (Link to /)
│   │   └── DashboardLink (Link to /admin)
│   └── SectionList
│       └── Section (repeatable)
│           ├── SectionToggle (button)
│           └── ModuleList (collapsible)
│               └── ModuleTab (repeatable)
```

## 3. Props / content slots

| Prop / slot | Type | Required | Default | Notes |
|---|---|---|---|---|
| `currentPath` | string | yes | — | For active state calculation |
| `navigationSections` | Section[] | yes | — | Data from registry |
| `closeOnNavigate` | boolean | no | false | Used in mobile drawer |
| `onClose` | function | no | — | Callback for mobile drawer |

## 4. State matrix

| State | Visual | Behavior | Trigger |
|---|---|---|---|
| Default | Deep blue bg (`#111944`), Off-white text. | Accordions collapsed unless active. | Initial |
| Hover | Section toggle shows light highlight. | Cursor pointer. | Mouse over toggle |
| Focus | Visible focus ring on toggles/links. | Keyboard ready. | Tab |
| Active / pressed | Toggle rotates chevron. | Expands/collapses section. | Click / Enter |
| Disabled | N/A | — | — |
| Loading | N/A | — | — |
| Error | Inline message "Módulos não carregados". | Blocks navigation. | Registry failure |
| Selected | Parent section expanded if child active. | Persists expansion. | `currentPath` match |

## 5. Behavior
- **Expansion Logic:** On mount, expand the section where `sectionContainsPath(currentPath)` is true. If `/admin`, expand all (configurable).
- **Persistent State:** Section expansion state is kept in local component state (`expandedSectionIds`).

## 7. Accessibility
- **Semantic element:** `<nav>` for the navigation area; `<button>` for toggles.
- **ARIA:** `aria-expanded` on `SectionToggle` correctly reflects state.
- **Keyboard map:**
  - `Tab`: Move between links and toggles.
  - `Enter / Space`: Trigger links or toggle sections.

## 8. Open questions
- Should we persist expansion state in `localStorage`?

## 9. Assumptions made
- ⚠️ ASSUMED: Sidebar is tall enough to require internal scrolling (`overflow-y-auto`).
