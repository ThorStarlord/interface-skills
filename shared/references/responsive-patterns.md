# Responsive Patterns

This document outlines standard responsive behaviors for layout components.

## Breakpoints

Breakpoint names align with Tailwind CSS defaults so that ranges produced by `ui-blueprint`, `ui-screen-spec`, and `ui-acceptance` map directly onto utility classes when code is generated.

| Name | Min width | Tailwind prefix | Typical device |
|------|-----------|-----------------|----------------|
| `sm` | 640px     | `sm:`           | Large phone / small tablet portrait |
| `md` | 768px     | `md:`           | Tablet portrait |
| `lg` | 1024px    | `lg:`           | Tablet landscape / small laptop |
| `xl` | 1280px    | `xl:`           | Desktop |
| `2xl`| 1536px    | `2xl:`          | Widescreen |

"Mobile" means `< sm` (no prefix in Tailwind). Always describe responsive behavior in terms of the named breakpoint (`md`, `lg`) rather than a raw pixel value, so the spec stays portable across CSS frameworks.

## Reflow Verbs

When a layout changes across breakpoints, the change must be described using one of these verbs (defined once so every spec uses the same vocabulary):

- **stack** — children that sat horizontally now sit vertically.
- **collapse** — a region disappears behind a control (hamburger menu, accordion).
- **hide** — the region is removed from view entirely (no replacement control).
- **move** — the region appears in a different slot of the grid.
- **resize** — the region's width or height changes proportionally to the viewport.
- **swap** — one component is replaced by a different component with the same role (desktop datepicker → mobile native date input).

## Common Transitions
- **Sidebar**: At `< md`, **collapse** behind a hamburger menu. At `md+`, visible as a fixed left rail.
- **Multi-column grids**: At `< sm`, **stack** to 1 column. At `sm`, 2 columns. At `lg+`, 3 or more columns.
- **Modal**: At `< md`, **resize** to full-screen sheet. At `md+`, centered dialog with max-width.
- **Primary navigation**: At `< md`, **swap** to bottom tab bar. At `md+`, top bar or side rail.
- **Data table**: At `< md`, **swap** to stacked card list (one card per row). At `md+`, traditional table.
