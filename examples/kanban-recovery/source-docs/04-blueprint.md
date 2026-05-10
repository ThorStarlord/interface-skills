---
spec_type: blueprint
spec_id: kanban-layout
created: 2026-05-10
status: current
source_evidence:
  - 01-inspector-evidence.md (DOM inventory, computed styles, existing implementation)
  - 02-brief.md (warm concierge, low-tech friendly, approval workflow)
  - 03-visual-calibration.md (layout archetype, density, shape, palette, typography)
---

# Blueprint: Kanban Approval Queue Layout

## A. Information Hierarchy

### Primary Focal Point: Hero Header Section
**What the user sees first on page load (desktop & mobile):**

- **Hero kicker:** "👀 Aprovar posts" — eye icon + label in compact badge
- **Page title (h2):** "Decida o que vai para a agenda" (16px–24px, black 900 weight)
- **Subtitle (p):** Context text: 
  - On **desktop/board view:** "Use o quadro completo para revisar ideias e agendar publicações em massa."
  - On **mobile/review view:** "Use este modo para decidir uma a uma, swipe para aprovar ou rejeitar."
- **View mode toggle:** Two buttons side-by-side
  - "Quadro completo" (LayoutDashboard icon) — switches to Board view
  - "Decidir uma a uma" (Library icon) — switches to Review deck view
  - On desktop: Both visible, Board is default
  - On mobile: Both visible, Review is default (auto-selected on load)
- **Hide Published toggle:** Eye icon ± strikethrough opacity — toggles published column visibility
- **Review badge (if review column has items):** "20+" badge on Review button (animates)

**Visual weight:** Hero dominates 20–25% of above-the-fold real estate (desktop). On mobile, it's full-width single-column stack.

---

### Secondary Focal Point: Pipeline Stepper
**Guides user through 4-stage workflow (persistent across modes):**

Layout: Horizontal flex row, left-aligned
```
◉ Ideias salvas —— ◯ Para decidir —— ◯ Agendados —— ◯ Publicados
```

- **Current stage indicator:** Filled dot (●) + bold label + accent bar below header
- **Past stages:** Filled dot (●) + muted label
- **Future stages:** Empty dot (○) + muted label
- **Connector lines:** Thin line between steps, opacity-50 (past) or opacity-30 (future)
- **Connector transition:** Color shifts from primary/70 (past) to border/50 (future)

**Visual purpose:** Orients user — "I'm in stage 2 of 4, reviewing posts I haven't decided on yet."

---

### Tertiary: Content Area (Board / Review Deck)
**Visible after hero + stepper, primary interaction zone:**

**Desktop (≥1024px):** 4-column Kanban grid
- User sees all 4 columns simultaneously (if viewport width ≥1440px; otherwise horizontal scroll)
- Drag-drop enabled; hover states show lift + shadow

**Tablet (768px–1023px):** TBD (see Responsive Specification section below)

**Mobile (<768px):** 
- Default: Swipeable Review deck (one card centered, pinned to viewport)
- Toggle to: Tab-based Board view (4 tabs, one active, scrollable cards vertically)

---

### Quaternary: Modals & Overlays (External Layer)
**Not part of page flow; appears on user action:**

- **PostDetailModal:** Overlay on canvas, modal::backdrop fixed to viewport, contains post caption/hashtags/date/errors
- **QuickCreateDetailModal:** Alternative modal for rapid post creation inline
- **Dropdown menu:** Triggered by MoreHorizontal button on card (3 items + separators)

---

### Quinary: Toasts & Notifications
**Bottom-right on desktop, bottom-center on mobile:**

- Success: "Post aprovado ✓" (green, 3-sec auto-dismiss)
- Error: "Não foi possível aprovar. Tente novamente." (red, manual dismiss or retry button)

---

## B. Text Wireframe

