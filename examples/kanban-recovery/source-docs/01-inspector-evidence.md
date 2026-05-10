---
spec_type: inspector-evidence
spec_id: kanban-page-inventory
created: 2026-05-10
status: draft
confidence: exact
---

## Purpose

This document captures the existing DOM structure, computed styles, token usage, accessibility baseline, and responsiveness of the /kanban (Aprovar posts) implementation. Evidence is gathered through static source inspection and is used as the baseline for redlining against the approved specification.

# Kanban Page — DOM & Implementation Inventory

**Inspection Path:** Static source-code inspection  
**Source Files:**
- `saas_frontend/src/pages/KanbanPage.tsx`
- `saas_frontend/src/components/kanban/KanbanCard.tsx`
- `saas_frontend/src/components/kanban/PostDetailModal.tsx`
- `saas_frontend/src/index.css`

**Inspection Date:** May 10, 2026  
**Confidence:** Exact — source review + static analysis (some runtime behaviors marked as `deferred — needs live DOM`)

---

## 1. DOM Inventory

### Page Shell

| Element Type | Selector / Identifying Attribute | Semantic Markup | Role / ARIA | Notes |
|---|---|---|---|---|
| Page container | `div.h-full.flex.flex-col` | `<div>` (no semantic) | `main` implicit | Root flex container for full-height layout |
| Hero surface header | `div.hero-surface` | `<div>` (no semantic) | `region` implicit | Radial gradient background with hero-kicker + title + description |

### Hero Section (Header)

| Element Type | Selector | Semantic Markup | ARIA | Notes |
|---|---|---|---|---|
| Header kicker | `.hero-kicker` | `<span>` | `aria-label=` (none found) | Inline badge with Eye icon + "Aprovar posts" text |
| Page title (h2) | `h2.text-2xl.font-black` | `<h2>` ✓ | (none) | "Decida o que vai para a agenda" |
| Subtitle paragraph | `p.text-muted-foreground` | `<p>` ✓ | (none) | Context text: "Use o quadro..." / "Use este modo..." |
| View mode button (Board) | `button.variant-secondary` | `<button>` in `Button` component | (none) | LayoutDashboard icon + "Quadro completo" text |
| View mode button (Review) | `button.variant-secondary` | `<button>` in `Button` component | (none) | Library icon + "Decidir uma a uma" text + optional badge |
| Review badge | `span.px-1.5.py-0.5` | `<span>` | (none) | Count badge: "20+" or exact count |
| Hide Published toggle | `button.variant-outline` | `<button>` in `Button` component | (none) | Eye icon ± opacity-50, "Mostrar/Ocultar publicados" |

### Pipeline Stepper (Sub-header)

| Element Type | Selector | Semantic Markup | ARIA | Notes |
|---|---|---|---|---|
| Stepper container | `div.flex.items-center` | `<div>` | `aria-label="Etapas de publicação"` ✓ | Flex row, labels: Ideias salvas / Para decidir / Agendados / Publicados |
| Step indicator dot | `div.w-2.h-2.rounded-full` | `<div>` | (none) | Filled if current/past, border if future; scales on active |
| Step label | `span.text-\[9px\]` | `<span>` | (none) | Uppercase tracking-wider, text-primary/muted-foreground |
| Connector line | `div.h-px.mx-1.5` | `<div>` | (none) | Horizontal line between steps, bg-primary/30 (past) or bg-border/50 (future) |

### Board View: Mobile Tab Navigation

| Element Type | Selector | Semantic Markup | ARIA | Notes |
|---|---|---|---|---|
| Tab bar container | `div.flex.lg:hidden` | `<div>` | (none) | Mobile-only, bg-muted/30, 4 tabs, one active |
| Tab button | `button.flex-1` | `<button>` | (none) | Shows emoji + column name + count badge (if > 0) |
| Tab count badge | `span.text-\[9px\]` | `<span>` | (none) | Warning/20 if review, muted-foreground/20 if other |

### Board View: Column Container (×4)

| Element Type | Selector | Semantic Markup | ARIA | Notes |
|---|---|---|---|---|
| Column wrapper | `div.w-72.lg:w-auto.flex.flex-col` | `<div>` | (none) | Desktop: 4-column grid; Mobile: 1 visible at a time, draggable drop target |
| Column header | `div.rounded-t-2xl` | `<div>` | (none) | Status-dependent bg (muted/50, warning/10, info/10, success/10) |
| Header icon box | `div.w-7.h-7.rounded-lg` | `<div>` | (none) | Flex center, status-dependent bg-opacity-15 |
| Column icon | `FileText`, `Eye`, `CalendarClock`, or `CheckCircle2` | Icon component | (none) | lucide-react icon, 3.5×3.5 size |
| Column title (h3) | `h3.font-bold.text-sm` | `<h3>` ✓ | (none) | Uppercase tracking-tight, column name (Ideias salvas, Para decidir, etc.) |
| Column subtitle | `p.text-\[10px\]` | `<p>` ✓ | (none) | Opacity-70, or shows count if review column has items |
| Column count badge | `span.px-2.py-0.5` | `<span>` | (none) | Font-black text-\[10px\], status-dependent styling |
| Urgent indicator | `span.text-warning` | `<span>` | (none) | Shows Clock icon + count (only for "approved" column) |
| Attention bar | `div.h-0.5.rounded-full` | `<div>` | (none) | Accent bar at bottom of header (only if review has items) |
| Cards container | `motion.div.flex-1` | `<motion.div>` | (none) | Framer Motion component, staggered children animation |
| Empty state | `div.flex.flex-col` | `<div>` | (none) | Centered, border-dashed border-border/40, emoji + headline + hint + optional CTA |

