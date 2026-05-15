---
spec_type: flow
spec_id: settings-account
created: 2026-05-06
status: draft
---

# Flow: Prosper Settings Page

## 1. Entry points

| From                          | Trigger                              | Lands on                |
|-------------------------------|--------------------------------------|-------------------------|
| Top-right user avatar dropdown| Click "Settings"                     | Profile section (default)|
| Direct URL                    | `/settings`, `/settings/profile`     | Profile section          |
| Direct URL                    | `/settings/notifications`            | Notifications section    |
| Direct URL                    | `/settings/billing`                  | Billing section          |
| Notification email            | Click "Manage notifications" link    | Notifications section    |

## 2. Journey graph

```text
[Entry] ──▶ [Profile] ◀────┐
              │             │
              ├──▶ [Notifications]
              │             │
              └──▶ [Billing] ──▶ [Stripe Customer Portal] (external)
```

All three internal sections are reachable from any other in one click via the sidebar — no nesting, no back stack.

## 3. Per-section flow

### Profile
1. Page loads → fetch profile → render form populated with current values.
2. User edits Display Name and/or Avatar.
3. User clicks **Save changes**.
4. PATCH `/api/users/me`.
   - Success → success toast "Settings updated successfully." → form remains on screen with new values; sidebar avatar/name update immediately.
   - Validation error → inline field error(s); Save button re-enables.
   - Server error → global error banner above the form; Save button re-enables; user can retry.
5. User clicks **Cancel** at any time → form reverts to the last saved values; no network call.

### Notifications
1. Page loads → fetch preferences → render toggle list.
2. User flips a toggle.
3. **Autosave** PATCH `/api/users/me` with the changed preference (debounced 400ms to coalesce rapid toggling).
   - Success → no toast; the toggle's saved-indicator dot appears next to the label for 2s then fades.
   - Failure → toggle reverts to its previous position; inline error text appears next to the label.

### Billing
1. Page loads → fetch subscription → render read-only summary (plan name, renewal date).
2. User clicks **Manage subscription** → opens Stripe Customer Portal in a new tab.
3. User returns to Prosper → on focus, refetch subscription so the displayed values reflect any change made in Stripe.

## 4. State that carries between sections

- **Active section** persists in URL (browser back/forward works).
- **Unsaved Profile edits**: if the user navigates to another section with unsaved changes, show a confirmation dialog ("You have unsaved changes. Discard them?"). Notifications has no unsaved-state because it autosaves.

## 5. Failure paths

| Failure                         | UI response                                                                |
|---------------------------------|----------------------------------------------------------------------------|
| Initial profile fetch fails     | Replace form with retry banner: "Couldn't load your settings. [Retry]"     |
| Initial notifications fetch fails| Same pattern, scoped to the notifications section.                         |
| Initial billing fetch fails     | Same pattern, scoped to the billing section.                                |
| Avatar upload fails             | Inline error below avatar; previous avatar remains in place; allow retry.   |
| Save fails (network)            | Global banner; form values preserved; Save button re-enabled.               |
| Save fails (validation)         | Inline field errors; Save button re-enabled; do not show global banner.     |

## 6. Success path metrics

The brief targets <90s from page load to success toast for the primary Profile update task. The flow above is single-step (load → edit → save), which supports that target.
