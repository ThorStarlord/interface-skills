---
spec_type: component
spec_id: post-detail-modal
based_on: kanban-approval-screen
created: 2026-05-10
status: draft
source_evidence:
  - 05-screen-spec.md
  - 04-blueprint.md
  - 03-visual-calibration.md
  - saas_frontend/src/components/kanban/PostDetailModal.tsx
---

# Component Spec: PostDetailModal

## 1. Context
- Lives on screen(s): /kanban, opened from KanbanCard interactions.
- Role: Full-detail review and edit surface for a single post, without leaving approval journey.
- Data it consumes: Selected content_calendar row + validation + mutation state.

## 2. Anatomy

```text
PostDetailModal
├── OverlayBackdrop (required)
├── DialogContainer (required)
│   ├── HeaderRegion (required)
│   │   ├── CloseButton
│   │   ├── OptionalBreadcrumb
│   │   └── Title: "Detalhes do post"
│   ├── BodyRegion (required)
│   │   ├── PreviewRegion (required)
│   │   │   └── PhoneMockupPreview
│   │   │       ├── MediaPreview
│   │   │       ├── CaptionPreview
│   │   │       ├── HashtagPreview
│   │   │       └── FormatChrome (carousel dots/story timer/etc.)
│   │   └── EditRegion (required)
│   │       ├── TitleField
│   │       ├── CaptionField
│   │       ├── HashtagsField
│   │       ├── FormatSelector
│   │       └── ScheduledDateTimeField
│   ├── ValidationRegion (conditional inline + helper text)
│   └── ActionRegion (required)
│       ├── ApproveButton (primary)
│       ├── RejectButton (secondary)
│       ├── RegenerateButton (tertiary)
│       └── EditInCreateButton (optional)
└── LoadingSkeleton (conditional replacement)
```

## 3. Props / Content Slots

### 3.1 Type Definitions

```ts
export type KanbanStatus = 'backlog' | 'review' | 'approved' | 'published';
export type AutomationTier = 'draft' | 'manual' | 'full_auto';

export interface ContentCalendarRow {
  id: string;
  title: string | null;
  final_copy: string | null;
  final_hashtags: string[] | null;
  media_url: string | null;
  media_type: 'image' | 'video' | null;
  post_format: 'carousel' | 'reel' | 'post' | 'stories' | null;
  kanban_status: KanbanStatus;
  automation_tier: AutomationTier | null;
  scheduled_date: string | null;
  last_error: string | null;
}

export interface PostDetailModalProps {
  isOpen: boolean;
  post: ContentCalendarRow | null;
  mode: 'view' | 'edit';
  isLoading?: boolean;
  isSubmitting?: boolean;
  errorMessage?: string | null;

  onClose: () => void;
  onApprove: (postId: string, payload?: Partial<ContentCalendarRow>) => Promise<void>;
  onReject: (postId: string) => Promise<void>;
  onRegenerate: (postId: string) => Promise<void>;
  onEditInCreate?: (postId: string) => void;
  onSaveDraft?: (payload: Partial<ContentCalendarRow>) => Promise<void>;

  hasUnsavedChanges?: boolean;
  validationErrors?: Record<string, string>;
  initialFocusRef?: React.RefObject<HTMLElement>;
}
```

### 3.2 Props Table

| Prop | Type | Required | Default | Purpose |
|---|---|---|---|---|
| isOpen | boolean | yes | false | Controls modal visibility |
| post | ContentCalendarRow \| null | yes | null | Selected post data |
| mode | 'view' \| 'edit' | yes | 'view' | Enables read-only vs editable UI |
| isLoading | boolean | no | false | Shows modal skeleton while post is loading |
| isSubmitting | boolean | no | false | Disables actions and shows saving feedback |
| errorMessage | string \| null | no | null | Displays recoverable submission/load error |
| onClose | () => void | yes | - | Requests modal close |
| onApprove | (postId, payload?) => Promise<void> | yes | - | Approve action (and optional edited payload) |
| onReject | (postId) => Promise<void> | yes | - | Reject action back to backlog |
| onRegenerate | (postId) => Promise<void> | yes | - | Requests fresh AI suggestion |
| onEditInCreate | (postId) => void | no | undefined | Opens /create with current post context |
| onSaveDraft | (payload) => Promise<void> | no | undefined | Optional save-in-place action for edit mode |
| hasUnsavedChanges | boolean | no | false | Triggers close confirmation |
| validationErrors | Record<string, string> | no | {} | Per-field validation feedback |
| initialFocusRef | RefObject<HTMLElement> | no | close button ref | Focus target when modal opens |