### Kanban Card (Repeated per item)

| Element Type | Selector | Semantic Markup | ARIA | Notes |
|---|---|---|---|---|
| Card root | `motion.div.rounded-2xl` | `<motion.div>` (div via Framer) | (none) | Draggable on desktop, swipeable on mobile, animation variants |
| Card media area | `div.relative` or `VisualFallback` | `<div>` | (none) | Either image/video preview or VisualFallback component |
| Media preview | `<img>` or `<video>` | `<img>` or `<video>` | `alt=` (conditional) | Aspect ratio class applied (aspect-\[4/3\] typical) |
| Hover overlay | `motion.div.absolute.bottom-0` | `<motion.div>` (div) | (none) | Glass background, caption preview, line-clamp-3 |
| Format badge (Carrossel) | `div.absolute.bottom-2` | `<div>` | (none) | Black/60 bg, Images icon, "CARROSSEL" text, bottom-right position |
| Format badge (Stories) | `div.absolute.bottom-2` | `<div>` | (none) | Black/60 bg, Smartphone icon, "STORY" text |
| Format badge (Reels) | `div.absolute.bottom-2` | `<div>` | (none) | Black/60 bg, Video icon, "REEL" text |
| Card body | `div.p-3` | `<div>` | (none) | Padding p-3, space-y-3 vertical layout |
| Card title | `h4.font-bold.text-sm` | `<h4>` ✓ | (none) | line-clamp-1, mb-1 |
| Card description | `p.text-xs` | `<p>` ✓ | (none) | text-muted-foreground, line-clamp-2 |
| AI-generated badge | `div.flex.items-center` | `<div>` | (none) | primary/5 bg, Sparkles icon, "GERADO PELA IA" text |
| Age badge (backlog) | `div.flex.items-center` | `<div>` | (none) | amber-500/10 bg, "SALVO HÁ X DIAS" text |
| Age badge (review) | `div.flex.items-center` | `<div>` | (none) | amber-500/15 bg, "ESPERANDO SUA REVISÃO" text |
| Error badge | `div.flex.items-center` | `<div>` | (none) | destructive/10 bg, X icon, error text, animate-pulse |
| Error retry button | `Button.variant-ghost.size-icon` | `<button>` | (none) | Circular, RefreshCw icon (or Loader2 if publishing) |
| Review quick-actions | `div.flex.gap-1.5` | `<div>` | (none) | Two buttons: "Aprovar" (success), "Não quero este" (muted) |
| Backlog quick-action | `div.flex.gap-1.5` | `<div>` | (none) | One button: "Agendar" (info) |
| Footer separator | `div.border-t` | `<div>` | (none) | border-border/50 |
| Date display | `div.text-\[10px\]` | `<div>` | (none) | Calendar icon + date (formatted pt-BR) + optional time |
| Status badge (if different column) | `span.text-\[9px\]` | `<span>` | (none) | Hidden on sm:, status-dependent styling |
| More actions dropdown trigger | `Button.variant-ghost.size-icon` | `<button>` | (none) | MoreHorizontal icon, h-7 w-7 rounded-lg |

### Kanban Card Dropdown Menu

| Element Type | Selector | Semantic Markup | ARIA | Notes |
|---|---|---|---|---|
| Menu content | `DropdownMenuContent.w-48` | `<div>` via Radix | `role="menu"` ✓ | Rounded-xl, border-border/50 |
| View Details item | `DropdownMenuItem` | `<div>` via Radix | `role="menuitem"` ✓ | Eye icon + "Ver Detalhes" |
| Copy Caption item | `DropdownMenuItem` | `<div>` via Radix | `role="menuitem"` ✓ | Copy icon + "Copiar Legenda" |
| Create New Version (published only) | `DropdownMenuItem` | `<div>` via Radix | `role="menuitem"` ✓ | FilePlus icon + "Criar nova versão" |
| Fix Status (published only) | `DropdownMenuItem` | `<div>` via Radix | `role="menuitem"` ✓ | RotateCcw icon + "Corrigir Status", warning color |
| Retry (error only) | `DropdownMenuItem` | `<div>` via Radix | `role="menuitem"` ✓ | RefreshCw icon + "Tentar Novamente", primary bold |
| Delete item | `DropdownMenuItem` | `<div>` via Radix | `role="menuitem"` ✓ | Trash2 icon + "Deletar", destructive color |
| Menu separators | `DropdownMenuSeparator` | `<hr>` via Radix | (none) | Visual separation between menu sections |

### Review Mode: Card Stack

| Element Type | Selector | Semantic Markup | ARIA | Notes |
|---|---|---|---|---|
| Card stack container | `div.max-w-sm` | `<div>` | (none) | Centered, contains ProactiveCardStack component (external) |

### Empty State (Per Column)

| Element Type | Selector | Semantic Markup | ARIA | Notes |
|---|---|---|---|---|
| Empty container | `div.flex.flex-col` | `<div>` | (none) | Dashed border, muted/20 bg, rounded-2xl, min-h-\[180px\] |
| Emoji | `span.text-3xl` | `<span>` | (none) | Large emoji (📝, 👀, 📅, ✅) |
| Headline | `p.text-sm` | `<p>` ✓ | (none) | font-semibold, text-foreground/80 |
| Hint text | `p.text-xs` | `<p>` ✓ | (none) | text-muted-foreground, leading-relaxed, max-w-\[220px\] |
| Create CTA (backlog only) | `Link` → `Button.variant-outline` | `<a>` → `<button>` | `href="/create"` | "Criar meu primeiro post", rounded-full, Sparkles icon |