### Desktop (≥1024px): 4-Column Kanban Board

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          👀 Aprovar posts                                    │
│                  Decida o que vai para a agenda                             │
│  Use o quadro completo para revisar ideias e agendar publicações em massa.   │
│                                                                              │
│  [Quadro completo ♥]  [Decidir uma a uma]  [👁️ Mostrar publicados]          │
├─────────────────────────────────────────────────────────────────────────────┤
│  ◉ Ideias salvas —— ◯ Para decidir —— ◯ Agendados —— ◯ Publicados           │
├─────────────────────────────────────────────────────────────────────────────┤
│
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐
│  │ 📝       │  │ 👀       │  │ 📅       │  │ ✅       │
│  │ Ideias   │  │ Para     │  │ Agendad  │  │ Publicad │
│  │ salvas   │  │ decidir  │  │ os       │  │ os       │
│  │ (8)      │  │ (3)      │  │ (12)     │  │ (87)     │
│  ├──────────┤  ├──────────┤  ├──────────┤  ├──────────┤
│  │ ╔════╗   │  │ ╔════╗   │  │ ╔════╗   │  │ ╔════╗   │
│  │ ║ 🎨 ║   │  │ ║ 🎨 ║   │  │ ║ 🎨 ║   │  │ ║ 🎨 ║   │
│  │ ║    ║   │  │ ║    ║   │  │ ║    ║   │  │ ║    ║   │
│  │ ╚════╝   │  │ ╚════╝   │  │ ╚════╝   │  │ ╚════╝   │
│  │          │  │ CARROSEL │  │ 📅 5/15  │  │ ✓ Pub.   │
│  │ Post 1   │  │          │  │ 14:00    │  │ 4 mai    │
│  │ Caption  │  │ Post A   │  │          │  │          │
│  │ preview  │  │ Caption  │  │ Post 3   │  │ Post X   │
│  │          │  │          │  │ Caption  │  │ Caption  │
│  │ [Agenda] │  │[✓] [✗]   │  │          │  │          │
│  │          │  │          │  │ [Agenda] │  │          │
│  ├──────────┤  ├──────────┤  ├──────────┤  ├──────────┤
│  │ ╔════╗   │  │ ╔════╗   │  │ ╔════╗   │  │ Missão   │
│  │ ║ 🎬 ║   │  │ ║ 🎬 ║   │  │ ║ 🎬 ║   │  │ cumprida │
│  │ ║    ║   │  │ ║    ║   │  │ ║    ║   │  │ 🎉       │
│  │ ╚════╝   │  │ ╚════╝   │  │ ╚════╝   │  │          │
│  │ STORY    │  │ REEL     │  │ POST     │  │ Nenhuma  │
│  │ Post 2   │  │ Post B   │  │ Post 4   │  │ para     │
│  │ Caption  │  │ Caption  │  │ Caption  │  │ publicar │
│  │          │  │ [⚠️ ERRO]│  │          │  │          │
│  │ [Agenda] │  │ [🔄]     │  │ [Agenda] │  │          │
│  │          │  │          │  │          │  │          │
│  └──────────┘  └──────────┘  └──────────┘  └──────────┘
│
└─────────────────────────────────────────────────────────────────────────────┘
```

**Key layout details:**
- 4 columns visible at once (18rem / 288px per column default)
- Column headers: rounded-t-2xl, status-dependent background (muted/50, warning/10, info/10, success/10)
- Cards: rounded-2xl, card color (white), 1.5rem gap between cards
- Card media: Aspect 4:3 (typical), format badge on bottom-right (CARROSEL/STORY/REEL)
- Card body: p-3 (12px padding), title + description + badge + buttons stacked vertically
- Approval buttons: h-10 (44px min touch target), flex row inside card footer
- Drag handle: Cursor: move when hovering card (indicates draggable)

---

### Tablet (768px–1023px): 2-Column or Full-Width Stack (Decision Needed)

**Option A: 2-Column Grid**
```
┌─────────────────────────────────────┐
│       Hero + Stepper (same)         │
├─────────────────────────────────────┤
│  ┌──────────────┐  ┌──────────────┐ │
│  │ Ideias salvas│  │ Para decidir  │ │
│  │ (8)          │  │ (3)           │ │
│  ├──────────────┤  ├──────────────┤ │
│  │ Card 1       │  │ Card A        │ │
│  │ ...          │  │ ...           │ │
│  │ [Agenda]     │  │ [✓] [✗]       │ │
│  ├──────────────┤  ├──────────────┤ │
│  │ Card 2       │  │ Card B        │ │
│  │ ...          │  │ (+ error bar) │ │
│  │ [Agenda]     │  │ [🔄]          │ │
│  └──────────────┘  └──────────────┘ │
│  ┌──────────────┐  ┌──────────────┐ │
│  │ Agendados    │  │ Publicados    │ │
│  │ (12)         │  │ (87)          │ │
│  ├──────────────┤  ├──────────────┤ │
│  │ Card 3       │  │ [Empty state] │ │
│  │ ...          │  │              │ │
│  │ [Agenda]     │  │              │ │
│  └──────────────┘  └──────────────┘ │
└─────────────────────────────────────┘
```

**Option B: Full-Width Single Column (Scrollable Horizontally)**
```
┌─────────────────────────────────────┐
│       Hero + Stepper (same)         │
├─────────────────────────────────────┤
│  [◄] ┌──────────────────────────────┐ │
│      │ Ideias salvas    (8)          │ │
│      ├──────────────────────────────┤ │
│      │ Card 1  Card 2  Card 3   ...  │ │
│      │ [Agenda] [Agenda] [Agenda]    │ │
│      └──────────────────────────────┘ │
│  [►] ┌──────────────────────────────┐ │
│      │ Para decidir      (3)         │ │
│      ├──────────────────────────────┤ │
│      │ Card A  Card B   ...          │ │
│      │ [✓][✗] [✓][✗]                 │ │
│      └──────────────────────────────┘ │
└─────────────────────────────────────┘
```

**Recommendation:** Option A (2-column grid) — maintains desktop scanability, fewer scrolls.

---

### Mobile (<768px): Two Interaction Modes

#### Mode 1: Review Deck (Default, Swipeable)

```
┌───────────────────────────────┐
│  👀 Aprovar posts             │
│  Use este modo para decidir   │
│  uma a uma.                   │
│                               │
│ [Quadro] [Decidir ♥]  [👁️]     │
├───────────────────────────────┤
│ Para decidir (3)              │
├───────────────────────────────┤
│                               │
│          ┌───────────┐        │
│          │ ╔═════╗   │        │
│          │ ║  🎨 ║   │        │
│          │ ║     ║   │        │
│          │ ╚═════╝   │        │
│          │           │        │
│          │ Post A    │        │
│          │ Caption   │        │
│          │ preview   │        │
│          │           │        │
│          │ [✓Aprovr] │        │
│          │ [✗ Não]   │        │
│          │           │        │
│          └───────────┘        │
│                               │
│     ◄ ─── Swipe ─── ►         │
│                               │
├───────────────────────────────┤
│ Card 1 of 3                   │
└───────────────────────────────┘
```

**Characteristics:**
- One card centered, full viewport height
- Card is "pinned" (doesn't scroll with page)
- Swipe left: Reject ("Não quero este") → card exits, next card fades in
- Swipe right: Approve ("Aprovar") → card exits, next card fades in
- Buttons below card as fallback for non-touch devices
- Reduced cognitive load: "Yes or No?" only

#### Mode 2: Board View (Tab-Based, Secondary)

```
┌───────────────────────────────┐
│  👀 Aprovar posts             │
│  Use o quadro completo...     │
│                               │
│ [Quadro ♥] [Decidir]  [👁️]    │
├───────────────────────────────┤
│ Para decidir (3)              │
├───────────────────────────────┤
│ [📝] [👀✓] [📅] [✅]           │
│ Ideias Para  Agendar Pub      │
│ salvas  (3)   (12)    (87)     │
├───────────────────────────────┤
│ Active Tab: "Para decidir"    │
│                               │
│ ┌─────────────────────────┐   │
│ │ ╔════╗  Card A (STORY) │   │
│ │ ║ 🎬 ║  Caption...      │   │
│ │ ╚════╝  [✓] [✗]        │   │
│ └─────────────────────────┘   │
│ ┌─────────────────────────┐   │
│ │ ╔════╗  Card B (REEL)  │   │
│ │ ║ 🎬 ║  Caption...      │   │
│ │ ╚════╝  [⚠️ ERRO] [🔄]  │   │
│ └─────────────────────────┘   │
│ ┌─────────────────────────┐   │
│ │ ╔════╗  Card C (POST)  │   │
│ │ ║ 🎨 ║  Caption...      │   │
│ │ ╚════╝  [✓] [✗]        │   │
│ └─────────────────────────┘   │
│                               │
└───────────────────────────────┘
```

**Characteristics:**
- 4 tab buttons at top: emoji + label + count badge
- Active tab highlighted: primary color + underline
- Content scrolls vertically (cards stack 1-column)
- Tabs sticky at top during scroll
- Tab switching: instant (CSS class toggle, no animation delay)

---

## C. Responsive Specification

### Breakpoints & Mode Switching

| Breakpoint | Trigger | Primary View | Interaction Model | Layout |
|---|---|---|---|---|
| **Desktop** | `≥1024px` (lg: in Tailwind) | 4-column Kanban board | Drag/drop on desktop | Grid: 4 × N (horizontal scroll if viewport < 1440px) |
| **Tablet** | `768px–1023px` (md:) | Single-column board with tabs (current implementation) | Tap to switch columns, swipe in review mode | One active column at a time |
| **Mobile** | `<768px` (sm: / no prefix in Tailwind) | Review deck on coarse-pointer first visit; board via toggle | Swipe to approve/reject, buttons as fallback | Single card centered, pinned to viewport |

### View Mode Auto-Selection

| Device | Default View Mode | User Can Toggle? | How? |
|---|---|---|---|
| Desktop (≥1024px) | Board ("Quadro completo") | Yes | Button in hero header |
| Tablet (768–1023px) | Board tabs on fine pointer; Review on coarse pointer | Yes | Button in hero header |
| Mobile (<768px) | Review deck on coarse pointer, else board | Yes | Button in hero header |

**Important:** When user manually toggles between Board and Review on mobile:
- **Board toggle:** Tab-based single-column view activates
- **Review toggle:** Full-viewport swipeable deck activates
- **State persistence:** Choice is stored in `sessionStorage` (`kanban_view_mode`) for the current browser session

---

### Layout Shift at Breakpoints

#### 1024px Threshold (lg: breakpoint)
```
BEFORE (Tablet 1023px):
- Single-column tabs
- One active column at a time

