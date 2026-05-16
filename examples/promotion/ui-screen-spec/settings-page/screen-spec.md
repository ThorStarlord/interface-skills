---
spec_type: screen-spec
spec_id: settings-account
created: 2026-05-06
status: draft
---

# Screen Spec: Prosper Settings Page

This spec covers the Settings page as a whole and the Profile section in detail. The Notifications and Billing sections follow the same chrome with section-specific bodies.

## 1. Component instantiation

| Region          | Component             | Props / data                                                                 |
|-----------------|-----------------------|------------------------------------------------------------------------------|
| App shell       | AppHeader             | (existing global; not in scope)                                              |
| Sidebar         | SettingsSidebar       | activeSection: "profile" \| "notifications" \| "billing", user               |
| Sidebar top     | UserProfileBadge      | avatarUrl, displayName, email                                                |
| Sidebar list    | NavList               | items: [{key, label, href}], activeKey                                       |
| Main panel      | SettingsContent       | switches on route                                                            |
| Profile section | ProfileForm           | initialValues, onSubmit, onCancel                                            |
| Action footer   | FormActions           | onSave, onCancel, isSubmitting, isDirty, disabled                            |

The ProfileForm is the only complex interactive component on this screen. It has its own component spec at component-specs/profile-form.md.

## 2. Component Layout & Region Details

### Component 1: AppHeader
Existing global header, out of scope for custom implementation but must render.

### Component 2: SettingsSidebar
Renders navigation bar with tabs: profile, notifications, billing.

### Component 3: UserProfileBadge
Displays active user's thumbnail avatar and full display name.

### Component 4: ProfileForm
Complex form container for direct edits to primary user metadata.

### Component 5: FormActions
Sticky footer action buttons validating dirty and submitting states.

## 3. State ownership

| State                          | Owner                | Notes                                                                              |
|--------------------------------|----------------------|------------------------------------------------------------------------------------|
| activeSection                  | URL / router         | URL is the source of truth; SettingsSidebar reads it.                              |
| Profile form values            | ProfileForm local    | Initialised from API; reset on Cancel.                                             |
| Profile form dirty flag        | ProfileForm local    | Computed from current values vs. initial values.                                   |
| Submit-in-flight flag          | ProfileForm local    | Disables the form and shows the Save button's pending state.                       |
| Server error message           | ProfileForm local    | Cleared on next submit attempt.                                                    |
| Toast queue                    | Global toast service | Triggered by ProfileForm after a successful save.                                  |
| Notification preferences       | NotificationsSection local | Optimistically updated; reverted on autosave failure.                       |
| Billing data                   | BillingSection local | Refetched on window focus.                                                     |

## 4. State taxonomy (per shared/references/state-taxonomy.md)

The Profile section must implement all of the following states:

| State          | Trigger                                          | Visible UI                                                                        |
|----------------|--------------------------------------------------|------------------------------------------------------------------------------------|
| **Default**    | Form has loaded, values match server state.      | Inputs filled, Save disabled, Cancel disabled.                                     |
| **Loading**    | Initial profile fetch in flight.                 | Skeleton rows in place of each input. Sidebar nav still interactive.               |
| **Empty**      | (Not applicable — every user has a profile.)     | —                                                                                  |
| **Edited**     | Any input value differs from saved.              | Save and Cancel become enabled; Save adopts primary visual treatment.              |
| **Submitting** | Save clicked.                                    | Save button shows spinner + label "Saving…"; entire form is busy and inputs are disabled. |
| **Success**    | PATCH returns 200.                               | Form returns to Default state with new initial values; toast "Settings updated successfully." |
| **Inline error** | PATCH returns 422 with field errors.            | Affected inputs show invalid and an inline error message; Save re-enabled. |
| **Global error** | PATCH returns 5xx or network failure.           | Banner above form: "Something went wrong. Try again." Save re-enabled.             |
| **Initial load failure** | Initial GET fails.                       | Replace form with retry banner: "Couldn't load your settings. Retry"             |

## 5. Keyboard map (page-level)

| Key             | Action                                                                                  |
|-----------------|-----------------------------------------------------------------------------------------|
| Tab             | Cycle through: sidebar nav items → form inputs (in document order) → Cancel → Save.      |
| Shift+Tab       | Reverse of above.                                                                        |
| Enter (within input) | Submit the form (equivalent to clicking Save), if dirty and not submitting.       |
| Escape (within input) | Cancel the edit (equivalent to clicking Cancel), if dirty and not submitting.    |
| Cmd/Ctrl+S      | Submit the form. (Browser default save-as is suppressed only on this page.)              |

Per shared/references/accessibility-baseline.md, every interactive element is reachable via Tab and shows a visible focus ring.

## 6. Cross-section behaviour

- Switching sidebar sections while the Profile form is Edited triggers a confirmation: "You have unsaved changes. Discard them?" with Discard / Stay buttons. Stay is the default-focused button.
- The success toast for Profile save dismisses automatically after 4s; clicking it dismisses immediately.