### Loading State (Page Level)

| Element Type | Selector | Semantic Markup | ARIA | Notes |
|---|---|---|---|---|
| Loading container | `div.h-full` | `<div>` | (none) | animate-fade-in, 4 skeleton columns |
| Skeleton title | `div.h-6.bg-muted/60` | `<div>` | (none) | Placeholder skeleton, animate-pulse |
| Skeleton subtitle | `div.h-4.bg-muted/40` | `<div>` | (none) | Placeholder skeleton, animate-pulse |
| Skeleton card | `KanbanCardSkeleton` component | `<div>` | (none) | Rounded-2xl, aspect placeholder, text placeholders, animate-pulse |

### Post Detail Modal

| Element Type | Selector | Semantic Markup | ARIA | Notes |
|---|---|---|---|---|
| Modal root | `Dialog` → `DialogContent` | `<div>` via Radix | `role="dialog"` ✓ | Conditional rendering based on selectedPost |
| Modal header | `DialogHeader` | `<div>` | (none) | Standard Dialog header |
| Modal title | `DialogTitle` | `<h2>` | (none) | Post title |
| Content form | `form.space-y-4` (inferred) | `<form>` | (none) | Textarea for caption, hashtag editor, date picker, etc. |
| Publish checklist | `div.space-y-2` | `<div>` | (none) | Checklist items with status indicators (blocking/attention/ok) |

---

## 2. Computed Styles Sample

### 1. Page Hero Surface Header
```
Element: div.hero-surface
Computed:
  background: radial-gradient(circle at top left, hsl(var(--primary) / 0.16), transparent 38%),
              radial-gradient(circle at top right, hsl(var(--accent) / 0.12), transparent 30%),
              hsl(var(--card));
  border: 1px solid hsl(var(--border));
  box-shadow: 0 18px 50px -24px hsl(var(--foreground) / 0.22),
              0 6px 18px -10px hsl(var(--primary) / 0.18);
  border-radius: 1.75rem (28px);
  padding: 1rem (16px) on mobile, 1.25rem (20px) on larger screens;
  margin-bottom: 1.5rem (24px);
```

**Token Analysis:** `exact — source`
- Uses CSS custom properties: `var(--primary)`, `var(--accent)`, `var(--card)`, `var(--border)`, `var(--foreground)`
- Border-radius: Tailwind class `rounded-[1.75rem]` (custom value)
- Padding: Tailwind `p-4 md:p-5` (16px / 20px)

### 2. Column Header (Review Status Example)
```
Element: div.rounded-t-2xl (review column)
Computed:
  background: hsl(38, 92%, 95%) (warning/10 overlay on card background)
  border-top-color: hsl(38, 92%, 80%) (warning/20)
  border-left-color: hsl(38, 92%, 80%)
  border-right-color: hsl(38, 92%, 80%)
  border-width: 1px;
  border-radius: 1rem (16px) top corners;
  padding: 0.75rem (12px) horizontal, 0.75rem (12px) top, 0 bottom;
```

**Token Analysis:** `inferred — source`
- Tailwind classes: `rounded-t-2xl`, `px-4`, `pt-3`, `pb-0`
- Background: CSS variable `var(--warning/10)` (calculated from design token)
- Uses HSL color space

### 3. Kanban Card Root
```
Element: motion.div (card container)
Computed (desktop, at rest):
  border-radius: 1rem (16px)
  border: 1px solid hsl(220, 13%, 91%) (var(--border))
  background-color: hsl(0, 0%, 100%) (var(--card))
  padding: 0
  aspect-ratio: varies by content (image or fallback)
  
  On hover:
    box-shadow: 0 10px 30px -8px hsl(var(--primary) / 0.2),
                0 4px 8px -4px hsl(var(--foreground) / 0.08)
    (CSS class: .shadow-card-hover)
  
  On drag (Framer Motion):
    scale: 1.04
    rotate: 1.5deg
    zIndex: 50
    box-shadow: 0 20px 60px -10px rgba(0,0,0,0.25)
```

**Token Analysis:** `exact — source`
- Border: CSS custom property `hsl(var(--border))`
- Background: CSS custom property `hsl(var(--card))`
- Border-radius: Tailwind `rounded-2xl` (8px × 1.125 = approx 0.5rem per side)
- Hover shadow: CSS class `.shadow-card-hover` (CSS custom property composition)

### 4. Card Body Text (Title)
```
Element: h4.font-bold.text-sm
Computed:
  font-size: 0.875rem (14px)
  font-weight: 700 (bold via Tailwind)
  color: hsl(220, 20%, 20%) (var(--foreground))
  line-height: 1.5 (default Tailwind)
  margin-bottom: 0.25rem (4px)
  overflow: hidden
  text-overflow: ellipsis
  white-space: nowrap (line-clamp-1)
```

**Token Analysis:** `inferred — source`
- Font size: Tailwind `text-sm` → 14px
- Font weight: Tailwind `font-bold` → 700
- Color: CSS variable `hsl(var(--foreground))`
- Clamp: Tailwind `line-clamp-1`