## 4. Layout and Responsive Contract

### 4.1 Desktop
- Modal is centered fixed overlay, max width 600px, max height 90vh.
- Two-column body:
  - Left: Preview region (sticky during edit panel scroll).
  - Right: Edit region with scrollable form.

### 4.2 Mobile
- Full-screen modal (`100vw x 100vh`), no exposed page background.
- Vertical stack:
  - Header (fixed top)
  - Preview (full width)
  - Edit fields
  - Action bar (sticky bottom, primary full width)

## 5. State Matrix

| State | Visual | Behavior | Trigger |
|---|---|---|---|
| Closed | Hidden overlay and dialog | No focus trap active | isOpen = false |
| Loading skeleton | Placeholder blocks in header/body/actions | Actions disabled | isOpen true + isLoading true |
| View-only | Fields rendered as read-only text/display controls | Approve/reject/regenerate active, no field edits | mode = 'view' |
| Edit mode | Inputs enabled, helper text and validation slots visible | Field updates local form state | mode = 'edit' |
| Submitting | Button spinners, dimmed content, "Salvando..." label | All destructive/close controls disabled except guarded cancel | isSubmitting = true |
| Error | Inline field errors + toast + error highlight | Retry allowed; failed fields focused | errorMessage or validationErrors present |
| Unsaved confirm pending | Confirmation dialog overlay above modal | User must confirm discard or continue editing | Close attempt with hasUnsavedChanges true |
| Success (transient) | Optional success toast + clean state | Either closes modal or returns to view mode | Mutation resolves |

## 6. Behavioral Specification

### 6.1 Open and Close Rules
- Open:
  - Triggered by card tap/click.
  - Focus moves to close button (or initialFocusRef).
- Close:
  - Escape closes only if hasUnsavedChanges is false and isSubmitting is false.
  - Backdrop click closes only under same condition.
  - If hasUnsavedChanges is true, show discard confirmation dialog.

### 6.2 Edit and Validation Rules
- Editable fields in edit mode:
  - Title (required, max 120 chars)
  - Caption (required, max 2200 chars)
  - Hashtags (optional, normalized list)
  - Format choice (required)
  - Scheduled date/time (required for approved/manual flows)
- Validation timing:
  - On blur for individual fields.
  - On submit for full form.
- Field error rendering:
  - Red border + inline red helper text under field.

### 6.3 Action Semantics
- Aprovar:
  - Saves edits (if any) and approves post.
  - If automation_tier = full_auto, transition intent is "approved and publish pipeline eligible".
  - If manual/draft, set approved without immediate publish expectation.
- Não quero este:
  - Moves post to backlog and closes modal by default.
- Regenerar:
  - Requests a fresh suggestion.
  - Keeps modal open with loading/submitting indicator until response.
- Editar no criar (optional):
  - Navigate to /create with selected post id/date context.

### 6.4 Sticky Preview Behavior
- Desktop preview panel remains sticky while edit form scrolls.
- Mobile preview remains in document flow, but should remain fully visible before first field.

## 7. Animation Contract

| Animation | Timing | Curve | Notes |
|---|---|---|---|
| Overlay fade-in | 140ms | ease-out | Backdrop opacity 0 -> 1 |
| Dialog entrance | 220ms | cubic-bezier(0.25, 0.46, 0.45, 0.94) | Fade + scale 0.98 -> 1 + slight y-up |
| Section stagger (body) | 120ms each | ease-out | Preview then form then action bar |
| Mode switch (view <-> edit) | 150ms | ease-in-out | Cross-fade editable controls |
| Submit loading spinner | continuous | linear | Respect reduced motion by replacing with static indicator |
| Dialog exit | 150ms | ease-in | Fade + slide-down |

Reduced-motion requirement:
- If prefers-reduced-motion is enabled, disable scale/slide transitions and keep simple opacity toggles.

## 8. Accessibility Requirements

### 8.1 Semantic Structure
- Root dialog container:
  - `role="dialog"`
  - `aria-modal="true"`
  - `aria-labelledby` points to header title id
  - `aria-describedby` points to optional summary/validation region
