---
name: ui-screen-spec
description: Missing bridge between blueprint and components (turns layout into implementation-ready screen contracts)
status: draft
---

# UI Screen Spec

This skill creates a screen-level composition spec from a blueprint. It describes which components appear in which regions, data dependencies, state ownership, and responsive behavior.

## Component Instantiation and Region Mapping
The screen spec must explicitly map components to layout regions defined in the blueprint.

```markdown
### Region: Sidebar (`<aside>`)
- **`NavigationMenu`**: Receives `activeItem` from page context.
- **`UserProfileBadge`**: Requires user object (avatar, name).

### Region: Main Content (`<main>`)
- **`DashboardHeader`**: Contains page title and primary action.
- **`DataGrid`**: Renders the main dataset.
```

## State Ownership and Taxonomy
Explicitly reference `state-taxonomy.md` when describing the application states for the screen. Every screen must define how it handles at least:

- **Ideal State:** All data loaded successfully.
- **Loading State:** Skeletons or spinners in specific regions.
- **Error State:** Network failure or empty dataset.
- **Empty State:** No data available yet.

Use the State Matrix representation to detail how different regions react to these states.
