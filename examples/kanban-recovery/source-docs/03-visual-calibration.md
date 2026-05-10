---
spec_type: visual-calibration
spec_id: kanban-visual-language
created: 2026-05-10
status: current
source_evidence:
  - 01-inspector-evidence.md (DOM inventory, computed styles, Tailwind tokens)
  - 02-brief.md (warm concierge, low-tech friendly, celebratory UX)
  - saas_frontend/src/pages/KanbanPage.tsx (Framer Motion, semantic tokens, layout)
  - saas_frontend/src/components/kanban/KanbanCard.tsx (card variants, status config)
  - docs/DESIGN_SYSTEM.md (warm concierge philosophy, premium aesthetics)
  - saas_frontend/src/index.css (semantic color tokens, CSS custom properties)
---

# Visual Calibration: Kanban Approval Queue

## 1. Layout Archetype

**Kanban Column Grid with Responsive Deck Overlay**

### Desktop (≥1024px)
- **Primary:** 4-column kanban board, horizontally scrollable
- **Column width:** 18rem (288px) per column, or `flex-1` on larger screens
- **Column stacking:** Side-by-side, no wrapping
- **Safe flow:** All 4 columns visible at once on 1440px+ screens; 2–3 visible on 1024px; horizontal scroll available

### Mobile (<1024px)
- **Primary:** Single-column tab view (4 tabs, one active)
- **Tab layout:** Flex bar with emoji + label + count badge, `lg:hidden`
- **Card view:** One column's cards stack vertically in a scrolling container
- **Alternative (Secondary):** Card deck / "Review Mode" — swipeable single-card view (ProactiveCardStack component)
- **Responsive breakpoint:** `lg:` at 1024px

### Review Mode (Deck View)
- **Container:** `max-w-sm`, centered on screen
- **Card presentation:** One card visible at full viewport height, pinned-center layout
- **Swipe interaction:** Drag left/right to reject/approve (exit animation on swipe)
- **Accessibility:** Touch-friendly, visual feedback on swipe intention

---

## 2. Density

**Medium Density — Spacious Cards with Breathing Room**

### Spacing Principles
- **Card gap:** 1.5rem (24px) between cards in column, maintained via Framer Motion stagger and Tailwind gap utilities
- **Padding inside card:** 0.75rem (12px) horizontal, 0.75rem (12px) vertical on media; p-3 (12px) on card body
- **Column header padding:** px-4 pt-3 pb-0 (16px horizontal, 12px top)
- **Column gutter:** 1rem (16px) between column edges on desktop
- **Card aspect ratio:** Maintained at 4:3 or 1:1 depending on format (carousel/story/reel)

### Visual Breathing
- Not a list of dense items; each card gets spatial prominence
- Media preview is large (aspect-maintained, ~200px height at mobile width)
- Hover states expand shadow radius, not compress space
- Empty states have ≥180px min-height with centered emoji, headline, and hint

### Touch Targets
- Approval buttons ("Aprovar", "Não quero este"): ≥44px height minimum (Tailwind `h-10` or larger)
- Status badge buttons: h-7 w-7 minimum on icon buttons (MoreHorizontal, retry)
- Tab buttons on mobile: Full width of tab container, ≥48px tall

---

## 3. Shape Language

**Rounded, Warm, Non-Sharp Aesthetic**

### Corner Radius Hierarchy

| Element | Radius Class | Pixels | Use |
|---------|---|---|---|
| Card root (media + body) | `rounded-2xl` | 1rem (16px) | Primary kanban cards |
| Column header | `rounded-t-2xl` | 1rem (16px) on top | Above column container |
| Button (primary/secondary) | `rounded-md` | 0.375rem (6px) | Action buttons (Aprovar, etc.) |
| Button (full pill style) | `rounded-full` | 50% | "Criar meu primeiro post" CTA, optional pill variants |
| Input fields / modals | `rounded-lg` | 0.5rem (8px) | Form inputs, dropdown menus (via Radix) |
| Empty state container | `rounded-2xl` | 1rem (16px) | Dashed border empty state |
| Dropdown menu | `rounded-xl` | 0.75rem (12px) | DropdownMenuContent via Radix |
| Icon boxes (column header) | `rounded-lg` | 0.5rem (8px) | Small icon backgrounds |

### Principle
- **No sharp edges.** All visible elements have some rounding to convey friendliness and care.
- **Consistent hierarchy:** Larger elements (cards) have bolder rounding; smaller elements (icons, buttons) have finer rounding.
- **Pill buttons for CTAs:** Full-bleed CTAs in empty states use rounded-full to signal "take this action" with premium feel.

---

## 4. Surface Style

**Layered Elevation with Semantic Depth Tokens**

### Shadow / Elevation Scale (from computed styles)

