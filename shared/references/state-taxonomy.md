# State Taxonomy

This taxonomy standardizes the way we talk about state in both components and screens.

## Interactive States (Components)
- Default
- Hover
- Active / Pressed
- Focus / Focus-Visible
- Disabled

## Application States (Screens)
- Ideal State
- Empty State
- Loading State (Skeleton / Spinner)
- Partial Data
- Error State
- Offline State
- Permission Denied

## State Matrix Representation
When documenting a component's states, use a matrix format to clearly show how interactive states overlap with application states (if applicable) or variations:

| State | Background | Border | Text/Icon | Shadow | Notes |
|-------|------------|--------|-----------|--------|-------|
| Default | `bg-surface` | `border-default` | `text-primary` | `shadow-sm` | Base state |
| Hover | `bg-surface-hover`| `border-hover` | `text-primary` | `shadow-md` | Cursor pointer |
| Active | `bg-surface-active`| `border-active` | `text-primary` | `none` | Scale down 98% |
| Focus | `bg-surface` | `ring-2 ring-brand`| `text-primary` | `shadow-sm` | Keyboard focus |
| Disabled | `bg-surface-disabled`| `border-disabled`| `text-disabled` | `none` | `cursor-not-allowed` |
