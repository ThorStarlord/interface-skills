---
spec_type: visual-calibration
spec_id: pulse-create
created: 2026-05-08
status: approved
recovery: true
---

# Visual Calibration: Pulse /create Route (Spec Recovery)

> **Recovery note:** This calibration documents the visual language currently in use (*Observed*) and the agreed visual direction going forward (*Target*). The observed language is inferred from the static source inspection. Approving this document means approving the Target.

---

## Layout Archetype

**Observed:** Two-column split — left column contains the form (caption, channel selector, media upload); right column contains the post preview. Columns are equal-width at 1280px.

**Target:** Two-column split, 60/40 ratio (form / preview). At `< 768px`, the preview collapses below the form (stack reflow). This is the single responsive layout replacing the mobile redirect.

---

## Density

**Observed:** Medium-compact. Form fields are `py-2.5 px-4` (10px/16px). Spacing between sections is inconsistent (24px between some groups, 16px between others, 32px in one place).

**Target:** **Medium**. Standardise all intra-section spacing to `space.4` (16px) and inter-section spacing to `space.6` (24px). Form fields remain compact — this is a high-frequency productivity tool, not a marketing landing page.

---

## Shape Language

**Observed:** Mixed. Primary buttons use `rounded-md` (6px), channel badges use `rounded-full`, the schedule modal backdrop uses `rounded-none` (square). Inconsistent.

**Target:** **Soft-geometric**. All interactive surfaces: `rounded-md` (6px). Badges and tags (non-interactive): `rounded-full`. Modals and panels: `rounded-lg` (8px). No square corners except dividers.

---

## Surface Style

**Observed:** Flat white. One surface level. No elevation or card-based grouping — the form and preview are visually undifferentiated from the page background.

**Target:** **Two-surface**. Page background: `color.surface.base` (`#f9fafb`). Form panel and preview panel: `color.surface.elevated` (`#ffffff`) with `shadow.sm` (`0 1px 3px rgba(0,0,0,0.08)`). This creates clear visual grouping without heavy chrome.

---

## Palette Guidance

**Observed:** `#7c3aed` (Tailwind `violet-600`) used as primary action colour. `#111827` for body text. `#ffffff` for surfaces. No system; values are repeated as literals.

**Target:**

| Role | Token | Value |
|---|---|---|
| Primary action | `color.action.primary` | `#7c3aed` |
| Primary action hover | `color.action.primary.hover` | `#6d28d9` |
| Primary action text | `color.action.primary.text` | `#ffffff` |
| Body text | `color.text.primary` | `#111827` |
| Secondary text | `color.text.secondary` | `#6b7280` |
| Surface base | `color.surface.base` | `#f9fafb` |
| Surface elevated | `color.surface.elevated` | `#ffffff` |
| Border | `color.border.default` | `#e5e7eb` |
| Error | `color.status.error` | `#ef4444` |
| Success | `color.status.success` | `#22c55e` |

---

## Typography

**Observed:** Inter is in use. `font-semibold text-2xl` for the page heading; `text-sm` for labels; `text-base` for body/textarea. Consistent enough to retain.

**Target:** Codify the observed scale as named tokens:

| Role | Token | Value |
|---|---|---|
| Page heading | `type.heading.xl` | Inter 24px / 700 / 32px line height |
| Section label | `type.label.sm` | Inter 12px / 600 / 16px line height |
| Body / input | `type.body.md` | Inter 16px / 400 / 24px line height |
| Button label | `type.label.md` | Inter 14px / 600 / 20px line height |

---

## Visual tone reference

Pulse's observed UI sits between Notion (clean, content-first) and Linear (compact, keyboard-driven). The target should lean toward **Linear's density** (high information per square inch) with **Notion's surface simplicity** (no heavy gradients, shadows, or decorative chrome). The violet accent is distinctive and should remain — it does not need to become more muted.