AFTER (Desktop 1024px):
- 4-column grid visible at once
- Cards ~18rem (288px) fixed width or flex-1
- Column gap: 1rem (16px)
- Drag/drop emphasizes the grid

Trigger: CSS @media (min-width: 1024px) or Tailwind's `lg:hidden` / `lg:flex` classes
Animation: None (instant layout reflow)
```

#### 768px Threshold (md: breakpoint)
```
BEFORE (Mobile 767px):
- Single Review deck (swipeable) OR single-column tabs
- Hero section full-width
- Stepper might reflow to 2 rows (2 steps per row)

AFTER (Tablet 768px):
- Single-column board tabs remain active in current implementation
- Hero section full-width, but buttons stack horizontally
- Stepper stays 1 row (4 steps)

Trigger: CSS @media (min-width: 768px)
Animation: Card positions reflow; cards scale horizontally to new column width
Interaction: Drag/drop remains desktop-first; tablet prioritizes tap navigation
```

---

### Gesture Vocabulary

| Device | Gesture | Action | Feedback |
|---|---|---|---|
| Desktop (mouse) | Hover | Card shadow lifts with slight vertical nudge, cursor: move | Box-shadow intensifies, Y-axis `-3px`, transition about 150ms |
| Desktop (mouse) | Drag card | Move card to new column | Dragged card scales 1.04×, shadow doubles, column target highlights with dashed border |
| Desktop (mouse) | Drop | Card locks into new column, backend updates status | Exit animation, success toast (optional), next card fades in |
| Mobile (touch) | Tap card | Open PostDetailModal | Modal fades in (250ms), card dimmed behind |
| Mobile (touch) | Swipe right | Approve card (if in Review deck) | Card slides right + fades out (200ms), next card fades in, success toast |
| Mobile (touch) | Swipe left | Reject card (if in Review deck) | Card slides left + fades out (200ms), next card fades in, info toast |
| Mobile (touch) | Tap "Para decidir" tab | Activate tab | Tab underline moves, content cross-fades |
| Tablet (touch) | Drag card on Board | Move card to new column | Same as desktop drag (shadow + scale feedback) |
| Tablet (touch) | Long-press | Show context menu (alternative to MoreHorizontal button) | Menu fades in near finger position, slightly delayed (500ms) |

---

### Reflow Logic (No Overflow)

**Principle:** Content always reflows into available width; never horizontal-scroll within columns.

| Scenario | Desktop (4-col) | Tablet (2-col) | Mobile (1-col tabs) |
|---|---|---|---|
| Column width | 288px (18rem) fixed | ~50% viewport – margins | ~90vw |
| Card width | 288px | ~50% viewport – margins | ~90vw – 2×padding |
| Card aspect | 4:3 maintained | 4:3 maintained | 4:3 maintained |
| Text clamp | `line-clamp-1` (titles), `line-clamp-2` (descriptions) | Same | Same |
| Button width | Full card width – padding | Full card width – padding | Full card width – padding |
| Dropdown menu | 192px (w-48) fixed | 192px fixed (may overflow viewport on small tablet — needs scroll container) | Full viewport – margins, scrollable if needed |

**Handling overflow on small tablet:**
- If dropdown menu would overflow viewport, shift it left so it stays visible
- OR: Render menu in a modal instead of dropdown on tablet/mobile
- Decision: Check inspector evidence for current implementation approach

---

## D. Density & Whitespace Decisions

### Spacing Scale

| Token | Size | Use Cases |
|---|---|---|
| `gap-0` | 0px | No gap (disabled) |
| `gap-1` | 0.25rem (4px) | Tight element grouping (rare) |
| `gap-1.5` | 0.375rem (6px) | Badge + icon spacing, inline elements |
| `gap-3` | 0.75rem (12px) | Card body internal spacing (p-3) |
| `gap-4` | 1rem (16px) | Column gutter, page margins |
| `gap-6` | 1.5rem (24px) | **Card-to-card vertical gap in column** |
| `gap-8` | 2rem (32px) | Hero section spacing, section dividers |

### Card Spacing

**Vertical stack within a column:**
```
Card 1 (top of column)
├─ media: aspect-[4/3], object-cover
├─ body: p-3 (12px padding)
│  ├─ title: font-bold, line-clamp-1, mb-1
│  ├─ description: text-xs, line-clamp-2, text-muted-foreground
│  ├─ badges: AI-generated, age, status, flex row, gap-1.5, my-2
│  └─ buttons: flex row, gap-1.5, h-10 (44px min)
└─ footer: border-t, px-3 py-2, flex row between date & more-actions

