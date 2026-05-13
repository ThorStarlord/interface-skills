---
spec_type: acceptance
spec_id: settings-account
based_on:
  - brief-settings-account
  - blueprint-settings-page
  - component-ProfileSettingsForm
  - system-settings-page
created: 2026-05-06
status: draft
---

# Acceptance checklist: Settings Page — Prosper Account Settings

## How to use this checklist

- Each item has a severity: **blocker** (must fix before ship), **major** (should fix before ship), **minor** (fix before next milestone), **polish** (fix when time permits).
- Each item is marked with an explicit automation source: **[A:playwright]**, **[A:axe]**, **[A:lint]**, **[A:unit]**, or **[M]**.
- Where a criterion traces back to a specific spec section, the source is noted in `[source]`.

---

## 1. Layout

| | Severity | Criterion | Source |
|---|---|---|---|
| ☐ | blocker | [M] At ≥768px viewport width, the page renders a split-panel layout: left sidebar fixed at 250px, right content panel fluid up to 800px max-width. | blueprint §Layout Hierarchy |
| ☐ | blocker | [M] The sidebar contains three items in order: User Profile Badge (avatar, name, email), then navigation links for Profile, Notifications, Billing. | blueprint §Layout Hierarchy |
| ☐ | blocker | [M] The main content panel contains: a page title heading, the section content area, and a form actions footer, in that vertical order. | blueprint §Layout Hierarchy |
| ☐ | major | [M] The form actions footer (Save / Cancel) is sticky to the bottom of the viewport when the content area is taller than the visible area. | blueprint §Layout Hierarchy |
| ☐ | major | [A:lint] All spacing values in the layout resolve to the tokens `spacing-sm` (0.5rem), `spacing-md` (1rem), or `spacing-lg` (1.5rem). No inline padding or margin literal values appear. | system §Spacing & Typography |
| ☐ | major | [M] The page title heading uses `font-heading` (Inter, 600 weight, text-2xl). No other font weight or size is used for the heading. | system §Spacing & Typography |
| ☐ | minor | [M] The sidebar User Profile Badge is visible at all times regardless of which section is active. It is not replaced by the section content. | blueprint §Layout Hierarchy |

---

## 2. Responsive

| | Severity | Criterion | Source |
|---|---|---|---|
| ☐ | blocker | [M] At <768px viewport width, the sidebar collapses and the navigation renders as a horizontally scrollable tab menu at the top of the page. The user profile badge is no longer shown in the navigation. | blueprint §Breakpoints |
| ☐ | blocker | [M] At <768px, the main content panel spans the full viewport width below the tab menu. | blueprint §Breakpoints |
| ☐ | major | [A:playwright] No horizontal scroll appears on the page body at 375px viewport width (the smallest common mobile size). | blueprint §Breakpoints |
| ☐ | major | [M] At <768px, all touch targets (tab items, buttons, toggle switches) are at least 44×44px. | accessibility default |
| ☐ | major | [M] The Save and Cancel buttons remain visible and reachable without scrolling past 150% of the viewport height at 375px on the Profile section. | brief §6 success criteria |

---

## 3. States (per component)

### 3.1 TextInput (Display Name field)

| | Severity | Criterion | Source |
|---|---|---|---|
| ☐ | blocker | [M] Default state renders with `border-default` (`#E5E7EB`) border and `bg-surface` (`#FFFFFF`) background. | component-spec §State Matrix |
| ☐ | blocker | [M] Focus state renders with a 2px ring in `action-primary` (`#2563EB`) and no change to border color. | component-spec §State Matrix |
| ☐ | blocker | [A:playwright] Focus-visible state is visible (ring is present) when the field receives focus via keyboard Tab. | component-spec §Accessibility |
| ☐ | blocker | [M] Error state renders with `border-red-500` border and the associated error message is visible below the field. | component-spec §State Matrix |
| ☐ | blocker | [A:unit] Error state: the input has `aria-invalid="true"` set when in error state, and `aria-invalid="false"` or the attribute is absent when valid. | component-spec §Accessibility |
| ☐ | blocker | [M] Disabled state renders with `bg-gray-100` background and `cursor-not-allowed` pointer. The field does not accept input. | component-spec §State Matrix |
| ☐ | major | [A:unit] Disabled state: the input has the native `disabled` attribute set, preventing keyboard focus. | component-spec §State Matrix |

### 3.2 UploadButton (Avatar upload)

| | Severity | Criterion | Source |
|---|---|---|---|
| ☐ | blocker | [M] Default state renders with `text-action-primary` (`#2563EB`) label text. | component-spec §State Matrix |
| ☐ | blocker | [M] Focus state renders with an underline on the button label text. | component-spec §State Matrix |
| ☐ | blocker | [A:playwright] The upload button is a `<button>` element (or has `role="button"`) and is reachable and activatable via Tab + Enter and Tab + Space. | component-spec §Accessibility |
| ☐ | blocker | [M] Disabled state renders with `text-disabled` label text. The button does not respond to click or keyboard activation. | component-spec §State Matrix |
| ☐ | major | [M] After a file is selected, the `ImagePreview` element updates to show the newly selected image before the form is saved. | component-spec §Anatomy |

