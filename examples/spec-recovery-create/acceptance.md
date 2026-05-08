---
spec_type: acceptance
spec_id: pulse-create
created: 2026-05-08
status: draft
recovery: true
---

# Acceptance Criteria: Pulse /create Route (Spec Recovery)

Severity levels: **[B]** Blocker — must pass before release | **[M]** Major — must pass before release | **[m]** Minor — fix in next patch | **[P]** Polish — nice to have

A = Automated test | M = Manual test

---

## Layout and Responsiveness

| ID | Criteria | Sev | Type |
|---|---|---|---|
| L-01 | At 1280px the layout is two columns: form (60%) on the left, preview (40%) on the right, with `space.6` (24px) padding inside each panel. | B | M |
| L-02 | At 768px–1023px the layout remains two columns but resizes to 65/35. | M | M |
| L-03 | Below 768px, a tab bar appears with "Form" and "Preview" tabs. The preview panel is not visible by default. | B | M |
| L-04 | The action bar (Publish now / Schedule… / Save draft) is sticky at the bottom of the form panel on all breakpoints. | B | M |
| L-05 | No horizontal scroll appears at any tested breakpoint (1280px, 768px, 375px). | M | A |

---

## Caption Input

| ID | Criteria | Sev | Type |
|---|---|---|---|
| C-01 | Caption textarea receives keyboard focus immediately on page load. | B | M |
| C-02 | A visible label "Caption" is present above the textarea and programmatically associated via `<label for>`. | B | A |
| C-03 | Character count displays "N characters remaining" and updates on every keystroke. | M | A |
| C-04 | Attempting to publish with an empty caption shows inline error "Add a caption before publishing." below the textarea. | B | M |

---

## Channel Selector

| ID | Criteria | Sev | Type |
|---|---|---|---|
| CH-01 | All channels are rendered as `<button>` elements (not `<div>` with onClick). Each has an accessible name matching the channel name. | B | A |
| CH-02 | Channels are ordered most-used-first (requires open question #2 resolution). ⚠️ | B | M |
| CH-03 | Multiple channels can be selected simultaneously. Selected state is visually distinct (filled background) and communicated via `aria-pressed`. | B | M |
| CH-04 | Attempting to publish with no channel selected shows inline error "Select at least one channel before publishing." | B | M |
| CH-05 | All channels are keyboard-navigable (Tab to reach the group; arrow keys to move between options; Space/Enter to toggle). | B | M |

---

## AI Draft

| ID | Criteria | Sev | Type |
|---|---|---|---|
| A-01 | Clicking "✦ Generate draft" shows a loading state: button label changes to "Generating…", spinner appears, button is disabled, `aria-busy="true"` is set. | B | M |
| A-02 | On success, `AiSuggestionCard` appears with the generated text and "Use this draft" / "Discard" actions. | B | M |
| A-03 | Clicking "Use this draft" replaces the caption textarea content with the AI suggestion. | B | A |
| A-04 | Generation that exceeds the agreed timeout threshold shows error "Couldn't generate a draft. Check your connection and try again." ⚠️ Threshold TBD pending open question #1. | B | M |
| A-05 | An `aria-live="polite"` region announces the AI result ("Draft ready — review and accept or discard" on success; error text on failure). | M | M |

---

## Media Upload

| ID | Criteria | Sev | Type |
|---|---|---|---|
| MU-01 | The media upload dropzone has an accessible name "Attach media (optional)". | B | A |
| MU-02 | Upload progress is visually indicated with a progress bar. | M | M |
| MU-03 | Uploading a file exceeding the size limit shows "This file exceeds [N] MB" (N TBD). ⚠️ | M | M |
| MU-04 | Uploading an unsupported format shows "Pulse supports JPG, PNG, GIF, and MP4. This file format isn't supported." | M | M |

---

## Schedule Modal

| ID | Criteria | Sev | Type |
|---|---|---|---|
| S-01 | Clicking "Schedule…" opens a modal on desktop with `role="dialog"`, `aria-modal="true"`, and focus moves to the first interactive element inside. | B | M |
| S-02 | Pressing Escape closes the modal and returns focus to the Schedule button. | B | M |
| S-03 | On mobile, clicking "Schedule…" opens a full-screen sheet, not a modal. | M | M |
| S-04 | When a scheduling conflict exists, `ScheduleConflictBanner` renders inside the modal with an alternative time suggestion. | M | M |

---

## Publish and Save

| ID | Criteria | Sev | Type |
|---|---|---|---|
| P-01 | Clicking "Publish now" disables both action buttons and shows a spinner on the Publish button during submission. | B | M |
| P-02 | On successful publish, a toast "Post published to [channel names]." appears and the form clears. | B | M |
| P-03 | On publish failure, a toast "Post couldn't be published. Your draft has been saved — try again." appears and the form is preserved. | B | M |
| P-04 | "Save draft" persists the current caption, channels, and media as a draft without publishing. | M | M |

---

## Accessibility (Baseline)

| ID | Criteria | Sev | Type |
|---|---|---|---|
| ACC-01 | All interactive elements are reachable by Tab key. Tab order matches visual reading order (top to bottom, left to right). | B | M |
| ACC-02 | All interactive elements have a visible focus indicator (not removed by `outline: none` without replacement). | B | M |
| ACC-03 | No axe-core critical violations. | B | A |
| ACC-04 | Contrast ratio ≥ 4.5:1 for all body text. Primary action button text on `color.action.primary` background: verified. | B | A |

---

## Success Criteria Traceability

| Brief criterion | Acceptance criteria |
|---|---|
| Create and publish in under 60 seconds (§6) | L-01, L-04, C-01, CH-01–CH-03 (enables fast channel selection), A-02–A-03 |
| AI draft ≤ agreed timeout (§6) | A-01, A-04 |
| WCAG AA — zero critical violations (§6) | ACC-01 through ACC-04, CH-01, CH-05, S-01, S-02 |
