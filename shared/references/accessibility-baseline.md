# Accessibility Baseline

All components and screens must meet this baseline before code generation.

## Forms
- Every input has a visible label or an `aria-label`.
- Error messages are associated with inputs via `aria-describedby`.
- Invalid states use `aria-invalid="true"`.

## Keyboard Navigation
- All interactive elements must be reachable via `Tab`.
- Focus outlines must be visible (`focus-visible`).
- Modals must trap focus.
- Custom dropdowns must support `ArrowUp`, `ArrowDown`, `Enter`, and `Escape`.

## Contrast & Color
- Text contrast must be at least 4.5:1 (WCAG AA).
- Color cannot be the only visual means of conveying information (e.g., add an icon or text to error states).

## TODO (Human Review Required)
- [ ] Incorporate screen reader announcement patterns (e.g., `aria-live` for toasts).
