---
spec_type: screen-spec
spec_id: pulse-create
created: 2026-05-08
status: draft
recovery: true
---

# Screen Spec: Pulse /create Route (Spec Recovery)

> **Status: draft** — pending resolution of open questions #1 (AI timeout), #2 (channel ordering), and #3 (unified responsive layout). These three items must be closed before this file can be promoted to approved.

---

## 1. Scope

Route: `/create`  
Single screen owning the full post-creation action. Covers caption authoring, channel selection, media attachment, AI draft generation, and publish/schedule actions.

---

## 2. Regions

| Region | Component | Data dependency | Owner |
|---|---|---|---|
| Page heading | Static `<h1>` | None | Layout |
| Channel Selector | `ChannelPicker` | `GET /api/workspace/channels` | Server — loaded on route entry |
| Caption Input | `CaptionInput` | Controlled local state; synced to post draft | Client |
| AI Draft Panel | `AiDraftButton` + `AiSuggestionCard` | `POST /api/ai/draft` | Server — on-demand |
| Media Uploader | `MediaDropzone` + `MediaThumbnail` | `POST /api/upload/signed-url`, object storage | Server — on-demand |
| Post Preview | `PostPreviewCard` | Derived from caption + channel selection + media | Client (derived) |
| Action Bar | Publish button, Schedule button, Save draft link | `POST /api/posts`, `POST /api/posts/schedule` | Server — on submit |
| Schedule Modal | `DateTimePicker` + `ScheduleConflictBanner` | `GET /api/queue/conflicts?datetime=...` | Server — on-demand |

---

## 3. State Ownership

| State | Location | Notes |
|---|---|---|
| Post draft (caption, channels, media) | React local state | Not persisted until "Save draft" or publish action |
| Channel list | React Query cache | Fetched on route entry; stale time 5 minutes |
| AI generation status | Local state on `AiDraftButton` | `idle \| generating \| success \| error \| rate-limited` |
| Upload progress | Local state on `MediaDropzone` | `idle \| uploading \| success \| error` |
| Schedule modal open/closed | Local state on Action Bar | — |
| Schedule conflict | Server response | `GET /api/queue/conflicts` |

---

## 4. Route Entry Behaviour

- **Authenticated:** Load channel list. Caption textarea receives focus. Post preview starts empty.
- **Unauthenticated:** Redirect to `/login?next=/create`.
- **Deep link with `?draft=<id>`:** Load existing draft by ID into the form. Caption, channels, and media pre-populated from draft data.

---

## 5. Key Interaction Flows

### 5.1 Publish now
1. User types caption; selects ≥ 1 channel.
2. (Optional) clicks "Generate AI draft" — caption is replaced with suggestion on accept.
3. (Optional) attaches media.
4. Clicks "Publish".
5. Action bar enters `submitting` state (buttons disabled, spinner on Publish).
6. On success: `POST /api/posts` returns 201; toast "Post published" appears; form clears.
7. On error: toast "Failed to publish — try again" appears; form state preserved.

### 5.2 Schedule
1. User clicks "Schedule ▾".
2. `ScheduleModal` opens (desktop: modal; mobile: full-screen sheet).
3. User selects date/time. Conflict check fires on date change.
4. If conflict: `ScheduleConflictBanner` renders within the modal with alternative time suggestion.
5. User confirms. Modal closes. Action bar shows "Scheduled for [date]".
6. Publish button label changes to "Confirm schedule".
7. User clicks "Confirm schedule" — same submit flow as 5.1.

### 5.3 AI draft
1. User clicks "Generate AI draft".
2. Button enters `generating` state: spinner, `aria-busy="true"`, label "Generating…".
3. On success (≤ [OPEN: agreed timeout] seconds): `AiSuggestionCard` appears below caption input with suggested text. Two actions: "Use this" (replaces caption) and "Discard".
4. On timeout/error: Button returns to idle; inline error message "Couldn't generate a draft — try again."
5. On rate-limit: Same as error with additional copy "You've reached the daily limit."

---

## 6. Component Map

| Region | Target component | Notes |
|---|---|---|
| Channel Selector | New: `ChannelPicker` (replaces raw div-soup `.channel-badge`) | Must be keyboard-navigable; see accessibility below |
| Caption | Refactor: `CaptionInput` (consolidate 3 implementations into 1) | — |
| AI Draft | `AiDraftButton` + `AiSuggestionCard` | Existing; add proper ARIA live region |
| Media | `MediaDropzone` + `MediaThumbnail` | Existing; fix accessible name of hidden input |
| Preview | `PostPreviewCard` | Existing |
| Schedule Modal | Refactor: `ScheduleModal` (add `role="dialog"`, focus trap) | — |

---

## 7. Accessibility Requirements

- All interactive elements keyboard-reachable via Tab.
- Channel selector: `role="group"`, individual channel options as `<button>` elements (not divs).
- Schedule modal: `role="dialog"`, `aria-modal="true"`, focus trapped inside modal when open, returns focus to Schedule button on close.
- AI draft button: `aria-live="polite"` region announces generation result to screen readers.
- Character count in caption: `aria-label="Caption, [N] characters"` updated as user types.
- Error states: inline error text associated with field via `aria-describedby`.

---

## 8. Open Items (blocking approval)

1. AI timeout threshold — see `brief.md §9 #1`. Until confirmed, the interaction flow in §5.3 uses a placeholder.
2. Channel ordering — see `brief.md §9 #2`. The `ChannelPicker` component spec cannot be finalised until ordering logic is confirmed.
3. Unified mobile layout — see `brief.md §9 #3`. Until the `MobileCreateRedirect` removal is approved by engineering, the mobile layout in `blueprint.md §3` is aspirational.
