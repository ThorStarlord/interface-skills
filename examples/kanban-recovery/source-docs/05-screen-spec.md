---
spec_type: screen-spec
spec_id: kanban-approval-screen
created: 2026-05-10
status: current
source_evidence:
  - 02-brief.md (goal, primary/secondary actions, success criteria)
  - 03-visual-calibration.md (layout archetype, density, shape, elevation)
  - 04-blueprint.md (information hierarchy, responsive behavior, text wireframe)
  - saas_frontend/src/pages/KanbanPage.tsx (actual component structure)
  - saas_frontend/src/components/kanban/ (KanbanCard, PostDetailModal, ProactiveCardStack)
---

# Screen Spec: Kanban Approval Queue (`/kanban`)

This document specifies the implementation contract for the Kanban approval surface, which is the clearing house where low-tech business owners make binary decisions: approve a post for publication, or send it back to the backlog for reconsideration.

---

## A. Region Mapping

### Zone 1: Hero Header (`KanbanHeader`)
**Purpose:** Establish page identity and provide access to mode switching

**Visual:** Full-width banner, `hero-surface` semantic color, `rounded-[1.75rem]`, `p-4 md:p-5`

**Regions:**
- **Left side (flex: 1):**
  - **Kicker badge:** "👀 Aprovar posts" (hero-kicker class, icon + label)
  - **Page title (h2):** "Decida o que vai para a agenda" (text-2xl font-black tracking-tight)
  - **Subtitle (p):** Context hint — changes based on viewMode
    - Board mode: "Use o quadro completo para revisar ideias e agendar publicações em massa."
    - Review mode: "Use este modo para aprovar uma ideia por vez, sem se perder no restante do painel."
  - **Data deps:** `viewMode`, `projectName` (not rendered, but informs copy)

- **Right side (flex row, self-start sm:self-center):**
  - **View mode toggle (ButtonGroup):**
    - "Quadro completo" button (LayoutDashboard icon) → `setViewMode('board')`
    - "Decidir uma a uma" button (Library icon) → `setViewMode('review')`
    - **Visual:** Flex row, gap-1, `bg-muted/50 p-1 rounded-xl border border-border/50`
    - **Badge:** Review button shows `reviewDeck.badgeCount` if > 0 (e.g., "20+")
  - **Hide published toggle:** Eye icon ± strikethrough
    - Text: "Mostrar publicados" or "Ocultar publicados"
    - Icon opacity: full when showing, 50% when hidden
    - Action: `setHidePublished(!hidePublished)`
  - **Data deps:** `viewMode`, `hidePublished`, `reviewDeck.badgeCount`, `reviewDeck.source`

---

### Zone 2: Pipeline Stepper (`PipelineStepper`)
**Purpose:** Orient user through 4-stage workflow (backlog → review → approved → published)

**Visual:** Horizontal flex row, gap-1, `mb-4`, `px-1`, persistent across board and review modes

**Regions:**
- **4 step indicators (one per status):**
  - Status: backlog, review, approved, published
  - Label: "Ideias salvas", "Para decidir", "Agendados", "Publicados"
  - **Dot indicator:** w-2 h-2 rounded-full
    - **Active (current stage):** bg-primary, scale-125
    - **Past stages:** bg-primary/40
    - **Future stages:** bg-border
  - **Label text:** text-[9px] font-bold uppercase tracking-wider
    - **Active:** text-primary
    - **Past:** text-primary/50
    - **Future:** text-muted-foreground/50
- **Connector lines (between dots):**
  - h-px mx-1.5 flex-1
  - **Past connector:** bg-primary/30
  - **Future connector:** bg-border/50
- **Data deps:** `activeTab` (determines which stage is highlighted), `PIPELINE_STEPS` config

---

### Zone 3a: Board View Container (Desktop/Tablet)
**Purpose:** Show 4-column kanban when `viewMode === 'board'`

**Visual:** 
- Mobile (<1024px, non-review mode): Tab navigation bar above scrollable single-column view
- Desktop (≥1024px): 4-column grid or horizontal scroll

**Sub-regions:**

#### Zone 3a-i: Mobile Tab Navigation
**Visible:** `lg:hidden` (mobile and tablet when not in review mode)

**Visual:** Flex row, `mb-4 bg-muted/30 p-1 rounded-xl border border-border/50`

**Regions per tab:**
- **4 tab buttons** (one per activeColumn):
  - **Layout:** Flex column, items-center, justify-center, gap-1
  - **Content:**
    - Emoji (column.emoji)
    - Title label (column.title) — text-[10px] font-bold uppercase truncated
    - Count badge (if count > 0) — text-[9px] font-black px-1.5 py-0.5 rounded-full
      - Review column: bg-warning/20 text-warning
      - Other columns: bg-muted-foreground/20 text-muted-foreground
  - **States:**
    - Active tab: bg-background text-primary shadow-sm ring-1 ring-border/50
    - Inactive: text-muted-foreground
    - Drag target (desktop): ring-2 ring-primary/30 bg-background
  - **Data deps:** `columnCounts[column.id]`, `activeTab`, `draggedItem`, `dropTargetTab`

#### Zone 3a-ii: Optional Hint Banner
**Visible:** `!hintDismissed && backlogItems.length >= 10`

**Visual:** Flex row, `mb-4 px-4 py-2.5 bg-info/10 border border-info/20 rounded-xl`, gap-3

**Content:**
- Info icon (w-4 h-4 text-info)
- Message: "Você já tem **N** ideias salvas. Use o modo Decidir uma a uma para aprovar mais rápido."
- "Decidir agora" button → `setViewMode('review')`
- Dismiss button (X icon) → `dismissHint()`

**Data deps:** `hintDismissed`, `backlogItems.length`

#### Zone 3a-iii: Kanban Columns Container
**Visual:** Flex row, `overflow-x-auto pb-4 custom-scrollbar`, `lg:grid lg:grid-cols-4`

