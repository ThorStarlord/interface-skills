---
spec_type: component
spec_id: kanban-card
based_on: 05-screen-spec.md
created: 2026-05-10
status: draft
source_evidence:
  - 05-screen-spec.md
  - 04-blueprint.md
  - 03-visual-calibration.md
  - saas_frontend/src/components/kanban/KanbanCard.tsx
---

# Component Spec: KanbanCard

## 1. Context
- Lives on screen(s): /kanban board view (desktop), /kanban review/deck view (mobile fallback interactions)
- Role: Primary decision object for approval queue; each card is a single actionable post suggestion
- Data it consumes: One row of content_calendar (ContentCalendarRow) plus board context (column status, selection, drag state)

## 2. Anatomy

```text
KanbanCard
├── CardContainer (required)
│   ├── ThumbnailRegion (required)
│   │   ├── MediaContent (optional if media missing)
│   │   ├── MediaPlaceholder (fallback)
│   │   └── FormatBadge (required overlay)
│   ├── ContentRegion (required)
│   │   ├── Title (required, clamped)
│   │   ├── Description (optional, clamped)
│   │   └── StatusBadge (required)
│   ├── QuickActions (required)
│   │   ├── ApproveButton
│   │   ├── RejectButton
│   │   └── MoreMenuButton
│   └── ErrorBanner (conditional)
│       ├── WarningBadge
│       └── RetryButton
└── LoadingSkeleton (conditional replacement)
```

Part rules:
- CardContainer: Drag source on desktop; tap target on mobile.
- ThumbnailRegion: Fixed 4:3 ratio with rounded corners; always rendered.
- MediaContent: Image/video preview when URLs are valid.
- MediaPlaceholder: Rendered when media_url missing/failed.
- FormatBadge: Top-right overlay with format label (Carrossel, Reel, Post, Stories).
- ContentRegion: Textual summary with strict clamp limits.
- QuickActions: Fast approve/reject/menu actions; shown on hover/focus desktop and always visible on mobile.
- ErrorBanner: Replaces standard quick actions in recoverable error paths.
- LoadingSkeleton: Full card skeleton while awaiting hydrated data.

## 3. Props / Content Slots

### 3.1 Type Definitions

```ts
export type KanbanStatus = 'backlog' | 'review' | 'approved' | 'published';

export interface ContentCalendarRow {
  id: string;
  title: string | null;
  description: string | null;
  final_copy: string | null;
  final_hashtags: string[] | null;
  media_url: string | null;
  media_type: 'image' | 'video' | null;
  post_format: 'carousel' | 'reel' | 'post' | 'stories' | null;
  kanban_status: KanbanStatus;
  automation_tier: 'draft' | 'manual' | 'full_auto' | null;
  scheduled_date: string | null;
  last_error: string | null;
}

export interface KanbanCardProps {
  post: ContentCalendarRow;
  columnStatus: KanbanStatus;
  isSelected: boolean;
  isDragging: boolean;
  onApprove: (postId: string) => void;
  onReject: (postId: string) => void;
  onMoreClick: (postId: string, anchorEl: HTMLElement) => void;
  onThumbnailClick: (postId: string) => void;

  // Optional control props for non-happy paths
  isLoading?: boolean;
  isError?: boolean;
  errorMessage?: string | null;
  onRetry?: (postId: string) => void;
  isDisabled?: boolean;
}
```

### 3.2 Props Table

| Prop | Type | Required | Default | Purpose |
|---|---|---|---|---|
| post | ContentCalendarRow | yes | - | Card data source from content_calendar row |
| columnStatus | KanbanStatus | yes | - | Current board column context for behavior variants |
| isSelected | boolean | yes | false | Highlights card when details modal is open |
| isDragging | boolean | yes | false | Applies drag visual state during desktop DnD |
| onApprove | (postId: string) => void | yes | - | Approve action callback |
| onReject | (postId: string) => void | yes | - | Reject action callback (back to backlog) |
| onMoreClick | (postId: string, anchorEl: HTMLElement) => void | yes | - | Opens More menu anchored to icon button |
| onThumbnailClick | (postId: string) => void | yes | - | Opens detail modal from image or card tap |
| isLoading | boolean | no | false | Replaces card content with loading skeleton |
| isError | boolean | no | false | Forces visual error state when true |
| errorMessage | string \| null | no | null | User-facing recoverable error message |
| onRetry | (postId: string) => void | no | undefined | Retry action for failed mutations |
| isDisabled | boolean | no | false | Blocks interactions while preserving readability |