[gap-6 / 24px vertical space]

Card 2
...
```

**Horizontal gaps (desktop board):**
```
Column 1       Column 2       Column 3       Column 4
├─ width: 288px
│
[gap-4 / 16px] [gap-4 / 16px] [gap-4 / 16px]
                    ↓              ↓              ↓
               Column 2    Column 3    Column 4
```

### Page Margins

| Breakpoint | Horizontal Margin | Vertical Margin |
|---|---|---|
| **Desktop (≥1024px)** | 32px (px-8) | 24px top/bottom (py-6) |
| **Tablet (768–1023px)** | 24px (px-6) | 20px top/bottom (py-5) |
| **Mobile (<768px)** | 16px (px-4) safe area | 16px top/bottom (py-4) |

### Touch-Target Sizing

All interactive elements ≥44px in one dimension (height preferred):

| Element | Height | Width | Padding Notes |
|---|---|---|---|
| Approval button ("Aprovar", "Não quero este") | `h-10` (40px) | Full card width – padding | Minimum acceptable |
| Dropdown trigger (MoreHorizontal) | `h-7 w-7` | 28×28px | Icon button, smaller but solid hit area |
| Tab button (mobile) | `h-12` (48px) | Flex-1 (equal share) | Full-width tab bar |
| Card itself | ≥180px (min-height for empty state) | Responsive (column width) | Entire card is tappable for detail modal |

### Empty State Styling

```
┌──────────────────────────────────────┐
│                                      │
│  min-height: 180px (min-h-[180px])   │
│                                      │
│  border: dashed, border-border/40    │
│  bg: muted/20 (very light gray)      │
│  rounded: rounded-2xl (16px)         │
│                                      │
│         ┌────────┐                   │
│         │ emoji  │  text-3xl         │
│         │ e.g. 📝 │                   │
│         └────────┘                   │
│                                      │
│  Headline                            │
│  "Sua fábrica está aquecida"         │
│  font-semibold, text-sm              │
│                                      │
│  Hint text                           │
│  "Crie seu primeiro post..."         │
│  text-xs, text-muted-foreground,     │
│  max-w-[220px], leading-relaxed      │
│                                      │
│  [CTA Button]                        │
│  rounded-full, variant-outline       │
│  "Criar meu primeiro post"           │
│                                      │
└──────────────────────────────────────┘
```

---

## E. Visual Zones & Component Placement

### Desktop Layout: 5 Zones

```
┌───────────────────────────────────────────────────────────────────────────────┐
│                              ZONE 1: Hero Header                               │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │ 👀 Aprovar posts                                                        │  │
│  │ Decida o que vai para a agenda                                          │  │
│  │ Use o quadro completo para revisar ideias...                            │  │
│  │ [Quadro completo ♥] [Decidir uma a uma] [👁️ Mostrar publicados]         │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│  gap-4 / 16px                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │              ZONE 2: Pipeline Stepper (4-Stage Progress)                │  │
│  │  ◉ Ideias salvas —— ◯ Para decidir —— ◯ Agendados —— ◯ Publicados      │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│  gap-6 / 24px                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐  │
│  │              ZONE 3: Content Canvas — 4-Column Board (Scrollable)       │  │
│  │  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐                   │  │
│  │  │ Col 1    │ │ Col 2    │ │ Col 3    │ │ Col 4    │                   │  │
│  │  │ Cards... │ │ Cards... │ │ Cards... │ │ Cards... │                   │  │
│  │  └──────────┘ └──────────┘ └──────────┘ └──────────┘                   │  │
│  └─────────────────────────────────────────────────────────────────────────┘  │
│                                                                                  │
│  ZONE 4 (External Layer): Modals (PostDetailModal, Dropdown menus)             │
│  ZONE 5 (External Layer): Toasts (success/error notifications, bottom-right)   │
└───────────────────────────────────────────────────────────────────────────────┘
```

### Mobile Layout: 5 Zones

```
┌─────────────────────────────────────┐
│    ZONE 1: Hero Header (Full Width) │
│ ┌───────────────────────────────┐   │
│ │ 👀 Aprovar posts              │   │
│ │ Use este modo para decidir    │   │
│ │ uma a uma.                    │   │
│ │ [Quadro] [Decidir ♥] [👁️]     │   │
│ └───────────────────────────────┘   │
│ gap-4 / 16px                        │
│ ┌───────────────────────────────┐   │
│ │  ZONE 2: Stepper (2-Row Reflow)   │
│ │  ◉ Ideias ——— ◯ Para decidir      │
│ │  ◯ Agendados — ◯ Publicados      │
│ │  (Or might stay 1-row, scrollable)│
│ └───────────────────────────────┘   │
│ gap-6 / 24px                        │
│ ┌───────────────────────────────┐   │
│ │ ZONE 3A: Review Deck (Pinned) │   │
│ │                               │   │
│ │     [Card pinned to VH]        │   │
│ │     [One at a time]           │   │
│ │                               │   │
│ │ Para decidir (3)              │   │
│ │ [Card A] [Swipe]              │   │
│ │                               │   │
│ │ -OR-                          │   │
│ │                               │   │
│ │ ZONE 3B: Board View (Tabs)    │   │
│ │ [📝] [👀✓] [📅] [✅]           │   │
│ │ Cards stack 1-col, scrollable │   │
│ │ below tabs                    │   │
│ │                               │   │
│ └───────────────────────────────┘   │
│                                     │
│ ZONE 4 (External): Modals           │
│ ZONE 5 (External): Toasts (btm-ctr) │
└─────────────────────────────────────┘
```

### Component Placement Rules

| Zone | Component | Position | Constraints |
|---|---|---|---|
| **Hero** | Page title (h2) | Top-center | Max-width: 90vw on mobile, full on desktop |
| **Hero** | View mode toggle | Below title, flex row, center | Buttons: variant-secondary, equal width or flex-1 |
| **Hero** | Hide Published toggle | Right of buttons OR below them (responsive) | Single button, variant-outline |
| **Stepper** | Progress dots + connectors | Full width, flex row, left-aligned | Scales down on mobile (might wrap to 2 rows if needed) |
| **Content (Desktop)** | 4-column board | Full viewport width, scrollable horizontally | Min-width: sum of 4 columns + gaps + margins |
| **Content (Mobile)** | Review deck | Centered, max-w-sm, pinned to viewport | Card height: responsive (70vh–90vh) |
| **Content (Mobile)** | Tab bar | Below hero/stepper, sticky on scroll | Full width, 4 equal-width tabs |
| **Modals** | PostDetailModal | Fixed layer, centered, backdrop darkens page | z-index: 50 (above everything except toasts) |
| **Modals** | Dropdown menu | Positioned absolutely near MoreHorizontal button | z-index: 40, flip to left if near right edge |
| **Toasts** | Notifications | Bottom-right on desktop, bottom-center on mobile | z-index: 60 (above modals), auto-dismiss in 3s |

---

## F. Reference Wireframe

### Desktop (≥1024px): Full 4-Column Board

```
VIEWPORT WIDTH: 1440px+