**Responsive:**
- Mobile: `flex gap-4 min-w-max` (horizontal scroll, shows activeTab column only unless lg)
- Desktop: `lg:grid lg:grid-cols-4` (all 4 visible)

**Per-column structure:**
- **Column wrapper:** w-72 lg:w-auto, flex flex-col, rounded-2xl
  - State: `dropTargetTab === column.id && !isCoarsePointer` → shadow-drop-target scale-[1.01]
  - Drag zones: `onDragEnter`, `onDragLeave`, `onDragOver`, `onDrop`
  - Data deps: `draggedItem`, `dropTargetTab`, `isCoarsePointer`

- **Column header:**
  - `rounded-t-2xl px-4 pt-3 pb-0 border-t border-x`
  - Background + border color per status:
    - backlog: bg-muted/50 text-muted-foreground border-border/50
    - review: bg-warning/10 text-warning border-warning/20
    - approved: bg-info/10 text-info border-info/20
    - published: bg-success/10 text-success border-success/20
  - **Content:** Flex row with icon, title, count
    - Icon: column.Icon (lucide-react component)
    - Title: column.title (e.g., "Ideias salvas")
    - Count badge: tabCount > 0 ? `${tabCount > 20 ? '20+' : tabCount}` : null

- **Column body:** bg-muted/10 rounded-b-2xl p-3 min-h-[500px] border-b border-x border-border/20
  - **No cards case:** EmptyColumnState component
  - **Cards case:** Staggered flex column of KanbanCard components
    - Gap: space-y-4 (1.5rem = 24px) via grid animation
    - Data deps: `getColumnPosts(column.id)` filtered by kanban_status !== 'archived'

---

### Zone 3b: Review Mode Container (Card Deck)
**Purpose:** Show single-card swipeable interface when `viewMode === 'review'`

**Visible:** `viewMode === 'review'`

**Visual:** Flex column, items-center, justify-center, flex-1, -mt-8, fade-in animation

**Sub-regions:**

#### Zone 3b-i: Review Deck Wrapper
**Visual:** w-full max-w-sm centered

**Content:**
- PipelineStepper (activeTab = `reviewDeck.source === 'review' ? 'review' : 'backlog'`)
- Optional hint: "Nada está em Para decidir agora. Este modo mostra suas ideias salvas para você aprovar mais rápido." (shown if `reviewDeck.source === 'backlog'`)
- ProactiveCardStack component:
  - **Props:**
    - `suggestions`: `reviewDeck.items` mapped to suggestion objects with `isRegenerating` flag
    - `onApprove`: `handleReviewDeckApprove` (moves to approved, optionally updates caption/date/format)
    - `onSkip`: `handleReviewDeckSkip` (moves back to backlog)
    - `onRegenerate`: `handleReviewDeckRegenerate` (calls n8n webhook `/webhook/2-1-content-generator-manual`)
    - `onRefresh`: `handleReviewDeckRefresh` (clears hidden IDs, refreshes posts)
    - `onGenerate`: Navigate to `/create`
    - `onCaptionSave`: `updateCard(id, { final_copy: caption })`
    - `isGenerating`: `regeneratingDeckIds.length > 0`
    - `companyName`: `project?.name ?? 'Minha empresa'`
    - `isFirstGeneration`: `getColumnPosts('published').length === 0`
    - `onOpenDetails`: `setSelectedReviewSuggestion(suggestion)` (opens PostDetailModal if user wants full preview)

- **Gesture indicators (below deck):**
  - Shown if `backlogItems.length > 0`
  - Green text: "Deslize para Direita para Aprovar"
  - Red text: "Deslize para Esquerda para Ver Depois" (50% opacity)
  - Text size: text-[10px] font-black uppercase tracking-[0.2em]

**Data deps:** `reviewDeck`, `regeneratingDeckIds`, `project?.name`, `isFirstGeneration`, `backlogItems.length`

---

### Zone 4: Modals & Overlays
**Purpose:** Provide detail view and editing without leaving kanban surface

**Modal 1: PostDetailModal**
- **Trigger:** User taps card or card header
- **Dismissal:** Click backdrop, press Escape, tap close button
- **Content:**
  - Header: Post thumbnail, status badge, error state (if last_error exists)
  - Fields (editable): final_copy, final_hashtags, scheduled_date, post_format, automation_tier
  - Action buttons: Approve, Reject, Reschedule, Edit, Copy Caption
  - Error retry: If last_error exists, show "Retry" button → `retryPublication(item.id)`
- **Data deps:** `selectedPost` (which item is being viewed), `project` (for meta mapping), `isPublishing` (disable buttons while publishing)

**Modal 2: QuickCreateDetailModal**
- **Trigger:** Currently not used in primary flow; reserved for inline rapid creation
- **Dismissed via:** Backdrop click or cancel button

**Dropdown Menu (per KanbanCard)**
- **Trigger:** MoreHorizontal button on card
- **Options:**
  - Duplicate → `duplicateCard(item.id)`
  - Delete → `deleteCard(item.id)`
  - [future] Reschedule → expand date picker inline

---

### Zone 5: Toast Notifications
**Purpose:** Provide real-time feedback for approvals, rejections, errors

**Visual:** Bottom-right (desktop), bottom-center (mobile), auto-dismiss or manual action

**Toast variants:**
- **Approval success:** Green, "Post aprovado ✓", 3s auto-dismiss
- **Rejection success:** "Movido para Ideias salvas", 3s auto-dismiss
- **Safe-flow undo prompt:** Shows 3s countdown with visual progress bar, "Desfazer" action button
- **Approval error:** Red, "Não foi possível aprovar. Tente novamente.", manual dismiss + retry button
- **Regeneration error:** "Erro ao gerar nova ideia. Tente novamente em alguns instantes."
- **Empty state info:** "Post já está nas ideias salvas. Continue revisando os próximos."

**Data deps:** `toast()` hook triggered by status transitions, errors, and user actions

---

## B. Component Anatomy