| Elevation | Usage | CSS Value | Tokens |
|---|---|---|---|
| Level 0 (Base) | Card at rest | `0 0 0 1px border-border` | border-border/60 |
| Level 1 (Hover) | Card hover, subtle lift | `0 10px 30px -8px hsl(var(--primary)/0.2), 0 4px 8px -4px hsl(var(--foreground)/0.08)` | Primary shadow + foreground shadow |
| Level 2 (Active/Dragging) | Card being dragged | `0 20px 40px -10px hsl(var(--primary)/0.3), 0 8px 16px -6px hsl(var(--foreground)/0.12)` | Intensified primary + foreground |
| Level 3 (Modal/Overlay) | Post detail modal, dropdown | `0 25px 50px -12px hsl(var(--foreground)/0.15)` | Deep foreground shadow |

### Background Surfaces

| Surface | Background | Tokens | Use |
|---|---|---|---|
| Card (white) | `hsl(0 0% 100%)` | `--card` | Primary kanban cards |
| Card with status accent | `hsl(var(--warning)/10)` etc | `--warning/10`, `--info/10`, `--success/10` | Column headers (status-dependent) |
| Empty state container | `hsl(var(--muted)/20)` | `--muted/20` | Dashed border empty state background |
| Format badge | `hsl(0 0% 60%)` | `black/60` | Opaque dark badge on media overlay |
| Hero surface (page header) | Radial gradient + card background | Layered: `radial-gradient(...primary), radial-gradient(...accent), --card` | Page hero with premium depth |
| Hover overlay (card media) | Glass background | Glass-morphism effect (inferred from inspector) | Fade-in overlay on media hover |

### Principle
- **Semantic depth:** Status (warning/info/success) backgrounds signal importance and guide attention.
- **Micro-interactions:** Shadows intensify on hover/drag to provide tactile feedback without moving the element (Y-axis lift at `-4px` to `-8px`).
- **No flat design:** Every surface has subtle depth via border, shadow, or status color to reinforce hierarchy.

---

## 5. Palette Guidance

**Bold, Warm, High-Contrast Aesthetic (Warm Concierge)**

### Semantic Color Tokens (from index.css)

| Token | HSL Value | Hex Approx | Purpose | Use Cases |
|---|---|---|---|---|
| `--primary` | 12 76% 61% | #F97316 (orange) | Primary action, CTA, approval | Buttons, highlights, primary brand |
| `--warning` | 38 92% 50% (amber) | #FBBF24 | Attention, pending review | "Para decidir" status, review badges |
| `--info` | 172 66% 50% (cyan) | #06B6D4 | Scheduled, planning | "Agendados" status, approved cards |
| `--success` | 142 76% 36% (green) | #22C55E | Published, completed | "Publicados" status, success feedback |
| `--destructive` | 0 84% 60% (red) | #EF4444 | Error, deletion, warning | Error badges, delete action |
| `--accent` | 172 66% 50% | #06B6D4 | Secondary brand accent | Supporting elements, secondary UI |
| `--muted` | 220 14% 96% | #F1F5F9 | Subtle backgrounds, disabled | Inactive states, secondary fills |
| `--foreground` | 220 20% 20% | #1E293B | Text, primary ink | All text content, foreground elements |

### Palette Principles

1. **Bold primary (orange):** High saturation, warm feeling. Signals action and energy. Used on approval buttons ("Aprovar") to draw attention.
2. **Semantic statuses:** Color + icon + text reinforces meaning without color-only signaling (WCAG AA compliance).
   - `warning/10` background for "Para decidir" — amber border and icon signal "waiting on user"
   - `info/10` for "Agendados" — cyan signals "planned, scheduled"
   - `success/10` for "Publicados" — green signals "complete"
3. **High contrast:** Text on backgrounds always meets WCAG AA (4.5:1) minimum. Check via HSL difference (lightness gap ≥50% typical).
4. **Supportive neutrals:** Muted backgrounds (96% lightness) create spacious, breathing room. No harsh blacks.
5. **Error visibility:** Red destructive state is high-saturation, never buried in muted backgrounds.

### Color Application Rules

| Element | Color | Notes |
|---|---|---|
| Card body (at rest) | `--card` (white) | Neutral, clean |
| Column header (backlog) | `--muted/50` background | Neutral, inactive channel |
| Column header (review) | `--warning/10` background | Amber signals "needs attention" |
| Column header (approved) | `--info/10` background | Cyan signals "planned" |
| Column header (published) | `--success/10` background | Green signals "done" |
| Approval button (Aprovar) | `--success` text on success/10 background | Green primary action |
| Rejection button (Não quero) | `--muted-foreground` on muted background | Neutral, secondary action |
| Delete / Error button | `--destructive` text on destructive/10 | Red danger signal |
| Empty state border | `--border/40` (dashed) | Subtle, not intrusive |
| AI-generated badge | `--primary/5` background | Subtle orange hint, not bold |
| Age badge (backlog) | `--warning/10` background | Amber signals "needs refresh" |
| Error badge (publishing) | `--destructive/10` background + animate-pulse | Red + pulse draws attention |