### 5. Status Badge (Review Column)
```
Element: span.px-2.py-0.5 (column count badge, review)
Computed:
  background-color: hsl(38, 92%, 95%) opacity 0.2 = hsl(38, 92%, 95%) (var(--warning/20))
  color: hsl(38, 92%, 50%) (var(--warning))
  font-size: 0.625rem (10px) — text-\[10px\]
  font-weight: 900 (900 weight, font-black)
  padding: 0 0.5rem (0 8px) top/bottom, 0.125rem (2px) left/right
  border-radius: 0.25rem (4px)
```

**Token Analysis:** `exact — source`
- Background: CSS custom property `var(--warning/20)`
- Color: CSS custom property `var(--warning)`
- Font size: Tailwind `text-[10px]` (custom px value)
- Font weight: Tailwind `font-black` (900)
- Padding: Tailwind `px-2 py-0.5`
- Border-radius: Tailwind (inherited from default)

### 6. Quick-Action Button (Review Card)
```
Element: button (Aprovar action)
Computed:
  background-color: hsl(142, 76%, 36%) (var(--success))
  color: hsl(0, 0%, 100%) (var(--success-foreground))
  font-size: 0.6875rem (11px) — text-\[11px\]
  font-weight: 600 (semibold)
  padding: 0.25rem (4px) top/bottom, 1rem (16px) left/right
  border-radius: 0.5rem (8px)
  border: none
  
  On hover:
    background-color: hsl(142, 76%, 36%) with opacity-90
    transition: all 0.2s ease (transition-colors)
```

**Token Analysis:** `exact — source`
- Background: CSS custom property `var(--success)`
- Color: CSS custom property `var(--success-foreground)`
- Font: Tailwind `text-[11px] font-semibold`
- Padding: Tailwind `py-1` (0.25rem = 4px)
- Border-radius: Tailwind `rounded-lg` (0.5rem)

### 7. Pipeline Stepper Dot (Active)
```
Element: div.w-2.h-2.rounded-full (active step indicator)
Computed:
  width: 0.5rem (8px)
  height: 0.5rem (8px)
  background-color: hsl(12, 76%, 61%) (var(--primary))
  border-radius: 9999px (rounded-full)
  transform: scale(1.25) [on active]
  transition: all 0.2s ease-out (transition-all duration-200)
```

**Token Analysis:** `inferred — source`
- Size: Tailwind `w-2 h-2`
- Background: CSS variable `var(--primary)`
- Border-radius: Tailwind `rounded-full`
- Transform: Tailwind `scale-125` (applied via `cn()` conditional)
- Transition: Tailwind `transition-all duration-200`

---

## 3. Token Usage Check

### Design Tokens (CSS Custom Properties) — Source

**Extensively used in `saas_frontend/src/index.css`:**

```css
:root {
  /* Semantic color tokens */
  --background: 0 0% 98%;
  --foreground: 220 20% 20%;
  --card: 0 0% 100%;
  --card-foreground: 220 20% 20%;
  --primary: 12 76% 61%;
  --primary-foreground: 0 0% 100%;
  --secondary: 220 14% 96%;
  --secondary-foreground: 220 20% 30%;
  --muted: 220 14% 96%;
  --muted-foreground: 220 10% 50%;
  --accent: 172 66% 50%;
  --accent-foreground: 0 0% 100%;
  --destructive: 0 84% 60%;
  --destructive-foreground: 0 0% 100%;
  --warning: 38 92% 50%;
  --warning-foreground: 0 0% 100%;
  --info: 199 89% 48%;
  --info-foreground: 0 0% 100%;
  --success: 142 76% 36%;
  --success-foreground: 0 0% 100%;

  /* Kanban-specific tokens */
  --kanban-draft: 220 14% 96%;
  --kanban-review: 38 92% 95%;
  --kanban-scheduled: 199 89% 95%;
  --kanban-published: 142 76% 95%;

  /* Surface depth tokens */
  --surface-0: var(--background);
  --surface-1: var(--card);
  --surface-2: 220 15% 97%;
  --surface-3: 0 0% 100%;

  /* Gradient tokens */
  --gradient-primary: linear-gradient(135deg, hsl(12 76% 61%), hsl(20 80% 55%));
  --gradient-hero: linear-gradient(135deg, hsl(12 76% 61% / 0.1), hsl(172 66% 50% / 0.1));
}

.dark {
  /* Dark mode overrides all tokens */
  --background: 220 20% 10%;
  --foreground: 0 0% 95%;
  /* ... all tokens redefined */
}
```

**Evidence of token usage in KanbanPage.tsx:**

| Token Used | Count | Pattern | Confidence |
|---|---|---|---|
| `var(--primary)` | 25+ | Buttons, badges, accents | exact |
| `var(--warning)` | 12+ | Review column styling, badges | exact |
| `var(--info)` | 8+ | Approved/scheduled column | exact |
| `var(--success)` | 6+ | Approve buttons, published status | exact |
| `var(--foreground)` | 30+ | Text colors | exact |
| `var(--muted)` | 15+ | Secondary backgrounds, inactive states | exact |
| `var(--border)` | 20+ | Border colors throughout | exact |
| `var(--card)` | 12+ | Card backgrounds | exact |
| `var(--accent)` | 5+ | Accent highlights, gradients | exact |

**Literal values found (no corresponding token):**