### KanbanHeader (Zone 1)
```
KanbanHeader
├─ Left Content (flex: 1)
│  ├─ Kicker Badge (hero-kicker)
│  │  ├─ Eye icon (w-4 h-4)
│  │  └─ Text: "Aprovar posts"
│  ├─ Page Title (h2)
│  │  └─ Text: "Decida o que vai para a agenda"
│  └─ Subtitle (p)
│     └─ Text: context-dependent hint
└─ Right Controls (flex row, gap-2)
   ├─ View Mode Toggle (ButtonGroup)
   │  ├─ Button: "Quadro completo" (LayoutDashboard icon)
   │  └─ Button: "Decidir uma a uma" (Library icon, with optional badge)
   └─ Hide Published Toggle (Button)
      ├─ Eye icon
      └─ Text: "Mostrar publicados" or "Ocultar publicados"
```

### PipelineStepper (Zone 2)
```
PipelineStepper (flex row)
├─ Step 1 (backlog)
│  ├─ Dot indicator (bg-primary | bg-primary/40 | bg-border)
│  ├─ Label ("Ideias salvas")
│  └─ Connector line (if not last)
├─ Step 2 (review)
│  ├─ Dot indicator
│  ├─ Label ("Para decidir")
│  └─ Connector line
├─ Step 3 (approved)
│  ├─ Dot indicator
│  ├─ Label ("Agendados")
│  └─ Connector line
└─ Step 4 (published)
   ├─ Dot indicator
   ├─ Label ("Publicados")
   └─ (no connector)
```

### KanbanColumn (Zone 3a-iii)
```
KanbanColumn
├─ Column Header (rounded-t-2xl, bg-status/10)
│  ├─ Icon (status-dependent)
│  ├─ Title ("Ideias salvas", etc.)
│  ├─ Subtitle (context text)
│  └─ Count Badge (if count > 0)
└─ Column Body (rounded-b-2xl, bg-muted/10)
   ├─ KanbanCard (if items > 0)
   │  ├─ Media thumbnail (aspect-[4/3], format badge)
   │  ├─ Card body (p-3)
   │  │  ├─ Title (text-sm font-semibold)
   │  │  ├─ Description (text-xs muted)
   │  │  └─ Status badge (kanban_status)
   │  └─ Actions row
   │     ├─ Approval buttons (Aprovar, Não quero) or drag handle
   │     └─ MoreHorizontal menu (dropdown)
   ├─ KanbanCard (stacked, gap-6)
   └─ KanbanCard
   OR
   └─ EmptyColumnState (if no items)
      ├─ Emoji
      ├─ Headline ("Sua fábrica está aquecida", etc.)
      ├─ Hint text
      └─ Optional CTA button (for backlog: "Criar meu primeiro post" → /create)
```

### KanbanCard (Sub-component)
```
KanbanCard
├─ Container (rounded-2xl, border border-border/60, drag-enabled on desktop)
├─ Media Container (aspect-[4/3], rounded-xl)
│  ├─ Image or video preview
│  └─ Format badge (CARROSEL, STORY, REEL) positioned bottom-right
├─ Card Body (p-3, space-y-2)
│  ├─ Title (text-sm font-semibold truncate)
│  ├─ Description (text-xs muted-foreground line-clamp-2)
│  ├─ Status badge (kanban_status color)
│  └─ Scheduled date (if approved and has scheduled_date)
│     └─ Text: "📅 2025-05-15 14:00" (if urgentCount > 0, show in warning color)
├─ Actions row (flex gap-2)
│  ├─ [Desktop] Approval buttons: "Aprovar" (success), "Não quero este" (destructive)
│  ├─ [Desktop] Drag handle: Cursor: move on hover
│  ├─ [Mobile] Swipe zones: Right swipe → approve, Left swipe → reject
│  └─ MoreHorizontal menu (icon button, w-6 h-6)
│     ├─ Duplicate
│     ├─ Delete
│     ├─ Separator
│     └─ [future] Reschedule
└─ Error state (if last_error)
   ├─ Status badge: "⚠️ ERRO"
   └─ Retry button (in place of approval buttons)
```

### PostDetailModal (Zone 4)
```
PostDetailModal
├─ Modal::Backdrop (fixed, clickable to close)
├─ Modal Content (max-w-md, p-6)
│  ├─ Header
│  │  ├─ Post thumbnail (w-full, aspect-video)
│  │  ├─ Close button (top-right)
│  │  └─ Status badge (kanban_status)
│  ├─ Body
│  │  ├─ Title field (editable, text-lg font-bold)
│  │  ├─ Caption field (editable, textarea)
│  │  ├─ Hashtags field (editable, tokenized input or textarea)
│  │  ├─ Scheduled date field (date + time picker)
│  │  ├─ Post format selector (Feed, Story, Reel)
│  │  ├─ Automation tier selector (Full auto, Manual)
│  │  ├─ Last error display (if error exists)
│  │  │  ├─ Error message (red text, text-xs)
│  │  │  └─ Retry button
│  │  └─ Metadata (created_at, updated_at) — text-xs muted
│  └─ Footer
│     ├─ Cancel button (variant: outline)
│     ├─ Approve button (variant: default/success, moves to approved)
│     ├─ Reject button (variant: destructive, moves to backlog)
│     └─ Optional: Reschedule picker inline
└─ State: selectedPost (which item opened modal), validationErrors (from Zod schema)
```

### ProactiveCardStack (Zone 3b-i)
```
ProactiveCardStack (via component library)
├─ Current card (pinned center, max-w-sm)
│  ├─ Media (full viewport width, aspect-video or 1:1)
│  ├─ Card body (p-4)
│  │  ├─ Title
│  │  ├─ Description / Caption
│  │  └─ Post format badge
│  ├─ Actions row (flex justify-between)
│  │  ├─ "Não quero" button (left, swipe-left target)
│  │  ├─ Card progress indicator (X de N)
│  │  ├─ "Regenerar" button or icon (center, if generated_by set)
│  │  └─ "Aprovar" button (right, swipe-right target)
│  └─ Caption editor (expandable, optional inline)
└─ Swipe zone (Framer Motion drag)
   ├─ Right swipe: Calls onApprove()
   ├─ Left swipe: Calls onSkip()
   ├─ Visual feedback: Scale, opacity, color shift during swipe
   └─ Exit animation: Card flies off screen (right or left)
```

