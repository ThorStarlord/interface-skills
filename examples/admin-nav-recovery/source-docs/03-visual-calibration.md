---
spec_type: visual-calibration
spec_id: admin-sidebar-nav
created: 2025-05-22
based_on: brief-admin-sidebar-nav
status: draft
---

# Visual Calibration Sheet: Admin Sidebar Navigation

## Translation Log

| User's word / phrase | Translator match | Concrete properties used | Confirmed or assumed |
|---|---|---|---|
| "Calm Mission Control" | Not in translator — interpreted as focused, low-noise, high-precision. | Medium density; High contrast labeling; Minimal decorative elements. | ✅ Confirmed (per CONTEXT.md) |
| "Warm Concierge" | Not in translator — interpreted as welcoming, rounded, professional. | Large corner radius (`rounded-[28px]`); Muted background with soft shadows. | ✅ Confirmed (per CONTEXT.md) |
| "Surgical instrument" | Not in translator — interpreted as precise, action-oriented, zero-clutter. | Actionable items prioritized; clear "you are here" indicators. | ✅ Confirmed (per CONTEXT.md) |
| "Like Linear" | Not in translator — assumed density and grouping logic. | Sidebar App archetype; Grouped sections; subtle active indicators. | ⚠️ Assumed (from blueprint goal) |

## Concrete Visual Decisions

- **Layout Archetype:** Sidebar App
- **Density:** Medium
  - Tailwind tokens: `px-7`, `py-7`, `space-y-9` (sections), `space-y-2` (tabs).
- **Shape Language:** Rounded
  - Tailwind tokens: `rounded-[28px]` for container; `rounded-full` for interactive tabs.
- **Surface Style:** Card-heavy / Elevated
  - Tailwind tokens: `shadow-[0_24px_80px_rgba(15,23,42,0.28)]`, `border-white/10`.
- **Palette Guidance:** Deep Blue institutional base (`#111944`). High-contrast Off-white text (`#edf3ff`). Active accent in Medium Blue (`#28346c`). Utility badges in Mint (`#dffbf2`).

## Reference Products

| Product | What the user wants to borrow | What to avoid from it |
|---|---|---|
| Linear | Grouping logic, density, and professional "work tool" feel. | Avoid complex sub-menu nesting if it adds clutter. |
| Stripe | Typography clarity and "surgical" precision of dashboard elements. | Avoid the overly "white" marketing feel; stick to the deep-blue institutional tone. |

## Open Questions

1. Should the active state for module-level tabs use the same "Elevated" pill style as the top-level "Painel de Gestão"?

## Assumptions

- ⚠️ ASSUMED: The "Linear-like" grouping is preferred over the current slightly flatter structure to handle future module growth.
- ⚠️ ASSUMED: The institutional Deep Blue is non-negotiable as it defines the "Admin" portal identity vs other portals.