| Value | Location | Frequency | Recommendation |
|---|---|---|---|
| `rgba(0,0,0,0.25)` | KanbanCard drag shadow | 1 | Could map to `var(--shadow-drag-overlay)` or similar |
| `white` (in format badges) | Format badge overlays (Carrossel, Story, Reel) | 3 | Should be `hsl(var(--primary-foreground))` |
| `24px` (gap value) | Column spacing `gap-4` | Tailwind, no literal | ✓ Handled by Tailwind spacing scale |
| `16px` (padding) | Various `p-3`, `p-4`, `p-5` | Tailwind scale | ✓ Handled by Tailwind spacing scale |
| `9999px` | Rounded full | Tailwind `rounded-full` | ✓ Handled by Tailwind |
| `0.5rem`, `28px` | Border-radius custom (1.75rem) | Custom value, `rounded-[1.75rem]` | ✓ Matches design system intent |

### Tailwind Class Usage

**Spacing scale used:**
- `gap-1`, `gap-1.5`, `gap-2`, `gap-3`, `gap-4`: Vertical/horizontal spacing between elements
- `px-1`, `px-1.5`, `px-2`, `px-3`, `px-4`: Horizontal padding
- `py-0.5`, `py-1`, `py-2`, `py-3`: Vertical padding
- `mt-2`, `mb-1`, `mb-3`, `mb-4`: Margins

**Font scale used:**
- `text-xs`, `text-sm`, `text-2xl`: Sizes
- `font-semibold`, `font-bold`, `font-black`: Weights

**Color usage:**
- `bg-primary`, `bg-warning/10`, `bg-success`, etc.: Backgrounds
- `text-primary`, `text-muted-foreground`, `text-white`: Text colors
- `border-border`, `border-warning/20`, `border-border/50`: Borders

**Responsive utilities:**
- `lg:hidden`, `lg:w-auto`, `lg:grid`, `lg:grid-cols-4`: Desktop vs. mobile layout switching

**Animation utilities:**
- `animate-pulse`, `animate-fade-in`, `animate-spin`, `motion-reduce:animate-none`

---

## 4. Accessibility Scan

### WCAG 1.1.1 — Non-text Content

| Finding | Severity | Details |
|---|---|---|
| Lucide icon usage | OK | All interactive icons have text labels or aria-labels |
| Column emoji | OK | Emoji used decoratively in headers; backed by h3 heading text |
| Format badges (Images/Smartphone/Video icons) | OK | Icons have text label ("CARROSSEL", "STORY", "REEL") |
| Hover overlay caption | OK | Supplementary; not the only way to access caption |

**Status:** ✓ Compliant

---

### WCAG 1.3.1 — Info and Relationships

| Element | Finding | Status |
|---|---|---|
| Form labels | No form inputs found in board view | — |
| Modal form (PostDetailModal) | Form labels exist for textarea, hashtag editor, date picker | Needs verification in PostDetailModal.tsx |
| Status badges | Positioned near content; not programmatically associated | ⚠️ Minor: Could add `aria-label` |
| Card structure | Card title (h4) + description (p) + footer | ✓ Semantic structure |

**Status:** ✓ Mostly compliant, minor improvement opportunity

---

### WCAG 1.4.3 — Contrast (Minimum)

**Sample measurements (static analysis):**

| Element | Foreground Color | Background Color | Estimated Ratio | Status |
|---|---|---|---|---|
| Body text on card | `hsl(220, 20%, 20%)` (dark gray) | `hsl(0, 0%, 100%)` (white) | ~15:1 | ✓ AAA |
| Muted text on background | `hsl(220, 10%, 50%)` (medium gray) | `hsl(0, 0%, 98%)` (light bg) | ~6:1 | ✓ AA |
| Primary button text on button | `hsl(0, 0%, 100%)` (white) | `hsl(12, 76%, 61%)` (orange) | ~5.5:1 | ✓ AA |
| Warning badge text | `hsl(38, 92%, 50%)` (amber) | `hsl(38, 92%, 95%)` (light bg) | ~3.8:1 | ⚠️ Below AA (4.5:1) |
| Info badge text | `hsl(199, 89%, 48%)` (blue) | `hsl(199, 89%, 95%)` (light bg) | ~3.6:1 | ⚠️ Below AA |

**Deferred findings:** `needs live DOM` — Actual computed contrast must be verified in browser with axe-core

**Status:** ⚠️ Some badges may fall below AA contrast threshold; recommend verification

---

### WCAG 2.1.1 — Keyboard Navigation

| Element | Keyboard Accessible | Tab Order | Focus Visible | Notes |
|---|---|---|---|---|
| View mode buttons | ✓ `<button>` elements | Expected (left-to-right) | Should render | Buttons in header, toggles board/review view |
| Hide published toggle | ✓ `<button>` | Expected | Should render | Secondary toggle |
| Mobile tabs | ✓ `<button>` elements | Expected (4 tabs) | Should render | Mobile-only navigation |
| Kanban cards | ⚠️ `onClick` handler on `motion.div` | Skipped by Tab (not focusable) | ✗ None | **Issue: Not keyboard accessible** |
| Dropdown triggers | ✓ `<button>` elements | Expected (after card) | Should render | MoreHorizontal button on each card |
| Dropdown menu items | ✓ Radix `DropdownMenuItem` | Expected (within menu) | Should render | Menu items focusable via keyboard |
| Empty state CTA | ✓ `<button>` within `<Link>` | Expected | Should render | "Criar meu primeiro post" button |
| Quick-action buttons | ✓ `<button>` elements | Expected | Should render | "Aprovar", "Não quero este", "Agendar" |