### EmptyColumnState (Sub-component)
```
EmptyColumnState
├─ Container (min-h-[180px], border dashed, rounded-2xl, flex column items-center justify-center)
├─ Emoji (text-3xl)
├─ Headline (text-sm font-semibold)
├─ Hint (text-xs muted-foreground, max-w-[220px])
└─ Optional CTA
   ├─ Shown only for backlog column
   ├─ Text: "Criar meu primeiro post" (Sparkles icon)
   ├─ Href: /create
   └─ Variant: outline, rounded-full
```

---

## C. Data Model

### Primary Data Source: Supabase `content_calendar` table

**Columns referenced on Kanban screen:**

| Column | Type | Usage | Required? |
|--------|------|-------|-----------|
| `id` | UUID | Unique post identifier | ✓ |
| `project_id` | UUID | Filter by project | ✓ |
| `kanban_status` | Enum ('backlog' \| 'review' \| 'approved' \| 'published' \| 'archived') | Determines column position | ✓ |
| `final_copy` | Text | Post caption / body text | ✓ |
| `final_hashtags` | Text[] | Hashtag list | ✗ |
| `post_preview_url` | URL | Thumbnail for card media | ✗ |
| `final_video_url` | URL | Video URL if format is video | ✗ |
| `scheduled_date` | Timestamp | When post should publish | ✗ |
| `post_format` | Enum ('feed' \| 'story' \| 'reel' \| 'carousel') | Content format | ✗ |
| `automation_tier` | Enum ('full_auto' \| 'manual') | Publishing trigger | ✓ |
| `generated_by` | Text | Source of content (e.g., 'S.0007', 'manual', 'proactive') | ✗ |
| `last_error` | Text | Error message from last publish attempt | ✗ |
| `content_details` | JSONB | Structured metadata (caption, brief, hashtags, platform, post_format) | ✗ |
| `created_at` | Timestamp | Post creation time | ✓ |
| `updated_at` | Timestamp | Last modification time | ✓ |

**Filter conditions:**
- `project_id === currentProjectId`
- `kanban_status !== 'archived'` (always exclude archived posts)
- `kanban_status IN ['backlog', 'review', 'approved', 'published']` (only active statuses on kanban)

### Secondary Data Sources

**`projects` table:**
- `id`: Used to filter content_calendar rows
- `name`: Displayed in ProactiveCardStack (e.g., "Restaurante João")
- `tier_automation`: Determines if user can use full_auto (may inform UI enablement)
- `strategic_plan_current`: Contains week_theme_overrides (not used on kanban directly, but context for calendar)

**`credentials` table:**
- `service_name = 'meta'`: Used to map Instagram account for preview (not rendered on kanban, but affects modal behavior)
- `user_id`: RLS filter ensures user only sees their own posts

**Realtime subscription:**
- Channel: `content_calendar:project_id=<projectId>`
- Events: INSERT, UPDATE, DELETE
- Effect: Auto-refresh column counts, add/remove cards, update status badges

---

## D. State Ownership

### URL State (via sessionStorage)
- `kanban_active_tab`: Which column tab is active on mobile (KanbanStatus enum)
- `kanban_view_mode`: 'board' or 'review' (persists across refreshes)
- `kanban_hide_published`: Boolean (user preference to hide/show published column)
- `kanban_hint_dismissed`: Boolean (user dismissed the "10+ ideas in backlog" hint)

### Component React State (KanbanPage)

| State | Type | Owned by | Lifetime | Trigger |
|-------|------|----------|----------|---------|
| `viewMode` | 'board' \| 'review' | KanbanPage | Until sessionStorage or user action | User toggle button, media query (coarse pointer) |
| `activeTab` | KanbanStatus | KanbanPage | Until user clicks tab (mobile only) | Mobile tab click, sessionStorage fallback |
| `hidePublished` | Boolean | KanbanPage | Until user toggle | Eye icon toggle button, sessionStorage |
| `hintDismissed` | Boolean | KanbanPage | Until page reload | Dismiss button (X icon), sessionStorage |
| `selectedPost` | Post \| null | KanbanPage | Until modal closes | Card click (open) or modal close button (close) |
| `selectedReviewSuggestion` | ProactiveSuggestion \| null | KanbanPage | Until modal closes or deck navigates | ProactiveCardStack click (open detail) |
| `draggedItem` | ContentCalendarItem \| null | KanbanPage | Until drop or drag ends | `handleDragStart`, `handleDragEnd` |
| `dropTargetTab` | KanbanStatus \| null | KanbanPage | Until drop or drag ends | `onDragEnter` (set), `onDragLeave` / `onDrop` (clear) |
| `reviewDeckHiddenIds` | string[] | KanbanPage | Until deck refreshes | `handleReviewDeckRegenerate` (hide), `handleReviewDeckRefresh` (clear) |
| `regeneratingDeckIds` | string[] | KanbanPage | Until regeneration finishes | `handleReviewDeckRegenerate` (add/remove) |
| `pendingUpdate` | `{ id: string; to: KanbanStatus }` \| null | KanbanPage | Safe-flow only, 3s undo window | `moveCard` (set), undo button or timeout (clear) |
| `isLgUp` | Boolean | KanbanPage | Until window resize | `window.matchMedia('(min-width: 1024px)')` |
| `isCoarsePointer` | Boolean | KanbanPage | Until pointer mode changes | `window.matchMedia('(pointer: coarse)')` |

### Derived State (computed, not stored)