### 3.3 Save button

| | Severity | Criterion | Source |
|---|---|---|---|
| ☐ | blocker | [M] The Save button is in a disabled state when no field values have changed from the last saved state. | brief §4 secondary actions |
| ☐ | blocker | [M] When the Save button is disabled, it does not respond to click or keyboard Enter. | brief §4 secondary actions |
| ☐ | blocker | [M] During submission, the Save button displays a loading spinner and its label changes to indicate work is in progress. The button does not accept a second click while loading. | brief §4 secondary actions |
| ☐ | blocker | [M] After a successful save, a success toast notification appears confirming the change was applied. The toast is dismissible. | brief §6 success criteria |
| ☐ | major | [M] After a failed save (API error), the Save button returns to its active (non-loading) state and an error message is displayed. The user is not left with a permanently spinning button. | brief §6 success criteria |

### 3.4 Navigation items (sidebar / tab strip)

| | Severity | Criterion | Source |
|---|---|---|---|
| ☐ | blocker | [A:lint] The active navigation item has `aria-current="page"` set. | acceptance original §Accessibility |
| ☐ | blocker | [M] Clicking a navigation item loads the corresponding section content in the main panel without a full page reload. | brief §4 secondary actions |
| ☐ | major | [M] The active navigation item is visually distinct from inactive items (e.g. different background or text weight) so the current section is unambiguous. | blueprint §Layout Hierarchy |

---

## 4. Behavior

| | Severity | Criterion | Source |
|---|---|---|---|
| ☐ | blocker | [M] Pressing Save triggers the form submission exactly once, even if the user clicks the button rapidly in succession. | component-spec §Anatomy |
| ☐ | blocker | [M] Pressing Cancel while unsaved changes exist reverts all fields to their last saved values. The user is not required to reload the page to discard changes. | brief §4 secondary actions |
| ☐ | blocker | [M] After a successful save, the sidebar User Profile Badge updates to reflect the new display name and avatar without requiring a page reload. | brief §6 success criteria |
| ☐ | major | [M] Notification preference toggles reflect the correct current state on page load (i.e. they match the value stored on the server, not a default). | brief §4 secondary actions |
| ☐ | major | [M] Switching between settings sections (Profile → Notifications → Billing) does not discard unsaved changes without warning. Either the unsaved state is preserved across section switches, or the user is warned before the state is lost. | brief §4 secondary actions |
| ☐ | minor | [M] Animations (section transitions, toast entrance) honor the `prefers-reduced-motion` media query — motion collapses to instant when the user has set a reduced-motion preference. | system §(motion — implied by flat surfaces token rule) |

---

## 5. Accessibility

