---
spec_type: component
spec_id: button
component: Button
created: 2026-05-08
status: approved
---

# Button — component spec (minimal)

## Anatomy
- Root `button` element
- Optional leading icon slot
- Optional trailing icon slot

## Props
- `label` (string) — visible label
- `variant` (one of `primary`, `secondary`, `ghost`) — visual style
- `disabled` (boolean)
- `loading` (boolean)
- `onClick` (function)

## States
- Default: enabled, `label` visible
- Hover: visual elevation or color change
- Focus: focus outline visible, keyboard accessible
- Disabled: not interactive, reduced contrast
- Loading: shows spinner, `aria-busy="true"` and `aria-live="polite"`

## Accessibility
- Use a native `button` element when possible.
- Ensure `aria-disabled` only when using non-button elements; prefer native button.
- Loading state: set `aria-busy="true"` on the button and hide label from assistive tech only if a screen-reader-friendly label is present.

## Visuals
- `primary`: filled brand color
- `secondary`: outline with brand color border
- `ghost`: no background, subtle text emphasis

## Acceptance (minimal)
- The button responds to keyboard `Enter` and `Space`.
- `disabled` prevents activation and is conveyed visually and programmatically.
- `loading` shows a spinner and prevents repeated activations.