| Derived | Computed from | Purpose |
|---------|---------------|---------|
| `activeColumns` | `hidePublished` + `baseColumns` | Filter columns array to show/hide published |
| `backlogItems` | `getColumnPosts('backlog')` filtered by kanban_status | Count and render backlog column |
| `reviewItems` | `getColumnPosts('review')` filtered by kanban_status | Count and render review column |
| `columnCounts` | `getColumnPosts(column.id).length` for each column | Render badge counts |
| `reviewDeck` | `getReviewDeckState(visibleReviewItems, visibleBacklogItems)` | Determine which source (review or backlog) feeds the deck |
| `isFirstGeneration` | `getColumnPosts('published').length === 0` | Determine celebratory empty state on ProactiveCardStack |

### Server State (Supabase)

**Stored and synced via `useKanban` hook:**
- `content_calendar` rows (fetched on mount, updated via realtime subscription)
- **Mutations via `moveCard(id, to: KanbanStatus)`:**
  - Updates `content_calendar.kanban_status = to`
  - Triggers Supabase RLS check (user_id + project_id must match)
  - On `review` → `approved`: Triggers Kanban Trigger webhook (S.0009a → S.0010)
  - On any update: Emits realtime event, updates all subscribed clients

**Optimistic updates pattern (safe-flow):**
1. User approves post → `pendingUpdate = { id, to: 'approved' }`
2. Toast shows "Movido para Agendados" + "Desfazer" button + 3s countdown
3. If undo clicked → cancel `baseMoveCard` call, keep local state
4. If 3s timeout → call `baseMoveCard(id, 'approved')`
5. Supabase updates, realtime event propagates to all tabs

---

## E. Interaction Flows

### Flow 1: Approve a Post (Desktop Board Mode)
```
User lands on /kanban (viewMode defaults to 'board' on desktop)
  ↓
User sees 4 columns: Ideias salvas (8), Para decidir (3), Agendados (12), Publicados (87)
  ↓
User sees review column has 3 posts waiting. Taps one to see detail modal.
  ↓
PostDetailModal opens:
  - Shows thumbnail (4:3 aspect)
  - Shows caption preview
  - Shows "Aprovar" button (green)
  ✓ User reads caption and is satisfied
  ↓
User taps "Aprovar" button
  ↓
System:
  1. Calls updateCard(id, { kanban_status: 'approved' })
  2. Closes PostDetailModal
  3. Shows toast: "Movido para Agendados" (safe-flow: + undo button, 3s countdown)
  4. Card animates out of "Para decidir" column, animates into "Agendados" column
  5. Column counts update: Para decidir (2), Agendados (13)
  6. If automation_tier === 'full_auto': Webhook triggers immediately to S.0009a → S.0010
  ↓
User sees immediate feedback: card moved, count changed, toast confirmed
```

### Flow 2: Reject / "Não quero este" (Mobile Review Deck Mode)
```
User lands on /kanban on mobile (coarse pointer detected, viewMode defaults to 'review')
  ↓
User sees single card in center of screen (ProactiveCardStack):
  - Image (4:3 aspect)
  - Caption
  - "Não quero" button (left), "Aprovar" button (right)
  - Gesture hint: "Deslize para Direita para Aprovar"
  ✓ User swipes LEFT on card (or taps "Não quero" button)
  ↓
System:
  1. Card animates out (flies left, opacity 0)
  2. Calls moveCard(id, 'backlog')
  3. Shows toast: "Movido para Ideias salvas"
  4. Next card appears (or empty state if no more)
  ↓
User sees next card in deck, ready to decide
```

### Flow 3: Review Deck Mode — Approve with Caption Edit
```
User in review deck, swipes or taps "Aprovar"
  ↓
ProactiveCardStack opens inline caption editor (expandable)
  ✓ User edits caption, taps "Salvar"
  ↓
System:
  1. Calls updateCard(id, { final_copy: newCaption })
  2. User taps final "Aprovar" button
  3. Calls handleReviewDeckApprove(id, { finalCopy: newCaption })
  4. Moves card to 'approved'
  5. Shows toast confirmation
  ↓
Card disappears from deck, next card appears
```

### Flow 4: Drag-and-Drop Move (Desktop Board Mode)
```
User hovers over card in "Para decidir" column (desktop, non-coarse pointer)
  ↓
System: Cursor changes to "move", card shows subtle lift (hover state)
  ✓ User presses mouse down, drags card to "Agendados" column header
  ↓
On drag over:
  1. Column header shows visual feedback: ring-2 ring-primary/30, scale slight lift
  2. Cursor remains "move"
  ↓
✓ User releases mouse over "Agendados" column
  ↓
System:
  1. Calls handleDrop('approved')
  2. Calls moveCard(id, 'approved')
  3. Card animates out of source column, animates into target column
  4. Toast: "Movido para Agendados" (safe-flow: + undo)
  5. Column counts update
  ↓
Card is now in "Agendados", ready for next decision
```

### Flow 5: Swipe Gesture Move (Mobile Board Mode, Tab View)
```
User on mobile in board mode, viewing "Para decidir" column via tab.
✓ User swipes RIGHT on KanbanCard
  ↓
System:
  1. Detects swipe offset > 110px
  2. Framer Motion drag triggers swipeEnd handler
  3. Card animates out (swipe direction)
  4. Calls moveToNext(item) → moves card to 'approved'
  5. Shows toast: "Movido para Agendados"
  ↓
Card disappears from visible column, next card slides up
```

### Flow 6: Regenerate Idea (Review Deck, Full Auto Flow)
```
User in review deck, sees post they don't like (e.g., copy doesn't fit).
✓ User taps "Regenerar" button (circular arrow icon)
  ↓
System:
  1. Sets isRegenerating = true (loading state on button)
  2. Hides card from deck (adds to reviewDeckHiddenIds)
  3. Makes POST to /webhook/2-1-content-generator-manual with:
     {
       project_id: projectId,
       posts_to_generate: 1,
       kanban_status_override: 'review'
     }
  ↓
n8n S.0007 processes request, generates new idea, inserts into content_calendar
  ↓
System:
  4. Calls refreshPosts() (realtime subscription fires)
  5. New post appears in reviewDeck (replaces old position or appends)
  6. Toast: "Nova ideia gerada! Revise aqui."
  7. User can now approve or skip the new idea
  ↓
If generation fails:
  - Toast: "Erro ao gerar nova ideia. Tente novamente em alguns instantes."
  - Card becomes unhidden (returns to deck)
  - User can retry or skip
```