| | Severity | Criterion | Source |
|---|---|---|---|
| ☐ | blocker | [A:playwright] Every interactive element on the page (navigation items, text inputs, upload button, toggles, Save, Cancel) is reachable by Tab in the keyboard-only flow. | brief §2 accessibility considerations |
| ☐ | blocker | [A:playwright] Tab order matches the visual reading order: sidebar navigation top-to-bottom, then main content top-to-bottom, then form footer. | brief §2 accessibility considerations |
| ☐ | blocker | [A:lint] Every form input has a programmatically associated `<label>` element, linked via matching `for`/`id` attributes or by wrapping. | component-spec §Accessibility |
| ☐ | blocker | [A:lint] Error messages are linked to their inputs via `aria-describedby`. | component-spec §Accessibility |
| ☐ | blocker | [A:axe] All text on the page achieves at least 4.5:1 contrast ratio against its background (`text-primary` `#111827` on `bg-surface` `#FFFFFF` passes). `text-secondary` `#6B7280` on `#FFFFFF` must be checked for large-text 3:1 rule where used below 18px. | system §Colors; a11y default |
| ☐ | blocker | [A:lint] The page `<form>` uses a `<form>` element, not a `<div>`, so native form semantics (submit on Enter, fieldset grouping) are available. | component-spec §Accessibility |
| ☐ | major | [M] When focus moves into the main content panel after a navigation section switch, focus is placed on the panel heading or first focusable element in the new section. Focus is not left stranded on a now-hidden element. | brief §4; acceptance original §Accessibility |
| ☐ | major | [A:lint] No element has a `tabindex` value greater than 0. | a11y default |
| ☐ | major | [M] The success toast is announced by screen readers without requiring the user to navigate to it (use `aria-live="polite"` or equivalent). | brief §6 success criteria |
| ☐ | minor | [M] The avatar `ImagePreview` element has a non-empty `alt` attribute describing the current avatar (e.g. the user's display name). | a11y default |

---

## 6. Visual polish

| | Severity | Criterion | Source |
|---|---|---|---|
| ☐ | major | [A:lint] All color values used in the rendered page are present in the system spec token set (`bg-surface`, `bg-surface-hover`, `text-primary`, `text-secondary`, `action-primary`, `action-primary-hover`, `border-default`). No off-system hex values appear in computed styles. | system §Colors |
| ☐ | major | [M] Borders on card/section containers use `border-default` (`#E5E7EB`). No other border color is used on contained surfaces. | visual-calibration §Concrete Visual Decisions |
| ☐ | major | [M] Corner radii on inputs, buttons, and card containers fall within `rounded-md` to `rounded-lg` range. No fully square (`rounded-none`) or fully circular (`rounded-full`) corners appear on rectangular containers. | visual-calibration §Concrete Visual Decisions |
| ☐ | major | [M] Text baselines, input heights, and button heights align to the spacing grid. No element appears vertically offset from its row. | system §Spacing & Typography |
| ☐ | minor | [M] Hover state on `action-primary` elements transitions to `action-primary-hover` (`#1D4ED8`). The transition is visible and not abrupt. | system §Colors |
| ☐ | minor | [M] The sidebar background uses `bg-surface-hover` (`#F9FAFB`) to create a subtle separation from the main content panel (`bg-surface` `#FFFFFF`). | visual-calibration §Surface Style |
| ☐ | polish | [M] Repeated form field groups (Label + Input) appear at consistent vertical intervals — no gap feels larger or smaller than its peers without a deliberate reason (section grouping). | visual-calibration §Density |

---

## 7. Microcopy

| | Severity | Criterion | Source |
|---|---|---|---|
| ☐ | blocker | [M] The Save button label is an action verb tied to the operation — not "Submit" or "OK". The label should communicate what is being saved (e.g. "Save changes" or "Save profile"). | brief §3 primary action |
| ☐ | blocker | [M] The Cancel button label is "Cancel" (not "Back", "Reset", or "Discard") to match the standard SaaS convention for this action. | brief §4 secondary actions |
| ☐ | major | [M] The success toast message confirms what was saved, not just that something succeeded. "Profile updated" is acceptable; "Success!" alone is not. | brief §6 success criteria |
| ☐ | major | [M] Error messages on form validation explain the problem specifically — e.g. "Display name cannot be empty" — not a generic "Invalid input" or "Error". | component-spec §Accessibility |
| ☐ | major | [M] The avatar upload HelperText communicates any constraints (file type, size limit) before the user uploads, not only after failure. | component-spec §Anatomy; brief §9 open question 1 |
| ☐ | minor | [M] The Billing section read-only fields include a visible label indicating they are not editable (e.g. greyed style or a "Managed by your plan" note), so users do not attempt to edit them and wonder why nothing happens. | brief §4 secondary actions |

---

## 8. Performance

| | Severity | Criterion | Source |
|---|---|---|---|
| ☐ | major | [A:playwright] The settings page reaches Largest Contentful Paint in under 2.5 seconds on a simulated 4G connection (Chrome DevTools throttle: "Fast 4G"). | performance default |
| ☐ | major | [A:playwright] Cumulative Layout Shift for the page is below 0.1 (no visible jump when sidebar or form content loads). | performance default |

---

## 9. Items intentionally NOT checked

- **Internationalisation and RTL layout** — the brief explicitly marks i18n out of scope for v1.4 (brief §8 non-goals). All microcopy is English-only.
- **Account deletion flow** — explicitly out of scope per brief §8 non-goals. No acceptance criteria for a "Danger Zone" section.
- **Password change and SSO configuration** — out of scope per brief §8 non-goals. Not present on this page.
- **Billing write operations (plan upgrade, payment method)** — billing section is read-only per brief §8 non-goals. CTA behaviour is an open question (brief §9, question 4) and not tested here until resolved.
- **Print styles** — not specified in any upstream spec.
- **Dark mode / theme switching** — the system spec defines only a light-mode token set. No dark-mode tokens are specified.
- **Avatar upload file-type validation UX** — the exact allowed file types and size limit are an open question (brief §9, question 1). The criterion for HelperText content (§7) is marked as depending on resolution of that question.

## 10. Open questions

1. Should notification preference toggles autosave or require an explicit Save? This determines whether the Save/Cancel footer appears on the Notifications section at all (brief §9, question 2).
2. Is there a character limit on the display name field? If yes, should an inline character counter appear in the TextInput? (brief §9, question 3)
3. Should the Billing section include any upgrade CTA? If yes, acceptance criteria for that CTA (states, microcopy, disabled behaviour) will need to be added in a follow-up. (brief §9, question 4)
4. Is the success toast the correct pattern for confirming saves, or should the brief's "immediately visible in the sidebar" criterion (brief §6) be the sole confirmation? Clarify so both criteria are not in conflict.