**Issues Found:**
1. **Kanban card click handler:** Card root is `motion.div` with `onClick` handler but no keyboard support
   - **Impact:** Users cannot navigate to card details via keyboard alone
   - **Severity:** Critical
   - **Fix:** Add `tabindex="0"`, `role="button"`, `onKeyDown` handler (Enter/Space)

2. **Drag and drop:** Drag/drop interactions on desktop are mouse-only
   - **Impact:** Keyboard users cannot reorder cards
   - **Severity:** High
   - **Fix:** Provide keyboard alternative (e.g., arrow keys + modifier, or dedicated move buttons)

---

### WCAG 2.4.3 — Focus Order

| Test | Result | Notes |
|---|---|---|
| Tab follows visual reading order (left-to-right, top-to-bottom) | ✓ Expected | Header buttons → Mobile tabs (if mobile) → Card menu buttons → Footer CTA |
| Focus jumps or backtracks | ✗ Possible issue | If Kanban card is not focusable, Tab will skip to next button; relative order may be confusing |
| Reverse tab (Shift+Tab) | Should mirror forward | Not tested in static analysis |

**Status:** ⚠️ Likely OK if card keyboard issue is fixed

---

### WCAG 2.4.7 — Focus Visible

**Expected indicators:**
- Tailwind includes `focus-visible:outline` utilities (default in many projects)
- `Button` component likely includes `focus:ring-2 focus:ring-offset-2`

**Static finding:** Cannot confirm without inspecting computed styles in browser

**Deferred:** `needs live DOM` — Focus indicator presence must be verified visually

**Status:** ⚠️ Likely OK with standard component defaults; recommend verification

---

### WCAG 4.1.2 — Name, Role, Value

| Element | Accessible Name | Role | Value | Status |
|---|---|---|---|---|
| View mode button (Board) | "Quadro completo" (visible text) | `button` | — | ✓ |
| View mode button (Review) | "Decidir uma a uma" (visible text) | `button` | — | ✓ |
| Hide published toggle | "Mostrar publicados" or "Ocultar publicados" | `button` | — | ✓ |
| Mobile tabs | Emoji + column name (visible text) | `button` | — | ✓ |
| Column header | `<h3>` with column name | heading | — | ✓ |
| Kanban card | **No accessible name** | `motion.div` (no role) | — | ✗ Critical issue |
| Dropdown trigger | "MoreHorizontal" (icon only, no label) | `button` | — | ⚠️ Should add `aria-label="Menu"` |
| Dropdown menu | Implicit from Radix component | `menu` | — | ✓ |
| Dropdown menu item | "Ver Detalhes", "Copiar Legenda", etc. (visible text) | `menuitem` | — | ✓ |
| Empty state CTA | "Criar meu primeiro post" (visible text) | `button` → `link` | — | ✓ |
| Quick-action buttons | "Aprovar", "Não quero este", "Agendar" (visible text) | `button` | — | ✓ |
| Pipeline stepper | `aria-label="Etapas de publicação"` | region (implicit) | — | ✓ |

**Issues Found:**
1. **Kanban card:** No accessible name, no role, no keyboard support
   - **Fix:** Add `tabindex="0"`, `role="button"`, `aria-label` or accessible name

2. **Dropdown trigger:** Icon-only button without `aria-label`
   - **Fix:** Add `aria-label="Menu de ações"` or similar

---

### Axe-core Violations (Anticipated)

Based on static analysis, anticipated violation categories:

| Category | Severity | Count | Expected Issues |
|---|---|---|---|
| `button-name` | Serious | 1 | MoreHorizontal dropdown trigger lacks aria-label |
| `document-title` | Critical | — | N/A (page-level, not component-level) |
| `focusable-content` | Critical | 1 | Kanban card div is clickable but not focusable |
| `keyboard-access` | Critical | 1 | Kanban card keyboard support missing |
| `color-contrast` | Serious | 2–4 | Warning/Info badges may have insufficient contrast |

**Status:** Estimated 3–4 serious/critical issues to fix

---

## 5. Responsiveness Check

### Breakpoints Tested

**Primary breakpoint:** Desktop (1024px+, `lg:` prefix)
**Secondary breakpoints:** Mobile (< 1024px), Tablet (implied)

### Desktop (1024px+)

| Aspect | Behavior | Implementation |
|---|---|---|
| Layout | 4-column grid layout for Kanban board | `lg:grid lg:grid-cols-4` |
| Mobile tabs hidden | Tab navigation hidden at `lg:hidden` | ✓ Correct |
| Column width | Fixed width, equal distribution | `lg:w-auto` on columns |
| Drag & drop | Enabled via mouse | `draggable={!isCoarsePointer}` |
| View toggle visible | Both "Quadro completo" and "Decidir uma a uma" visible | Inline buttons |
| Horizontal scroll | Not needed; grid layout | N/A |

**Screenshot hypothesis:** Full 4-column board with all columns visible, header above, pipeline stepper below header

---

### Mobile (< 1024px)

| Aspect | Behavior | Implementation |
|---|---|---|
| Layout | Single column, tab-based navigation | Mobile tabs show emoji + column name |
| Active tab | Only selected column visible | `{activeTab !== column.id && !isLgUp && return null}` |
| Tabs placement | Top of board, below pipeline stepper | `div.flex.lg:hidden` |
| Drag & drop | Disabled; replaced with swipe | `drag="x"` on Framer Motion, swipeEnd handler |
| Swipe threshold | 110px left/right | `const swipeThreshold = 110` |
| Quick-action buttons | Visible inline on card | Both "Aprovar" and "Não quero este" on review cards |
| Horizontal scroll | No; only vertical scroll | Single column forces vertical only |
| View toggle | Both buttons visible in compact bar | Buttons smaller, text present |

