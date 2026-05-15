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
- Color cannot be the only visual means of conveying information (for example, add an icon or text to error states).

## Screen Reader Announcements
- Status messages that appear without user interaction (toasts, autosave indicators, validation summaries) must be wrapped in a region with `role="status"` and `aria-live="polite"`.
- Critical errors that interrupt a flow (failed save, session expired) use `role="alert"` (which implies `aria-live="assertive"`).
- Loading regions that replace content use `aria-busy="true"` on the container while the content is being fetched, then `aria-busy="false"` once the content is rendered.
- Dynamic content insertions outside the user's focus path (for example, a new chat message arriving) must announce via an `aria-live` region or be reachable via a clearly labelled landmark.

## Landmark Structure
- Every screen has exactly one `<main>` element.
- Primary navigation uses `<nav aria-label="...">` with a descriptive label when multiple `<nav>` elements exist on the page.
- Page heading hierarchy starts at `<h1>` and does not skip levels.
