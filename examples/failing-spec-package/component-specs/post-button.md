---
spec_type: component-spec
spec_id: failing-package
component: PostButton
created: 2026-05-08
status: approved
---

# Component Spec: PostButton

## Anatomy

- Root: `<button type="submit">`
- Label slot: text node ("Submit" by default)
- Icon slot: optional trailing icon

## Props

| Prop | Type | Default | Description |
|---|---|---|---|
| `label` | string | "Submit" | Button label text |
| `disabled` | boolean | false | Disables the button |
| `onClick` | function | — | Click handler |

## States

<!-- DEFECT FD-06: The `loading` state is intentionally absent.
     This button triggers an async submit action (see brief §6 "submit button shows a loading state").
     A button that triggers async actions MUST define a loading state.
     ui-spec-linter should catch this as a Blocker. -->

<!-- DEFECT FD-07: The `focus-visible` state is intentionally absent.
     All interactive elements must define focus-visible treatment for keyboard navigation.
     ui-spec-linter should catch this as a Major issue. -->

### Default
- Background: `color.action.primary` (`#2563eb`)
- Text: white
- Border-radius: `radius.md` (6px)
- Padding: 10px 16px

### Hover
- Background: `color.action.primary.hover` (`#1d4ed8`)

### Disabled
- Background: `color.surface.base`
- Text: `color.text.primary` at 40% opacity
- Cursor: `not-allowed`

## Accessibility

- `type="submit"` so it works inside a `<form>`.
- Label text is the accessible name (no separate `aria-label` needed if label prop is descriptive).

## Usage example

```jsx
<PostButton label="Submit post" onClick={handleSubmit} />
```
