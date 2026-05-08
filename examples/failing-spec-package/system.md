---
spec_type: system
spec_id: failing-package
created: 2026-05-08
status: approved
---

# Design System: Post Composer Widget

## Colour Tokens

| Token | Value |
|---|---|
| `color.action.primary` | `#2563eb` |
| `color.action.primary.hover` | `#1d4ed8` |
| `color.text.primary` | `#111827` |
| `color.surface.base` | `#f9fafb` |
| `color.surface.elevated` | `#ffffff` |

## Typography Tokens

| Token | Value |
|---|---|
| `type.body.md` | Inter 16px / 400 |
| `type.label.sm` | Inter 12px / 600 |
| `type.heading.lg` | Inter 20px / 700 |

<!-- DEFECT FD-05: The space.* token category is intentionally absent.
     ui-spec-linter should catch this as a Blocker because:
     - blueprint.md references "standard spacing" without tokens
     - No space.* tokens are defined in this file
     - The component spec references spacing without token values
-->

## Shape Tokens

| Token | Value |
|---|---|
| `radius.sm` | 4px |
| `radius.md` | 6px |
| `radius.lg` | 8px |

## Shadow Tokens

| Token | Value |
|---|---|
| `shadow.sm` | 0 1px 3px rgba(0,0,0,0.08) |