┌─────────────────────────────────────────────────────────────────────────────────────┐
│  px-8 (32px margin)                                                                 │
│  ┌───────────────────────────────────────────────────────────────────────────────┐  │
│  │  py-6 (24px padding)                                                          │  │
│  │                                                                               │  │
│  │   👀 Aprovar posts                                   [View Buttons] [Hide]     │  │
│  │   Decida o que vai para a agenda                                              │  │
│  │   Use o quadro completo para revisar...                                       │  │
│  │                                                                               │  │
│  │  py-6 / gap-8                                                                 │  │
│  │  ◉ Ideias salvas ── ◯ Para decidir ── ◯ Agendados ── ◯ Publicados             │  │
│  │                                                                               │  │
│  └───────────────────────────────────────────────────────────────────────────────┘  │
│  gap-6 / 24px                                                                       │
│  ┌───────────────────────────────────────────────────────────────────────────────┐  │
│  │ w-full, overflow-x-auto (if needed), flex gap-4                              │  │
│  │                                                                               │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐          │  │
│  │  │ Col: 288px  │  │ Col: 288px  │  │ Col: 288px  │  │ Col: 288px  │          │  │
│  │  │ Header      │  │ Header      │  │ Header      │  │ Header      │          │  │
│  │  │ (rounded-t) │  │ (rounded-t) │  │ (rounded-t) │  │ (rounded-t) │          │  │
│  │  ├─────────────┤  ├─────────────┤  ├─────────────┤  ├─────────────┤          │  │
│  │  │ Card 1      │  │ Card A      │  │ Card 3      │  │ Card X      │          │  │
│  │  │ 288px       │  │ 288px       │  │ 288px       │  │ 288px       │          │  │
│  │  │ (draggable) │  │ (draggable) │  │ (draggable) │  │ (draggable) │          │  │
│  │  │             │  │             │  │             │  │ (empty)     │          │  │
│  │  │ gap-6       │  │ gap-6       │  │ gap-6       │  │             │          │  │
│  │  │             │  │             │  │             │  │             │          │  │
│  │  │ Card 2      │  │ Card B      │  │ Card 4      │  │ (empty)     │          │  │
│  │  │ (draggable) │  │ (draggable) │  │ (draggable) │  │             │          │  │
│  │  │             │  │             │  │             │  │             │          │  │
│  │  │ gap-6       │  │ gap-6       │  │ gap-6       │  │             │          │  │
│  │  │             │  │ [error]     │  │             │  │             │          │  │
│  │  │ (empty)     │  │ [retry]     │  │ (empty)     │  │ (empty)     │          │  │
│  │  │             │  │             │  │             │  │             │          │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘          │  │
│  │                                                                               │  │
│  └───────────────────────────────────────────────────────────────────────────────┘  │
│  px-8                                                                               │
└─────────────────────────────────────────────────────────────────────────────────────┘