---

## 6. Typography

**Modern, Friendly, Hierarchical (from index.css + DESIGN_SYSTEM.md)**

### Font Stack
- **Primary:** `Inter` (sans-serif, 300 / 400 / 500 / 600 / 700 weights)
- **Accent (optional):** `Fraunces` (serif, 600 / 700 / 800 weights) — reserved for hero headlines, not kanban cards

### Typographic Hierarchy (Kanban Context)

| Element | Size | Weight | Line Height | Use |
|---|---|---|---|---|
| Page title (h2) | `text-2xl` (1.5rem) | `font-black` (900) | tight | "Decida o que vai para a agenda" |
| Column title (h3) | `text-sm` (0.875rem) | `font-bold` (700) | tight | Column names (Ideias salvas, etc.) |
| Column subtitle | `text-[10px]` | regular (400) | relaxed | Descriptive text under title, opacity-70 |
| Card title (h4) | `text-sm` (0.875rem) | `font-bold` (700) | tight | Post title/caption preview |
| Card description | `text-xs` (0.75rem) | regular (400) | relaxed | Post content preview, text-muted-foreground |
| Badge text (AI, age, error) | `text-[9px]` | `font-semibold` (600) | tight | Compact status labels |
| Button text | `text-sm` (0.875rem) | `font-medium` (500) | normal | "Aprovar", "Não quero este", etc. |
| Empty state headline | `text-sm` (0.875rem) | `font-semibold` (600) | normal | "Sua fábrica está aquecida" |
| Empty state hint | `text-xs` (0.75rem) | regular (400) | relaxed | Supportive context, max-w-[220px] |
| Time/date display | `text-[10px]` | regular (400) | normal | "Publicado em X de maio" |

### Typographic Principles

1. **Bold titles:** Column titles and card titles use `font-bold` to create visual hierarchy and scannability.
2. **Text clamp:** Body text in cards uses `line-clamp-1` (titles) or `line-clamp-2` (descriptions) to prevent overflow.
3. **Muted secondary text:** Subtitles and hints use `text-muted-foreground` (50% opacity on 220 10% 50%) for visual subordination.
4. **Tiny badges:** Status labels use `text-[9px]` to stay compact while remaining readable at 16px base font size.
5. **Warm language:** All copy is human-first, not utilitarian. Example: "Aprovar" (approve) not "Accept"; "Para decidir" not "Pending".

---

## 7. Animation Direction

**Purposeful Motion — Framer Motion Staggered Entry & Drag Feedback**

### Entry Animation (Staggered)

**Column cards enter sequentially on page load/mount:**

```
columnVariants = {
  hidden: {},
  show: {
    transition: { staggerChildren: 0.045 }
  }
}

cardVariants = {
  hidden: { opacity: 0, y: 10, scale: 0.97 },
  show: {
    opacity: 1, y: 0, scale: 1,
    transition: { duration: 0.22, ease: [0.25, 0.46, 0.45, 0.94] }
  },
  exit: {
    opacity: 0, scale: 0.94, y: -8,
    transition: { duration: 0.16, ease: [0.42, 0, 1, 1] }
  }
}
```

**Effect:**
- Cards fade in + slide up 10px + scale from 0.97 → 1.0
- Stagger delay: 45ms between cards (smooth cascade)
- Duration: 220ms per card
- Easing: Custom cubic-bezier `[0.25, 0.46, 0.45, 0.94]` (gentle ease-out)
- **Perception:** Kanban loads with energy, drawing eye left-to-right across columns

### Exit Animation

- Cards fade out + scale to 0.94 + slide up 8px
- Duration: 160ms (faster exit)
- Easing: Sharp ease-out `[0.42, 0, 1, 1]`
- **Perception:** Card removal feels swift, not jarring

### Hover / Interactive Feedback

| State | Animation | Effect |
|---|---|---|
| Card hover (desktop) | Shadow intensity + Y-lift | Box-shadow increase (Level 1 → Level 2), subtle `-4px` to `-8px` Y-axis lift |
| Drag start | Scale + shadow boost | `scale: 1.05` (approx), Level 2 shadow intensifies |
| Drag in progress | Reduced motion respects prefers-reduced-motion | If `useReducedMotion()` → no animation, instant state |
| Drag end | Snap to grid + fade in | Framer Motion drag handlers trigger re-layout |
| Swipe on mobile (Review) | Deck slide + exit animation | Card slides off-screen on swipe; next card fades in |
| Button hover (Approve/Reject) | Color shift + lift | Background color intensifies, `-2px` Y-lift on button |

### Motion Principles