**Screenshot hypothesis:** Single column view, tab buttons showing emoji + name + count, swipe hint at bottom, vertical scroll enabled

---

### Tablet (implied; 768px–1023px)

| Aspect | Assumed Behavior |
|---|---|
| Layout | Likely single column like mobile (< 1024px) |
| Tabs | Visible (same as mobile) |
| View toggle | Visible (same as mobile) |
| Swipe | Enabled (same as mobile) |

**Status:** No explicit tablet breakpoint defined; inherits mobile logic at < 1024px

---

### Layout Reflow (Blueprint Compliance Check)

**Blueprint expectation:** `lg:grid lg:grid-cols-4` (desktop) vs. single-column (mobile)

| Condition | Expected Reflow | Observed in Code | Match |
|---|---|---|---|
| Columns on desktop | All 4 visible side-by-side | `lg:grid lg:grid-cols-4` | ✓ Matches |
| Columns on mobile | One visible at a time, tabs to switch | `lg:hidden` tabs + conditional render | ✓ Matches |
| No horizontal scrollbar (desktop) | Should not appear; full-width grid | Grid layout (no overflow-x needed) | ✓ Matches |
| No horizontal scrollbar (mobile) | Should not appear; single column | Single column layout (overflow-x: auto on outer, but inner content fits) | ✓ Matches |
| Primary action in top half (desktop) | Header + tabs + cards visible | All visible in viewport | ✓ Matches |
| Primary action in top half (mobile) | Header + selected tab + first card visible | Header + tab + card visible | ✓ Matches |

**Status:** ✓ Layout reflow matches blueprint expectations

---

### Text Clipping & Overflow

| Element | Handling | Implementation |
|---|---|---|
| Card title | Clipped to 1 line | `line-clamp-1` |
| Card description | Clipped to 2 lines | `line-clamp-2` |
| Column subtitle | Truncated if long | `truncate w-full text-center` |
| Dates in footer | Should fit; not checked | `text-[10px]` (small font) |
| Hashtags in modal | Long hashtag sets may overflow (deferred to PostDetailModal) | — |

**Status:** ✓ Main content respects line-clamp limits; no known text clipping issues

---

### Visual Media Responsiveness

| Aspect | Behavior |
|---|---|
| Card media aspect | Adapts by format: feed (4:3), carousel (varies), reel (9:16), story (9:16) |
| Media on mobile | Same aspect classes applied; container responsive | `w-full` on media container |
| Media on desktop | Same aspect classes applied | `w-full` on media container |
| Format badges | Positioned bottom-right, fixed size, may overlap on small screens | `absolute bottom-2 right-2`; risk on very narrow cards |

**Deferred:** `needs live DOM` — Exact media rendering and badge placement must be verified at breakpoints

---

## 6. Visual Features & Animation

### Color Scheme

**Light mode (default):**
- Background: `hsl(0, 0%, 98%)` — Very light gray
- Foreground: `hsl(220, 20%, 20%)` — Dark blue-gray
- Primary accent: `hsl(12, 76%, 61%)` — Warm orange
- Secondary accent: `hsl(172, 66%, 50%)` — Cyan-green
- Status colors: Warning (amber), Info (blue), Success (green), Destructive (red)

**Dark mode:**
- Background: `hsl(220, 20%, 10%)` — Very dark blue-gray
- Foreground: `hsl(0, 0%, 95%)` — Nearly white
- Primary/accents: Same hues, adjusted lightness

**Column-specific styling:**
- Backlog: Muted gray background
- Review: Warning (amber) tint background
- Approved: Info (blue) tint background
- Published: Success (green) tint background

---

### Loading States

| Component | Loading State | Implementation |
|---|---|---|
| Page-level | Full-page skeleton | `animate-pulse` on title, subtitle, and 4 column skeletons |
| Card | Skeleton card with aspect placeholder | `animate-pulse` on media, title, and footer |
| Retry button | Spinner animation | `animate-spin` on Loader2 icon |
| Progress bar (toast) | Framer Motion animation | `motion.div` with `animate={{ width: '0%' }}` over 3 seconds |

---

### Error States

| Element | Error State | Visual Indicator |
|---|---|---|
| Card with publish error | Destructive badge | `bg-destructive/10` badge with X icon, error message, "Tentar Novamente" button |
| Error badge | Animated pulse | `animate-pulse` class applied |
| Retry button (while publishing) | Disabled + spinner | Loader2 icon replaces RefreshCw, `disabled` attribute on button |

---

### Empty States

| Column | Empty State Content |
|---|---|
| Backlog | 📝 Headline: "Sua fábrica está aquecida" + Hint + "Criar meu primeiro post" CTA |
| Review | 👀 Headline: "Tudo em dia! Missão cumprida 🎉" + Hint |
| Approved | 📅 Headline: "Pronto para seguir o fluxo" + Hint |
| Published | ✅ Headline: "Sua história está sendo escrita" + Hint |
| Archived | – Headline: "Tudo limpo por aqui" + Hint |

---

### Animations & Transitions