CARDS EXPAND: ←
If viewport < 1440px, content scrolls horizontally to show all 4 columns.
```

### Tablet (768–1023px): 2-Column Grid

```
VIEWPORT WIDTH: 900px (example)

┌─────────────────────────────────────┐
│ px-6 (24px)                          │
│ ┌─────────────────────────────────┐  │
│ │ 👀 Aprovar posts                │  │
│ │ Use o quadro...                 │  │
│ │ [View Btns]  [Hide]             │  │
│ │ py-5, gap-8                     │  │
│ │ ◉ Ideias ── ◯ Para ── ◯ Agend...│  │
│ └─────────────────────────────────┘  │
│ gap-6                                │
│ ┌─────────────────────────────────┐  │
│ │ flex gap-4, 2-column grid       │  │
│ │                                 │  │
│ │ ┌──────────────┐ ┌───────────┐ │  │
│ │ │ Col 1: ~45%  │ │ Col 2:45% │ │  │
│ │ │ Header       │ │ Header    │ │  │
│ │ ├──────────────┤ ├───────────┤ │  │
│ │ │ Card 1       │ │ Card A    │ │  │
│ │ │ ~45vw        │ │ ~45vw     │ │  │
│ │ │ gap-6        │ │ gap-6     │ │  │
│ │ │ Card 2       │ │ Card B    │ │  │
│ │ │ gap-6        │ │ gap-6     │ │  │
│ │ │ (empty)      │ │ (empty)   │ │  │
│ │ └──────────────┘ └───────────┘ │  │
│ │ ┌──────────────┐ ┌───────────┐ │  │
│ │ │ Col 3: ~45%  │ │ Col 4:45% │ │  │
│ │ │ Header       │ │ Header    │ │  │
│ │ ├──────────────┤ ├───────────┤ │  │
│ │ │ Card 3       │ │ (empty)   │ │  │
│ │ │ gap-6        │ │ (empty)   │ │  │
│ │ │ Card 4       │ │ (empty)   │ │  │
│ │ │ (empty)      │ │ (empty)   │ │  │
│ │ └──────────────┘ └───────────┘ │  │
│ │                                 │  │
│ └─────────────────────────────────┘  │
│ px-6                                 │
└─────────────────────────────────────┘
```

### Mobile (<768px): Review Deck (Swipeable)

```
VIEWPORT WIDTH: 375px (iPhone SE example)

