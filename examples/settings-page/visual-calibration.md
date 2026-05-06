---
spec_type: visual-calibration
spec_id: settings-account
created: 2026-05-06
status: draft
---

# Visual Calibration: Prosper Settings Page

## 1. Source vocabulary

The original request used the following vague terms. Each is translated below into a concrete, testable decision before any layout work begins.

| Vague term used         | Translation question asked                                          | Decision                                                                                  |
|-------------------------|---------------------------------------------------------------------|-------------------------------------------------------------------------------------------|
| "clean"                 | Empty, sparse, or low-noise?                                        | **Low-noise** — every element earns its place; remove decorative borders and shadows.      |
| "modern"                | What reference product looks "modern" to the user?                  | Linear and Vercel dashboard — flat surfaces, restrained color, generous spacing.           |
| "professional"          | Restrained or formal?                                               | **Restrained** — neutral palette, no marketing-style illustrations or gradients.           |
| "easy to use"           | Few decisions per screen, or familiar patterns?                     | **Familiar patterns** — left sidebar nav, form-on-right is the SaaS settings convention.   |

## 2. Concrete visual decisions

### Layout archetype
**Split panel** — fixed-width left sidebar for navigation, fluid main panel for the active section's form. This is the conventional pattern for SaaS settings (Notion, Linear, Stripe, GitHub) and matches the user's "easy to use" mental model.

### Density
**Medium** — vertical rhythm is `space.4` (16px) between form rows, `space.6` (24px) between form sections, `space.8` (32px) between page sections. Form inputs are 40px tall (default web SaaS sizing). This is denser than a marketing site, sparser than a data table.

### Shape language
**Mildly rounded** — `radius.md` (6px) for inputs and buttons, `radius.lg` (8px) for cards and modals. No fully rounded pills. No square corners.

### Surface style
**Flat with hairline borders** — main content area has a single 1px border at `color.border.default` and no shadow. Cards inside the main area use the same hairline border, no elevation. Modals and toasts get a single subtle drop shadow to indicate elevation; nothing else does.

### Palette guidance
**Monochrome with one accent.** Greys for everything: text, surfaces, borders, navigation. The accent `color.action.primary` (`#2563EB`) is used only for the primary action of the page (Save button) and the active sidebar item. Status colors (`color.status.success`, `color.status.error`) appear only in toasts and inline validation, not in the static UI.

### Typography rhythm
- Page heading: `type.heading.lg` (24px, weight 600, line-height 1.3)
- Section heading: `type.heading.md` (18px, weight 600, line-height 1.4)
- Body: `type.body.md` (14px, weight 400, line-height 1.5)
- Helper / meta: `type.body.sm` (13px, weight 400, line-height 1.5, color `text.secondary`)

## 3. What this calibration rules out

- No coloured section headers, no avatar gradient, no marketing-style imagery.
- No accordion-collapsed sections — the user sees the full active section at all times.
- No icon-only navigation in the sidebar — every nav item has a visible label at all viewports above `< sm`.
- No multi-column form layouts inside a section — every field is full-width within the main panel.

## 4. Reference products

The user did not name a reference. Based on the calibration above, the closest visual reference is the **Linear settings page** and **Vercel project settings**. When in doubt about a styling decision, look there first.
