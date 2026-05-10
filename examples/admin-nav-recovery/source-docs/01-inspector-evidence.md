---
spec_type: inspector-evidence
spec_id: admin-sidebar-nav
based_on: none — no linked spec
created: 2025-05-22
inspection_method: static source-code
status: draft
---

# Inspector Evidence Report: Admin Sidebar Navigation

**URL / file inspected:** `metamorfose-platform/components/shell/portal-shell.tsx`, `metamorfose-platform/lib/shell-navigation.ts`, `metamorfose-platform/lib/admin-product-surface.ts`
**Inspection date:** 2025-05-22
**Spec package linked:** none
**Inspection method:** static source-code
**Primary breakpoint tested:** Desktop (implied by `lg:block w-[420px]` in `PortalShell`)

---

## 1. DOM Inventory (AdminSidebar)

| Element type | Selector | Semantic role | Semantic markup present? | Notes |
|---|---|---|---|---|
| div | (container) | none | No | Main sidebar wrapper |
| a | `Link[href="/admin"]` (Brand) | link | Yes | Top branding section |
| nav | `nav` | navigation | Yes | Navigation container |
| a | `Link[href="/"]` | link | Yes | "Voltar aos Portais" |
| a | `Link[href="/admin"]` | link | Yes | "Painel de Gestão" |
| section | `section` | none | No | Section group wrapper (one per navigation section) |
| button | `button` | button | Yes | Section toggle (accordion header); has `aria-expanded` |
| div | `div` (Items wrapper) | none | No | Appears when section is expanded |
| a | `Link[href={item.href}]` | link | Yes | Individual module tab |
| span | `span` (Badge) | none | No | "Demo" or "Em breve" badge inside tab |

**Total interactive elements found:** Variable (based on registry) + 4 fixed links/buttons.
**Elements missing semantic markup:**
- Section wrappers (`section` tag used but no ARIA landmark or heading association).
- Active state indicators (currently only visual/text color change, no `aria-current="page"`).

---

## 2. Computed Styles Sample (Inferred)

| Element | Selector | Text color | Bg color | Font size | Font weight | Border radius | Padding (T R B L) | Confidence |
|---|---|---|---|---|---|---|---|---|
| Sidebar Container | `div.flex.h-full` | `#edf3ff` | `#111944` | — | — | 0px | 0px | exact — source |
| Brand Link | `Link[href="/admin"]` | `#ffffff` | transparent (hover: `white/5`) | — | — | 0px | 28px 28px 28px 28px (px-7 py-7) | inferred — source |
| Nav Item (Inactive) | `Link.rounded-full` | `#edf3ff/95` | transparent (hover: `white/8`) | 24px (text-2xl) | 500 (medium) | 9999px (full) | — | inferred — source |
| Nav Item (Active - Panel) | `Link[href="/admin"]` | `#ffffff` | `#28346c` | 24px (text-2xl) | 600 (semibold) | 9999px (full) | — | inferred — source |
| Section Toggle | `button` | `#edf3ff` | transparent | 20px (text-xl) | 700 (bold) | 0px | 4px 20px 4px 20px (px-5 py-1) | inferred — source |
| Badge (Demo/Soon) | `span.rounded-full` | `#16223f` | `#dffbf2` | 18px (text-lg) | 700 (bold) | 9999px (full) | 4px 20px 4px 20px (px-5 py-1) | inferred — source |

---

## 3. Token Usage

**CSS custom properties (`var(--)`) detected:** 0 references in `AdminSidebar` (uses hardcoded hex and Tailwind opacity).
**Literal color values found:**
- `#111944` (Deep Blue) — Sidebar Background
- `#edf3ff` (Off-white) — Default Text
- `#bdeff1` (Light Cyan) — Border
- `#28346c` (Active Blue) — Active Background (Panel only)
- `#dffbf2` (Mint) — Badge Background
- `#16223f` (Dark Blue) — Badge Text
- `white/10`, `white/8`, `white/5` — Various opacities for borders and hovers.

**Literal spacing values found:**
- `h-16 w-16` (64px) — Brand Icon
- `px-7 py-7` (28px) — Brand Padding
- `mt-10` (40px) — Navigation top margin
- `space-y-9` (36px) — Section spacing
- `min-h-[58px]` — Nav Item minimum height

---

## 4. Accessibility Findings (Static)

**Inspection method:** Manual source-code audit.

| Severity | Element | Selector | Issue | WCAG criterion |
|---|---|---|---|---|
| serious | Tab Link | `AdminSidebar a` | No `aria-current="page"` used for active links. | 4.1.2 |
| moderate | Brand Link | `AdminSidebar a[href="/admin"]` | Redundant links: Brand and "Painel de Gestão" both point to `/admin`. | 2.4.4 |
| moderate | Icon | `LucideIcon` | Icons inside tabs (Home, LayoutGrid, etc.) are not marked `aria-hidden="true"`. | 1.1.1 |
| minor | Section Toggle | `button` | Text is uppercase via `uppercase` class; may affect screen reader prosody. | 1.3.1 |

---

## 5. Responsiveness

| Breakpoint | Viewport width | Horizontal scroll? | Primary action in top half? | Text clipped? | Blueprint reflow match? |
|---|---|---|---|---|---|
| Desktop | `lg:block` (>1024px) | No | Yes | No | matches (persistent sidebar) |
| Mobile/Tablet | `<1024px` | No | Yes (via burger) | No | matches (drawer pattern) |

---

## 6. Inspector notes

- **CRITICAL FINDING**: Individual module tabs (e.g., "Atendimento", "Inbox") currently **lack active state logic** in `AdminSidebar`. Only the "Painel de Gestão" top-level link has a conditional class for `props.currentPath === "/admin"`.
- **Finance Path Inconsistency**: The sidebar uses `item.href` from the registry. In `admin-product-surface.ts`, the "final" href for Finance is `/admin/financeiro`. The target canonical path `/admin/finance` is currently listed as `legacyHref`.
- **Icon Set**: The sidebar uses `lucide-react`. Icons are mapped via `iconForKey` helper.
- **Section Expansion**: Managed by `expandedSectionIds` state, initialized by `getInitialAdminExpandedSections`. It expands all sections if on the dashboard (`/admin`) or the specific section containing the current path.
- **Deep-linking Expansion**: `sectionContainsPath` uses `.startsWith(item.href + "/")`, which is correct for module sub-pages.

**This report contains evidence only. No judgments about correctness or severity are made here. Pass this report to `ui-redline` for evaluation against the spec.**