┌──────────────────────────────┐
│ px-4 (16px)                   │
│ ┌────────────────────────────┐│
│ │ 👀 Aprovar posts           ││
│ │ Use este modo para decidir ││
│ │ uma a uma.                 ││
│ │ py-4, gap-3                ││
│ │ [Quadro] [Decidir ♥]  [👁️] ││
│ └────────────────────────────┘│
│ gap-3                         │
│ ┌────────────────────────────┐│
│ │ Stepper (may stack to 2-rows)│
│ │ ◉ Ideias ── ◯ Para ──     ││
│ │ ◯ Agendados ── ◯ Publicados ││
│ └────────────────────────────┘│
│ gap-6                         │
│ ┌────────────────────────────┐│
│ │ max-w-sm, mx-auto          ││
│ │ Review Deck (Pinned)       ││
│ │ ┌──────────────────────┐   ││
│ │ │ Para decidir (3)     │   ││
│ │ │                      │   ││
│ │ │   ┌──────────────┐   │   ││
│ │ │   │ [Card media] │   │   ││
│ │ │   │ aspect 4/3   │   │   ││
│ │ │   │              │   │   ││
│ │ │   │ Card Body    │   │   ││
│ │ │   │ "Post A"     │   │   ││
│ │ │   │ "Caption..." │   │   ││
│ │ │   │              │   │   ││
│ │ │   │[✓ Aprovar]   │   │   ││
│ │ │   │[✗ Não quero] │   │   ││
│ │ │   │              │   │   ││
│ │ │   └──────────────┘   │   ││
│ │ │ Card 1 of 3          │   ││
│ │ │ ◄ ─ Swipe ─ ►         │   ││
│ │ └──────────────────────┘   ││
│ └────────────────────────────┘│
│ px-4                          │
│                               │
│ [Toast notifications at floor]│
│ "Post aprovado ✓"            │
└──────────────────────────────┘
```

---

## G. Responsive Behavior Rules

### What Triggers Layout Mode Switching?

**JavaScript Breakpoint Hook:**
```javascript
import { useMediaQuery } from '@/hooks/useMediaQuery'; // or similar