### Flow 7: Empty State → Create (First-Time User)
```
User lands on /kanban. Kanban is empty (no posts in any column).
  ↓
All columns show EmptyColumnState:
  - Backlog: "Sua fábrica está aquecida" + "Criar meu primeiro post" button
  - Review: "Tudo em dia! Missão cumprida 🎉"
  - Approved: "Pronto para seguir o fluxo"
  - Published: "Sua história está sendo escrita"
  ↓
✓ User taps "Criar meu primeiro post" (only in backlog column)
  ↓
Navigate to /create?date=TODAY
  ↓
User creates their first post → post lands in backlog → returns to /kanban (or refresh)
  ↓
Kanban now shows 1 post in backlog, stepper updates, empty states disappear
```

### Flow 8: Real-Time Sync (Two Tabs Open)
```
Tab A (user): /kanban in board mode, viewing "Para decidir" column (3 posts)
Tab B (background): /kanban also open
  ↓
User in Tab A approves a post → calls moveCard(id, 'approved')
  ↓
System (Tab A):
  1. Updates local state
  2. Calls Supabase updateCard()
  3. Toast appears (undo available if safe-flow)
  ↓
Supabase realtime event fires:
  - Tab A: Removes card from review column, adds to approved column
  - Tab B: Receives realtime event, updates its own getColumnPosts() cache
  ↓
Tab B (user sees):
  - "Para decidir" count changes from 3 → 2
  - "Agendados" count changes from 12 → 13
  - Card that was approved now appears in approved column (if user scrolls there)
  - NO PAGE RELOAD needed; Supabase subscription keeps both tabs in sync
```

---

## F. Error States & Handling

### Approval Fails (Rate Limit / Stripe Limit / Instagram Error)

**Scenario:** User approves post, Instagram API returns 429 (rate limited) or Instagram rejects due to rate limit.

**UX Response:**
1. Toast shows: "Não foi possível aprovar. Tente novamente." (error variant, red)
2. Card stays in "Para decidir" column (state not changed, safe-flow undo cancels operation)
3. `last_error` field on post is updated with error message
4. PostDetailModal (if open) shows error inline: "⚠️ ERRO: Rate limit exceeded"
5. Retry button appears (calls `retryPublication(item.id)` → tries webhook again)
6. **User action:** Retry later or move to another post

**Backend flow:**
- n8n S.0010 catches error, writes to `last_error` field, emits realtime event
- Frontend updates toast + card status badge

### Stripe Token Limit Exceeded

**Scenario:** User approves post, but they've exhausted their free idea quota or token balance.

**UX Response:**
1. Toast: "Você atingiu o limite. Mude seu plano para continuar."
2. Card stays in "Para decidir"
3. `last_error` shows: "Insufficient tokens / credits"
4. Card shows status badge: "⚠️ LIMITE"
5. **User action:** Click "Mudar plano" link in toast → navigate to /settings/billing

### Drag-Drop Fails (Network Error During Move)

**Scenario:** User drag-drops card, but network request fails before Supabase updates.

**UX Response:**
1. Card animates to target column optimistically
2. Toast appears: "Movimento salvo..." (info variant)
3. Request fails → Toast updates: "Erro ao mover. Tente novamente." (error, manual dismiss + retry button)
4. Card snaps back to original column (revert animation)
5. **User action:** Retry or move on to different post

### Regenerate Fails (n8n Error or No Fresh Ideas Available)

**Scenario:** User taps "Regenerar" on a post, but n8n can't generate another idea (no more ideas, quota exhausted, etc.).

**UX Response:**
1. Card temporarily hidden from deck
2. n8n returns error: `{ success: false }`
3. Toast: "Ainda não encontrei outra ideia. Mantive esta sugestão por aqui para você decidir com calma."
4. Card unhides in deck (same position as before)
5. **User action:** Approve this post or skip to backlog; try regenerating on another post

### Realtime Subscription Fails / Lost Connection

**Scenario:** User has kanban open, network disconnects, realtime subscription drops.

**UX Response:**
1. Card counts may become stale (not auto-updating)
2. User can still perform local actions (approve, reject, drag), but updates won't sync to other tabs
3. On reconnect: `useKanban` hook detects loss and refreshes posts via `refreshPosts()`
4. Stepper and column counts re-sync automatically
5. **User action:** No action needed; data syncs automatically on reconnect

### Last Error Display in Post Detail Modal

**When shown:**
- If `selectedPost.lastError` is populated (from `content_calendar.last_error`)

**Visual:**
```
[Error box, red background, text-xs]
⚠️ <error message>
[Retry button] [Dismiss button]
```

**Retry action:** `retryPublication(item.id)` → triggers n8n S.0010 again with same post

---

## G. Edge Cases & Constraints

### Edge Case 1: Empty Board (First-Time User, Zero Posts)

**Condition:** `getColumnPosts('backlog').length === 0 && getColumnPosts('review').length === 0 && ...` (all empty)

**UX:**
- All columns show EmptyColumnState
- Backlog: "Sua fábrica está aquecida" + "Criar meu primeiro post" button
- Review: "Tudo em dia! Missão cumprida 🎉"
- Stepper shows no active stage (all dots are neutral color)
- No toast warnings

**Behavior:**
- If user is in review mode, ProactiveCardStack shows empty state: "Nenhuma ideia por enquanto"
- If user in board mode, stepper is grayed out, all columns show celebratory empty states

### Edge Case 2: First Generation (User Just Published First Post)

**Condition:** `getColumnPosts('published').length > 0` (first time)

**UX:**
- ProactiveCardStack props: `isFirstGeneration={true}`
- This triggers celebratory messaging on empty backlog/review
- Copy changes to: "Missão cumprida 🎉 Seu primeiro post está no ar!"