1. **Stagger timing:** 45ms is slow enough to feel intentional, fast enough to not feel sluggish.
2. **Cubic-bezier easing:** Not linear; curves favor smooth, human feel over robotic timing.
3. **Reduced motion respected:** If `prefers-reduced-motion` is set, all animations are disabled (via `useReducedMotion()` hook).
4. **No forced motion:** Interactive elements (buttons, drag) only animate if user initiated; no auto-playing video previews or scrolling.
5. **Drag feedback:** Dragging a card scales it up slightly + increases shadow to show it's "lifted" off the page.
6. **Review deck swipe:** Swiping left/right on card stack is the primary mobile approval gesture — fast, satisfying, low cognitive load.

---

## 8. Reference Implementations

**Products that match or inspired this aesthetic:**

| Product | Aspect Matched | Why |
|---|---|---|
| **Notion** | Kanban view, rounded cards, semantic status colors | Inspiration for column layout, status-based backgrounds |
| **Stripe Dashboard** | Premium gradients, semantic tokens, high contrast | Inspiration for bold primary orange, clean surfaces |
| **Linear** | Card-based workflow, staggered entry animation, drag feedback | Inspiration for motion design, approval queue feel |
| **Figma** | Rounded cards, large touch targets, celebratory empty states | Inspiration for design system tokens, rounded-lg aesthetic |
| **Monday.com** | Column-based project view, swipeable mobile mode | Inspiration for responsive layout (desktop board + mobile deck) |

---

## 9. Accessibility & Inclusive Design

### Color & Contrast
- All status colors meet WCAG AA 4.5:1 contrast on their backgrounds.
- Color is never the only signifier; every status has icon + text + background.
- Error states use red + animation (pulse) + text to signal problems.

### Touch & Motor
- All interactive targets ≥44px height (approval buttons, dropdown triggers).
- No hover-only states; important info is visible on focus/active.
- Swipe gestures have visual feedback before and after.

### Cognitive Load
- Empty states are celebratory ("Missão cumprida 🎉") not utilitarian ("No data").
- Column titles are human-first ("Para decidir" not "Review Queue").
- Each column has a clear emoji + icon + color to aid visual scanning.

### Motion
- `prefers-reduced-motion` is respected; animations are disabled if set.
- No auto-playing content; user controls all motion.
- Drag/drop has visual feedback but is not required; buttons are always available as fallback.

---

## 10. Component Token Mapping

**How to apply this visual calibration to component specs (downstream `06-component-specs.md`):**

### Card Component
- Use `rounded-2xl` + Level 1 shadow at rest, Level 2 on hover
- Apply status-dependent background from palette table (e.g., `--warning/10` for review cards)
- Font: Inter, bold titles + regular descriptions
- Padding: p-3 on body, aspect-maintained media container

### Button Component
- Primary (Approve): Orange (`--primary` / `--success` depending on context), rounded-md, ≥44px height
- Secondary (Reject): Muted (`--muted-foreground`), rounded-md
- Icon buttons: Rounded-lg, h-7 w-7 minimum
- Hover: Color shift + `-2px` Y-lift

### Column Header Component
- Background: Status-dependent (`--warning/10`, `--info/10`, etc.)
- Title: h3, bold, uppercase tracking-tight
- Subtitle: p, small, opacity-70
- Border: Top-left and top-right rounded, full-width colored attention bar if column has urgent items

### Empty State Component
- Dashed border, `rounded-2xl`, `--muted/20` background
- Centered flex layout with emoji, headline, hint, optional CTA
- CTA uses `rounded-full` for premium feel
- Min-height: 180px to ensure visual space

### Modal / Dropdown Component
- Rounded-lg or rounded-xl
- Level 3 shadow (deepest)
- Interior uses semantic tokens for any status indicators

---

## Summary

**ViralFactory Kanban = Warm Concierge + Kanban Workflow + Modern Web Design**

- **Archetype:** 4-column grid (desktop) + single-tab stack (mobile) + swipeable deck (review mode)
- **Density:** Medium — spacious cards with 1.5rem gap, not cramped
- **Shape:** Fully rounded aesthetic (rounded-2xl cards, rounded-md buttons, no sharp edges)
- **Surface:** Layered elevation, semantic status backgrounds, subtle shadows on hover
- **Palette:** Bold warm orange primary, semantic warning/info/success/destructive, high-contrast text
- **Typography:** Inter bold titles + regular body, small badges, human-first copy
- **Motion:** Framer Motion staggered entry (45ms), drag feedback, exit animation, respects prefers-reduced-motion
- **Accessibility:** WCAG AA contrast, ≥44px touch targets, no color-only signifiers, celebratory UX

**Next step:** Load `06-component-specs.md` to detail state machines, props, and acceptance criteria for each kanban component (Card, Column, Button, Modal, etc.).