- Edit region must use semantic `<form>` for editable fields.

### 8.2 Focus Management
- Trap focus within modal while open.
- Initial focus on close button or supplied initialFocusRef.
- Restore focus to invoking card trigger on close.
- Confirmation dialog (unsaved changes) creates nested focus trap and returns focus correctly.

### 8.3 Labels and ARIA
- Every editable field has visible `<label for>` association.
- Icon-only buttons require explicit aria-label (close, regenerate where icon-only variant exists).
- Validation errors must be associated via `aria-describedby`.
- Status updates (submit success/error) announced in polite live region.

### 8.4 Keyboard Map

| Key | Action |
|---|---|
| Tab / Shift+Tab | Navigate through interactive controls inside modal |
| Enter | Submit when focused on primary action or form submit intent |
| Escape | Close modal if safe (no unsaved changes and not submitting) |
| Arrow keys | Navigate format segmented control/date picker where applicable |

### 8.5 Contrast and Target Size
- Minimum contrast ratio 4.5:1 for all text.
- All actionable controls minimum touch target 44x44 px.

## 9. State Machines

### 9.1 Modal Lifecycle State Machine

```text
Closed
  -> Loading (open with pending data)
  -> ViewOnly (open with resolved data and mode=view)
  -> EditMode (open with resolved data and mode=edit)

Loading
  -> ViewOnly (data loaded, mode=view)
  -> EditMode (data loaded, mode=edit)
  -> Error (load failed)
  -> Closed (user closes and safe to dismiss)

ViewOnly
  -> EditMode (user toggles edit)
  -> Submitting (approve/reject/regenerate)
  -> ConfirmDiscard (close intent with unsaved changes true)
  -> Closed (close intent with unsaved changes false)

EditMode
  -> ViewOnly (cancel edit, no unsaved changes)
  -> Submitting (approve/save/regenerate)
  -> ConfirmDiscard (close attempt with unsaved changes)
  -> Error (validation or submit error)

Submitting
  -> ViewOnly (submit success, keep modal open)
  -> Closed (submit success with close-on-success)
  -> Error (submit failure)

Error
  -> Submitting (retry)
  -> EditMode (user fixes field errors)
  -> ViewOnly (dismiss non-field error)

ConfirmDiscard
  -> Closed (confirm discard)
  -> EditMode (cancel discard)
```

### 9.2 Approval Outcome State Machine

```text
ApproveRequested
  -> ApprovedManual (automation_tier = manual or draft)
  -> ApprovedAutoPublishEligible (automation_tier = full_auto)
  -> ApprovalError (mutation failed)
```

Notes:
- ApprovedAutoPublishEligible means UI marks approved and downstream publish workflow should run; modal does not directly publish.

## 10. Dependencies

### 10.1 Component Dependencies
- Modal/Dialog primitive with focus trap and portal support
- Button component variants (primary/outline/ghost)
- Input, Textarea, Select, DateTime picker components
- Toast/notification system
- PhoneMockup preview component with format chrome variants
- ConfirmationDialog component for unsaved changes

### 10.2 Data Dependencies
- content_calendar fields required:
  - id, title, final_copy, final_hashtags, media_url, media_type, post_format, kanban_status, automation_tier, scheduled_date, last_error
- Route/navigation dependency:
  - /create supports contextual deep-link (post id/date)

## 11. Edge Cases

| Edge case | Expected behavior |
|---|---|
| post is null while isOpen true | Show loading skeleton; block actions until data resolves |
| Empty title | Show fallback "Sem título" in preview and require title in edit mode |
| No media | Render preview placeholder preserving Instagram frame layout |
| Failed regenerate | Keep modal open, show error toast and retry button |
| Network timeout on approve | Enter Error state, preserve unsaved data, allow retry |
| Escape pressed during submit | Ignore close request and announce "Salvando, aguarde" |
| Close with unsaved changes | Always open confirm dialog before dismissing modal |
| Validation error in date/time | Focus invalid field and announce error text |
| full_auto approval but publish pipeline unavailable | Show non-blocking warning toast: approved now, publish pending |

## 12. Open Questions
1. Should "Editar no criar" preserve unsaved edits in navigation payload or force save before leaving?
2. In view-only mode, can reject/regenerate still run, or should edit permission gate all actions?
3. For full_auto approvals, should modal remain open for optimistic publish status feedback or close immediately?