### Edge Case 3: Two Tabs Open, Realtime Conflict (Post Approved in Tab A, Approved Again in Tab B)

**Scenario:**
- Tab A approves post → moves to 'approved' → toast shows undo
- Tab B simultaneously tries to approve same post before realtime event arrives
- User in Tab B presses "Aprovar"

**System behavior:**
1. Tab B's request arrives at Supabase
2. Post is already in 'approved' status (from Tab A)
3. Safe-flow undo timer on Tab B: no operation (already in target state, is idempotent)
4. Realtime event propagates to Tab B
5. Tab B reflects new state (if Tab A rejected it afterward, etc.)
6. **No error shown** — move is idempotent

### Edge Case 4: Mobile Keyboard Open on Modal

**Scenario:** User on mobile, opens PostDetailModal, virtual keyboard opens (textarea focus).

**UX:**
- Modal content scrolls up to keep Approve button visible above keyboard
- Textarea maintains focus, keyboard appears
- Approve/Reject buttons remain touchable (above keyboard)
- Backdrop can still be tapped to close (outside keyboard)
- On keyboard dismiss: Modal scrolls back to normal position

### Edge Case 5: Long Caption Truncation in Card Preview

**Condition:** `final_copy` is >100 characters

**UX:**
- Card body shows: `line-clamp-2` on description
- Truncated text + "..." at end
- Full caption visible in PostDetailModal or ProactiveCardStack detail view

### Edge Case 6: Media Load Fails (Broken Image URL)

**Condition:** `post_preview_url` or `final_video_url` is invalid or 404

**UX:**
- Image placeholder (bg-muted/50, aspect-[4/3])
- Fallback icon (e.g., ImageIcon) in center
- No error toast (graceful degradation)
- Card is still interactable (can approve/reject)
- In PostDetailModal: "Imagem não disponível. O post ainda pode ser publicado." (info text)

### Edge Case 7: Drag on Mobile Touch (Should NOT Trigger Drag, Only Swipe)

**Condition:** `isCoarsePointer === true` (mobile) AND user attempts to drag card

**Behavior:**
- Drag handlers disabled via conditional: `!isCoarsePointer ? handleDragStart : undefined`
- Swipe handlers take precedence: `onSwipeEnd` detects swipe offset
- Cursor remains "default" (not "move")
- User must use swipe gestures or tap buttons, not drag

### Edge Case 8: Safe-Flow Undo During Page Unload

**Condition:** User approves post (pendingUpdate set, undo window open), then navigates away / closes tab

**System behavior:**
1. useEffect cleanup runs on unmount
2. Checks `pendingUpdateRef.current` (persisted pending update)
3. If timer is still running, calls `baseMoveCard()` before unmount completes
4. Post is moved server-side; user won't lose their intent

### Edge Case 9: Published Column Hide / Show Toggle

**Condition:** User taps "Ocultar publicados" / "Mostrar publicados"

**UX:**
- `hidePublished` state toggles
- If hiding: Published column disappears from view, stepper still shows 4 steps
- If showing: Published column reappears (rightmost)
- sessionStorage persists preference across refresh
- Count badge on published column is preserved (just hidden from view)

### Edge Case 10: Automation Tier = Manual (No Auto-Publish)

**Condition:** `automation_tier === 'manual'` on an approved post

**Behavior:**
- When user approves, post moves to 'approved' but webhook S.0009a is NOT triggered
- Post sits in 'approved' waiting for manual trigger (operator must publish via admin panel)
- Card shows status badge: "📋 Aguardando" (info color)
- On PostDetailModal: "Este post requer aprovação manual antes de publicar"
- **User does not see a publish failure;** system waits for operator action

### Edge Case 11: Column Count > 99

**Condition:** `columnCounts[column.id] > 99`