const isMobile = useMediaQuery('(max-width: 767px)');
const isTablet = useMediaQuery('(min-width: 768px) and (max-width: 1023px)');
const isDesktop = useMediaQuery('(min-width: 1024px)');
```

- **Responsive listener:** Window resize triggers `useEffect` to recalculate breakpoint
- **State synced:** Current breakpoint stored in React state or passed via context
- **View mode auto-updated:** If user is in "Review" mode on desktop and resizes to mobile, view auto-switches to "Review deck" (or stays "Board" per user preference in localStorage)

---

### Mobile Gesture Model: Swipe vs. Drag

| Gesture | Desktop | Tablet | Mobile |
|---|---|---|---|
| **Hover** | ✓ Full shadow lift + scale | ✓ (if trackpad) | ✗ |
| **Click/Tap** | ✓ Open PostDetailModal | ✓ Open PostDetailModal | ✓ Open PostDetailModal |
| **Drag (desktop)** | ✓ Drag to column | ✗ (touch-friendly swipe alternative) | ✗ |
| **Swipe (mobile)** | ✗ | Partial (if in Board tab view) | ✓ Primary interaction (Review deck) |
| **Long-press** | ✗ | ✓ (optional context menu) | ✓ (optional context menu) |

---

### Auto-Switch: Review Mode on Mobile

**Current Implementation Rule (from 02-brief.md & evidence):**

- User lands on `/kanban` on **desktop** → Board view is selected by default
- User lands on `/kanban` on **mobile** → Review deck is selected by default
- User **manually switches** → Choice is stored in `localStorage` with key `kanban_viewMode`
- On **page reload**, view mode preference is restored from localStorage
- On **breakpoint resize** (e.g., desktop → mobile), view mode does NOT auto-switch unless viewport is first `sm` and user then scrolls/resizes to `lg`

**Rationale:** User intent trumps device. If user explicitly chose Board view on mobile, respect it on reload. If device changes drastically (unfolding phone to tablet), defer to user's explicit choice.

---

### Empty State Placement & Messaging

**Kanban column is empty if:**
- No posts in that status bucket exist in database, OR
- User has toggled "Hide Published" and published column is empty

**Empty state renders:**
- Inside the column container (below column header)
- Min-height: 180px (min-h-[180px])
- Centered emoji + headline + hint + optional CTA

**Column-specific empty messaging:**

| Column | Emoji | Headline | Hint | CTA |
|---|---|---|---|---|
| **Ideias salvas** | 📝 | "Comece a criar" | "Novas ideias aparecem aqui após serem salvas." | "Criar meu primeiro post" → `/create` |
| **Para decidir** | 👀 | "Fila vazia!" | "Assim que há novas ideias, elas aparecem para sua aprovação." | (None, or "Criar manualmente") |
| **Agendados** | 📅 | "Nada agendado" | "Após aprovar posts, você poderá agendar datas e horários." | (None) |
| **Publicados** | ✅ | "Missão cumprida! 🎉" | "Todos os posts foram publicados com sucesso." | (None, celebratory) |

**CTA routing:**
- "Criar meu primeiro post" on "Ideias salvas" → navigates to `/create?date=today` with no post ID (new post flow)
- No automatic navigation from other columns (user stays on kanban to decide)

---

## H. Implementation Checkpoints

Before moving to component specs (06-component-specs.md), verify:

- [ ] **Desktop board layout:** 4 columns visible ≥1024px, drag-drop enabled
- [ ] **Tablet layout:** 2-column grid (or single-column scrollable), decision documented
- [ ] **Mobile layout:** Review deck default (swipeable), Board tabs available
- [ ] **View mode toggle:** Both buttons visible in hero, toggle persists across reloads
- [ ] **Stepper:** 4 stages visible, current stage highlighted with accent bar
- [ ] **Column headers:** Status-dependent background colors applied (muted/50, warning/10, info/10, success/10)
- [ ] **Cards:** Rounded-2xl, gap-6 between cards, media aspect 4:3, body p-3
- [ ] **Approval buttons:** h-10 (44px min), full card width, flex row at bottom
- [ ] **Empty states:** Centered emoji + headline + hint, min-h-180px, dashed border
- [ ] **Gesture model:** Drag (desktop), Swipe (Review deck mobile), tap for modal
- [ ] **Responsive breakpoints:** lg:hidden for mobile, lg:flex for desktop
- [ ] **Touch targets:** All ≥44px in one dimension
- [ ] **Toasts:** Bottom-right desktop, bottom-center mobile
- [ ] **Modals:** PostDetailModal centered, dropdown positioned relative to trigger

---

## Summary: Key Layout Decisions

| Decision | Choice | Rationale |
|---|---|---|
| **Desktop columns** | 4-column grid, fixed 288px width | Maximizes visibility, matches kanban best practice |
| **Tablet layout** | 2-column grid (recommended) | Maintains scannability better than single-column scroll |
| **Mobile primary** | Review deck (swipeable) | Reduces cognitive load, optimized for touch, one decision at a time |
| **Hero hierarchy** | Title + subtitle + buttons full-width | Mobile first, then unifies hero across breakpoints |
| **Stepper reflow** | Stays 1-row, scrollable if needed | Persists workflow context across all breakpoints |
| **Card gap** | 24px (gap-6) vertical | Medium density, breathing room, premium feel |
| **Touch targets** | 44px minimum (h-10 buttons) | WCAG accessibility standard for coarse pointers |
| **Empty state CTA** | Routes to `/create` only on "Ideias salvas" | Prevents friction; other columns celebrate completion |
| **Gesture vocab** | Drag (desktop) + Swipe (mobile) + Tap (all) | Maximizes platform idioms, reduces cognitive switching |