## 4. Content Contract

### 4.1 Field Mapping from content_calendar

| UI field | Source field(s) | Mapping rule |
|---|---|---|
| Card title | post.title, post.final_copy | Use post.title when present; fallback to first 70 chars of final_copy; fallback to 'Sem título' |
| Card description | post.description, post.final_copy | Use post.description when present; fallback to first sentence of final_copy |
| Thumbnail media | post.media_url, post.media_type | Render media_url if valid; otherwise placeholder by format |
| Format badge | post.post_format | carousel -> Carrossel, reel -> Reel, post -> Post, stories -> Stories |
| Status badge | post.kanban_status | Map enum to PT-BR display labels from CONTENT-JOURNEY-UX-CONTRACT |
| Error banner | post.last_error, isError, errorMessage | Prefer explicit errorMessage; else last_error summary |

### 4.2 Clamp Rules
- Title: max 2 lines (`line-clamp-2`), ellipsis overflow.
- Description: max 1 line (`line-clamp-1`), ellipsis overflow.
- Badge labels: single line, no truncation; shrink font before clipping.

## 5. State Matrix

| State | Visual | Behavior | Trigger |
|---|---|---|---|
| Rest | Neutral card surface, border-default, thumbnail visible | Standard click/tap/drag handlers active | Initial render |
| Hover | Shadow lift + scale 1.01, action row emphasis | Quick actions appear on desktop | Pointer enters card |
| Focus | Visible 2px focus ring (high contrast), action row visible | Space/Enter opens modal; tab can reach action buttons | Keyboard focus on card root |
| Focus-visible | Same as focus; no hover dependency | Same as focus | Keyboard-driven focus |
| Active/Pressed | Brief press scale 0.99, stronger border | Fires click action on release | Pointer/touch press |
| Dragging | Elevated shadow, opacity 0.72, scale 1.04 | Pointer drag controls reorder/column move | Drag start |
| Selected | Border highlight (`primary`), subtle tint, menu suppressed | Indicates modal-linked selection | isSelected = true |
| Loading | Skeleton blocks + shimmer, no content text | All actions disabled | isLoading = true |
| Error | Red-tinted border/background, warning badge, retry CTA | Approve/reject replaced by retry flow | isError true or post.last_error present |
| Disabled | Muted colors and reduced opacity | Ignore approve/reject/menu/drag events | isDisabled = true |
| Success (transient) | Green flash + check micro-badge (120ms) | Transitions to exit state immediately after approve/reject success | Mutation resolve |
| Exit (column move) | Fade + slide-down | Card unmounts from current column | Status change to other column |

## 6. Behavioral Specification

### 6.1 Interaction Rules by Form Factor
- Mobile:
  - Tap card or thumbnail opens PostDetailModal via onThumbnailClick.
  - Swipe right requests approve; swipe left requests reject.
  - If swipe confidence below threshold, snap back to rest.
- Desktop:
  - Drag handle or card drag area starts DnD reorder/column transfer.
  - Click thumbnail or press Space/Enter opens details.
  - More menu button opens options menu.

### 6.2 More Menu Contract
- Trigger: three-dots button in quick actions row.
- Menu items (exact order):
  1. Editar
  2. Regenerar
  3. Deletar
- Keyboard:
  - Enter or Space opens menu.
  - Arrow up/down navigates options.
  - Escape closes menu and restores focus to trigger.

### 6.3 Keyboard Fallback for Drag
- Up/Down arrows: reorder within same column.
- Left/Right arrows: move card between adjacent columns when permitted.
- Space:
  - First press enters "grabbed" mode (`aria-grabbed=true`).
  - Second press drops card in focused location.

## 7. Animation Contract

| Animation | Timing | Curve | Notes |
|---|---|---|---|
| Entrance (staggered) | 220ms | ease-out cubic-bezier(0.25, 0.46, 0.45, 0.94) | Fade-in + slide-up; stagger from list container |
| Hover lift | 100ms | ease-out | Scale 1.01 + shadow increase |
| Drag lift | 150ms | ease-in-out | Scale 1.04 + shadow boost + opacity drop |
| Press feedback | 70ms | ease-out | Scale down to 0.99 |
| Exit to new column | 150ms | ease-in | Fade + slide-down |
| Error pulse | 180ms (2 pulses max) | ease-in-out | Warning badge pulse only; no infinite pulse |