**Badge rendering:**
- Shows "99+" (never shows full count if > 99)
- Text size remains text-[9px] (doesn't overflow)

### Edge Case 12: Network Request Takes >3 Seconds on Safe-Flow Undo

**Condition:** User approves, safe-flow shows undo for 3s, but server request still pending after timeout

**System behavior:**
1. 3s timer completes, `baseMoveCard()` is called
2. Request that was already in flight completes (eventually)
3. Supabase acknowledges the update
4. Realtime event propagates
5. **Result:** No conflict; operation is atomic from Supabase perspective

---

## H. Responsive Specification

### Breakpoints (Tailwind defaults)

| Name | Width | Layout |
|------|-------|--------|
| Mobile | <768px | Column tab view (one column visible) OR review deck |
| Tablet | 768px–1023px | TBD (2-column or single-column + tab bar) |
| Desktop | ≥1024px | 4-column grid (all visible if width ≥1440px, else horizontal scroll) |

### Specific Responsive Behaviors

**Mobile (<768px):**
- Hero: Single column (title stacks on buttons)
- Buttons: Wrap if needed (flex-wrap)
- Column tabs: Full-width button group, `lg:hidden`
- Column container: `w-72` (horizontal scroll)
- Card width: Full width of scrollable container
- Swipe gestures: Enabled (`onSwipeEnd`)
- Drag: Disabled (no cursor: move)
- Hint banner: Shows if `backlogItems.length >= 10`

**Tablet (768px–1023px):**
- Column tabs: Visible (similar to mobile)
- Grid: Not yet activated (still `flex gap-4 min-w-max`)
- Can show 2–3 columns visible at once if scrolling

**Desktop (≥1024px):**
- Column tabs: Hidden (`lg:hidden`)
- Grid: Active (`lg:grid lg:grid-cols-4`)
- All 4 columns visible (if viewport ≥1440px)
- If viewport 1024px–1440px: Horizontal scroll to see all 4
- Card width: `lg:w-auto` (flex: 1 or grid-based)
- Drag: Enabled (cursor: move on hover)
- Swipe: Disabled (desktop-only uses drag + click)

### Touch-Friendly Adjustments

**Button sizes:**
- Min height: 44px (touch target)
- Approval buttons: `h-10` (40px) ≥ 44px when accounting for padding
- Icon buttons: `w-6 h-6` (24px) — **CAVEAT:** May be too small; should be `w-8 h-8` (32px) or wrapped in larger touch surface
- Tab buttons: Full flex-1 width, min-height enforced

**Spacing:**
- Card gap: 1.5rem (24px) — sufficient spacing between touch targets
- Column padding: p-3 (12px) — adequate tap margin
- Hero padding: p-4 md:p-5 — breathing room

### Orientation

**Portrait (mobile/tablet):**
- Single column view (unless desktop)
- Modal appears full-height
- Keyboard can push content; modal scrollable

**Landscape (tablet/desktop):**
- 4-column grid (desktop) or 2-column tab view (tablet)
- Modal fixed, doesn't scroll with page
- Stepper remains visible at top

---

## I. Accessibility Requirements

### WCAG 2.1 Level AA Compliance

**Keyboard Navigation:**
- All buttons and interactive elements reachable via Tab key
- Drag-and-drop has keyboard fallback (arrow keys to move between columns, Enter to place)
- Modal closable via Escape key
- Stepper not keyboard-interactive (visual indicator only)

**Screen Readers:**
- `aria-label` on container: "Etapas de publicação" (PipelineStepper)
- `aria-label` on view mode buttons: "Modo quadro" / "Modo decidir uma a uma"
- Column headers: `<section role="region" aria-label="Coluna: Para decidir (3 posts)">`
- Cards: `<article role="article" aria-label="Post: 'Título da ideia' — Em revisão">`
- Modals: `role="dialog"`, `aria-labelledby="modal-title"`, trap focus

**Color Contrast:**
- All text ≥4.5:1 contrast ratio (WCAG AA standard)
- Status badges use color + icon + text (not color-only)
- Icon-only buttons have `aria-label`

**Focus Indicators:**
- All interactive elements show visible focus ring (ring-offset via Tailwind)
- Focus order follows visual order: Hero → Stepper → Tabs/Columns → Modals

**Reduced Motion:**
- `prefers-reduced-motion` media query respected for Framer Motion animations
- Animations can be disabled; content remains functional
- Toast countdown progress bar removed if `prefersReducedMotion` is true

**Alt Text & Labels:**
- Image previews: `alt="Post thumbnail"` (not critical content)
- Status icons: Accompanied by text label (e.g., "Para decidir", "Publicado")
- Buttons: Clear, action-oriented labels ("Aprovar", "Não quero", not just icons)

---

## J. Performance Constraints

### Load Time Targets
- **Initial page load:** <2s (incl. Supabase data fetch)
- **Card preview media:** <1.5s (post_preview_url image load)
- **Interaction feedback:** <100ms visual response (drag lift, button tap)
- **Drag animation:** 60fps smooth (no jank)

### Data Fetching
- **Pagination:** Not yet implemented; fetch all posts in `content_calendar` for current project on mount
- **Realtime subscriptions:** Supabase realtime channel subscribed on mount, listens for INSERT/UPDATE/DELETE
- **Lazy loading:** Card media uses native `loading="lazy"` attribute (if using <img> tags)

### State Management
- **useKanban hook:** Manages content_calendar fetch + cache + updates
- **Memoization:** KanbanCard memoized to prevent unnecessary re-renders on parent updates
- **Virtualization:** Not yet implemented; may be needed if >100 posts in single column

---

## K. Browser & Device Support

### Supported Platforms
- **Desktop:** Chrome, Firefox, Safari, Edge (latest 2 versions)
- **Mobile:** iOS 14+, Android 10+ (via web)
- **Pointer types:** Fine (mouse/trackpad), Coarse (touch)
- **Network:** 4G minimum; supports offline via service worker (future enhancement)

### Known Limitations
- **Drag-and-drop:** Not supported on coarse pointer devices (touch) — swipe is primary gesture
- **Safari mobile:** Virtual keyboard may not perfectly resize modal; scroll behavior tested
- **IE 11:** Not supported; uses modern JavaScript (no polyfills)

---

## L. Related Specifications

- **02-brief.md** — Product goals, success criteria, non-goals
- **03-visual-calibration.md** — Visual language (layout, density, shape, elevation)
- **04-blueprint.md** — Information hierarchy, responsive layout, text wireframe
- **06-component-specs.md** (future) — Detailed spec for KanbanCard, PostDetailModal, ProactiveCardStack state machines
- **08-acceptance-checklist.md** (future) — QA checklist for implementation verification
- **Content Journey UX Contract** — End-to-end `/campaign → /create → /kanban → /calendar` flow
- **Database Schema (llm-docs)** — `content_calendar` table structure, RLS policies

---

## M. Implementation Checklist (For Developers)

- [ ] **Zone 1 (Header):** Hero with title, subtitle, view toggle, hide-published button
- [ ] **Zone 2 (Stepper):** 4-step visual indicator showing current stage
- [ ] **Zone 3a (Board View):** 4 columns with drag-drop, media previews, action buttons
- [ ] **Zone 3b (Review Deck):** Swipeable card stack with gesture feedback
- [ ] **Zone 4 (Modals):** PostDetailModal for full preview + editing, QuickCreateDetailModal (reserved)
- [ ] **Zone 5 (Toasts):** Success, error, info notifications with appropriate actions
- [ ] **Data sync:** Realtime Supabase subscription, refresh on realtime events
- [ ] **Mobile responsiveness:** Tab view for columns, swipe gestures, touch-friendly targets
- [ ] **Accessibility:** Keyboard nav, screen readers, focus indicators, color contrast
- [ ] **Performance:** <2s initial load, <1.5s media load, smooth animations (60fps)
- [ ] **Error handling:** Rate limit, token exhaustion, network failures, media load failures
- [ ] **Empty states:** Celebratory copy per column, CTA buttons where appropriate
- [ ] **Safe-flow undo:** 3s undo window with countdown for move operations
- [ ] **Real-time sync:** Multiple tabs stay in sync via realtime events

