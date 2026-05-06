# Acceptance Criteria: Settings Page

## Visual & Layout
- [ ] Layout uses a split panel on desktop and horizontal tabs on mobile.
- [ ] Typography and spacing use the exact tokens from `system.md`.

## Functionality
- [ ] Navigating between Profile, Notifications, and Billing updates the main content without a full page reload.
- [ ] Save button is disabled if no changes have been made.
- [ ] Save button shows a loading spinner during submission.
- [ ] A success toast appears after successful submission.

## Accessibility (a11y)
- [ ] Navigation menu uses appropriate `aria-current="page"` for the active item.
- [ ] Form inputs are properly associated with their labels using `htmlFor` and `id`.
- [ ] Focus is managed correctly when switching tabs.