Reduced-motion requirement:
- If prefers-reduced-motion is enabled, disable scale/translate animations and keep only instant opacity transitions.

## 8. Accessibility Requirements

### 8.1 Semantics and Roles
- Card root must be keyboard-focusable (`tabindex=0`) and expose a descriptive label:
  - `aria-label="Post: <resolved title>, status <display status>"`
- Drag-enabled card uses `aria-roledescription="draggable card"`.
- More menu trigger is a button with `aria-haspopup="menu"` and `aria-expanded`.

### 8.2 Keyboard Map

| Key | Action |
|---|---|
| Tab / Shift+Tab | Navigate between card root and inner controls |
| Enter | Open details modal when card root focused |
| Space | Open details modal; in drag mode toggles grab/drop |
| Arrow keys | Reorder/move card in keyboard drag fallback |
| Escape | Exit keyboard drag mode or close menu |

### 8.3 Screen Reader Rules
- On status move, announce via polite live region:
  - "Post movido para <status label>."
- On error state, announce assertively once:
  - "Falha ao atualizar post. Tente novamente."
- Thumbnail button should include post context in label:
  - `aria-label="Abrir detalhes do post <title>"`

### 8.4 Contrast and Targets
- Minimum text contrast: 4.5:1.
- Icon-only controls must have visible focus ring and 44x44 px tap target.

## 9. State Machine

### 9.1 Interaction State Machine

```text
Rest
  -> Hover (pointer enter)
  -> Focused (tab focus)
  -> Pressed (pointer down)
  -> Dragging (drag start desktop)
  -> Loading (isLoading true)
  -> Error (isError true or last_error detected)

Hover
  -> Rest (pointer leave)
  -> Pressed (pointer down)
  -> Dragging (drag start)

Focused
  -> Rest (blur)
  -> ModalOpen (Enter/Space)
  -> KeyboardDragging (Space on drag handle mode)

Pressed
  -> ModalOpen (click release on card/thumbnail)
  -> MenuOpen (click release on more button)
  -> Rest (cancel)

Dragging
  -> Rest (drop same column)
  -> ExitAnimating (drop other column)
  -> Error (drop mutation fails)

KeyboardDragging
  -> Focused (Space drop)
  -> ExitAnimating (arrow move across columns + drop)
  -> Error (mutation fails)

MenuOpen
  -> Rest (menu close)
  -> Loading (menu action triggers async op)

Loading
  -> ExitAnimating (success with status move)
  -> Rest (success without move)
  -> Error (failure)

Error
  -> Loading (retry)
  -> Rest (dismiss error)

ExitAnimating
  -> Unmounted (card leaves source column)
```

### 9.2 Selection/Modal Link State Machine

```text
Unselected
  -> Selected (onThumbnailClick or card open)

Selected
  -> Unselected (modal close)
  -> Selected (data refresh while modal open)
```

## 10. Dependencies

### 10.1 Component Dependencies
- Button component (primary, destructive, icon variants)
- Badge component for status/format/warning chips
- DropdownMenu component for More menu
- Skeleton component for loading state
- Motion system (Framer Motion or equivalent)

### 10.2 Data/Contract Dependencies
- content_calendar required fields:
  - id, title, description, final_copy, media_url, media_type, post_format, kanban_status, automation_tier, scheduled_date, last_error
- Label map dependency:
  - Must map enum values to PT-BR display labels (never render raw enum strings)

## 11. Edge Cases

| Edge case | Expected behavior |
|---|---|
| Empty title and empty final_copy | Show fallback title "Sem título" and keep card operable |
| Missing media_url | Render placeholder with format icon + neutral background |
| Invalid/404 media URL | Fallback to placeholder and show non-blocking warning badge |
| Failed regenerate from More menu | Keep card in place, show toast error, preserve menu close behavior |
| Network timeout on approve/reject | Move to Error state with retry button and timeout message |
| Duplicate rapid taps on approve | Debounce action and keep single in-flight request |
| Drag while isDisabled | Prevent drag start, keep muted visual state |
| Keyboard drag across hidden published column | Skip hidden column target and announce next valid target |

## 12. Open Questions
1. Should swipe gestures be active on all mobile columns or only in review/deck mode?
2. On "Regenerar", should card keep same id with updated content or be replaced by a new row id?
3. If modal is open and card receives realtime update, should selected highlight animate or remain static?