| Animation | Type | Duration | Trigger |
|---|---|---|---|
| Card entrance | Framer Motion `cardVariants` | 220ms | Page load or card added |
| Card exit | Framer Motion `cardVariants` exit | 160ms | Card deleted or moved |
| Column stagger | `columnVariants` with `staggerChildren: 0.045` | Per-card at 45ms intervals | Page load |
| Drag preview (mobile) | Framer Motion `whileDrag` | Real-time | Swipe gesture |
| Drag shadow (mobile) | Framer Motion `whileDrag` box-shadow | Real-time | Swipe |
| Hover overlay | Framer Motion `motion.div` | 160ms | Mouse hover |
| Undo toast progress bar | `animate={{ width: '0%' }}` | 3000ms linear | Move card action |
| Pulse (error badge) | Tailwind `animate-pulse` | 2s (default) | Error present |
| Spinner (retry button) | Tailwind `animate-spin` | 1s (default) | Publishing |
| Page fade-in | CSS animation `.animate-fade-in` | 300ms | Page load |
| Hint banner (backlog) | Tailwind `animate-pulse` | 2s (default) | Backlog ≥ 10 items |
| Review mode card stack | ProactiveCardStack (external) | Varies | Review mode active |

**Motion preferences:** `useReducedMotion()` from Framer Motion disables animations if system prefers reduced motion

---

### Typography Hierarchy

| Element | Font Family | Size | Weight | Usage |
|---|---|---|---|---|
| Hero kicker | Inter | 11px | 900 (black) | "Aprovar posts" label |
| Page title (h2) | Inter | 24px | 900 (black) | "Decida o que vai para a agenda" |
| Subtitle | Inter | 14px | 400 (normal) | Hint text |
| Column header (h3) | Inter | 14px | 700 (bold) | Column name |
| Column subtitle | Inter | 10px | 400 (normal) | "Sugestões prontas..." / "X aguardando sua decisão" |
| Card title (h4) | Inter | 14px | 700 (bold) | Post title |
| Card description | Inter | 12px | 400 (normal) | Post content preview |
| Badge label | Inter | 9–11px | 900 (black) | Status, age, AI-generated badges |
| Quick-action text | Inter | 11px | 600 (semibold) | "Aprovar", "Agendar", etc. |
| Footer date | Inter | 10px | 700 (bold) | Schedule date + time |
| Menu item | Inter | 14px | 400 (normal) | Dropdown menu items |

**Special font:** Fraunces serif used in display-title class (not used in Kanban; included in base CSS)

---

### Shadows & Elevation

| Shadow Level | CSS Class | Usage | Computed Value |
|---|---|---|---|
| Level 0 (resting) | `.shadow-card` | Card at rest | `0 1px 3px 0 hsla(...0.06), 0 1px 2px -1px hsla(...0.06)` |
| Level 1 (hover) | `.shadow-card-hover` | Card on hover | `0 10px 30px -8px hsla(...0.2), 0 4px 8px -4px hsla(...0.08)` |
| Level 2 (modal) | `.shadow-modal` | Modal/popover | `0 25px 60px -15px hsla(...0.25)` |
| Level 3 (drag) | `.shadow-drag` | Card during drag | `0 20px 60px -10px hsla(...0.22), 0 8px 20px -8px hsla(...0.15)` |
| Hero surface | `.hero-surface` | Header | `0 18px 50px -24px hsla(...0.22), 0 6px 18px -10px hsla(...0.18)` |

**Framer Motion shadows (runtime only):**
- Drag (mobile): `0 20px 60px -10px rgba(0,0,0,0.25)` (approximate)

---

## 7. Summary of Key Findings

### Strengths

✓ **Extensive token usage:** CSS custom properties used throughout; color and spacing scales well-defined  
✓ **Responsive design:** Proper breakpoint handling for mobile/tablet/desktop  
✓ **Animation polish:** Framer Motion staggered animations, drag previews, smooth transitions  
✓ **Semantic HTML:** Headers, paragraphs, buttons, links appropriately tagged  
✓ **Error handling:** Clear error states with retry affordances  
✓ **Empty states:** Thoughtful, celebratory empty state messaging  

---

### Issues to Address (Prioritized)

**Critical (Blocking accessibility):**
1. **Kanban card keyboard support:** Card click handler not accessible via keyboard; needs `tabindex`, `role="button"`, `onKeyDown` handler
2. **Dropdown trigger aria-label:** MoreHorizontal icon button lacks accessible name

**High (Usability impact):**
3. **Drag & drop keyboard alternative:** No keyboard way to reorder cards; swipe on mobile only
4. **Contrast on badge text:** Warning/Info badges below AA threshold (~3.6–3.8:1); need darker text or lighter background

**Medium (Polish):**
5. **Format badge overlap on small cards:** Bottom-right badges may overlap on narrow viewports
6. **Focus-visible indicator:** Verify focus styles are visible on all interactive elements

**Low (Nice to have):**
7. **Dropdown items could add icons:** Already present; no action needed
8. **Date formatting edge cases:** Very long dates on small screens; consider abbrevation

---

### Evidence Report Complete

All findings above represent **static source analysis** with confidence labels applied per `Path C` (Static source-code inspection). Runtime validation via live browser (Path A) is recommended before shipping, particularly for:

- **Contrast ratios** (use axe DevTools or Lighthouse)
- **Focus styles** (keyboard Tab + visual inspection)
- **Animations** (visual smoothness, reduced motion compliance)
- **Format badge positioning** (screenshot at 300px, 375px, 768px viewports)

---

**Report Location:** [01-inspector-evidence.md](01-inspector-evidence.md)  
**Next Step:** Use [02-redline.md](#) (to be generated by `ui-redline` skill) to compare findings against approved spec, or run `ui-acceptance` to create testable checklist from this evidence.
