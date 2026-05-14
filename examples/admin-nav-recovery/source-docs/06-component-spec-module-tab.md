---
spec_type: component
spec_id: module-tab
based_on: none
created: 2025-05-22
status: draft
---

# Component spec: ModuleTab

## 1. Context
- **Lives on screen(s):** Inside `AdminSidebar`.
- **Role on those screens:** Individual navigation link.
- **Data it consumes:** `href`, `label`, `icon`, `badge`.

## 2. Anatomy

```
ModuleTab (Link)
├── IconContainer
│   └── LucideIcon
├── Label (Text)
└── Badge (Optional)
```

## 3. Props / content slots

| Prop / slot | Type | Required | Default | Notes |
|---|---|---|---|---|
| `href` | string | yes | — | Destination path |
| `label` | string | yes | — | Link text |
| `icon` | string | yes | — | Key for Lucide icon |
| `isActive` | boolean | yes | — | Calculated by parent |
| `badge` | string | no | null | e.g., "Demo" |

## 4. State matrix

| State | Visual | Behavior | Trigger |
|---|---|---|---|
| Default | Off-white text, transparent bg. | Navigates on click. | Initial |
| Hover | `white/8` bg, `white` text. | Cursor pointer. | Mouse over |
| Focus | Focus ring (offset 2px). | Keyboard ready. | Tab |
| Active (Pressed)| Slight dimming of background. | Fires navigation. | Mousedown |
| Selected (Active State)| `bg-[#28346c]`, `white` text. | Indicates current page. | `isActive === true` |
| Disabled | N/A | — | — |
| Loading | N/A | — | — |

## 7. Accessibility
- **Semantic element:** `<a>` (via Next.js `Link`).
- **ARIA:** `aria-current="page"` when `isActive` is true. `aria-hidden="true"` on icons.
- **Keyboard map:**
  - `Enter`: Navigate.

## 8. Open questions
- Should icons change color when active? (Target: White).

## 9. Assumptions made
- ⚠️ ASSUMED: High contrast ratio for active blue (`#28346c`) against deep blue (`#111944`).
