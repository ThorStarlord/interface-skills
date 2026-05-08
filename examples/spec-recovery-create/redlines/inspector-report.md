---
spec_type: inspector-evidence
spec_id: pulse-create
based_on: none — no linked spec (recovery run)
created: 2026-05-08
inspection_method: static source-code
status: approved
---

# Inspector Evidence Report: Pulse /create Route

**URL / file inspected:** `src/pages/create/CreatePage.tsx` and related component files  
**Inspection date:** 2026-05-08  
**Spec package linked:** none (pre-spec recovery run)  
**Inspection method:** static source-code (Path C — no live browser available; app requires SSO)  
**Primary breakpoint tested:** 1280px desktop (inferred from responsive class variants)

---

## 1. DOM Inventory

| Element type | Selector / identifier | Semantic role | Semantic markup present? | Confidence | Notes |
|---|---|---|---|---|---|
| textarea | `#caption-input` | `<textarea>` | Yes | exact — source | Has `aria-label="Caption"` |
| button | `[data-testid="ai-draft-btn"]` | `<button>` | Yes | exact — source | Has `aria-busy` set dynamically |
| button | `.channel-badge` | `<div onClick>` | **No** | exact — source | No `role`, no `tabIndex` — div-soup |
| button | `[data-testid="publish-btn"]` | `<button>` | Yes | exact — source | — |
| button | `[data-testid="schedule-btn"]` | `<button>` | Yes | exact — source | — |
| input (file) | `#media-upload` | `<input type="file">` | Yes | exact — source | Has `aria-label="Upload media"` |
| select | `[data-testid="channel-select"]` | `<div role="listbox">` | Partial | exact — source | Has `role="listbox"` but child items lack `role="option"` |
| dialog | `ScheduleModal` | `<div>` | **No** | exact — source | No `role="dialog"`, no `aria-modal`, no focus trap |

**Total interactive elements found:** 8 primary, ~14 including ChannelBadge instances  
**Elements missing semantic markup:** 3 (`.channel-badge` divs, `ScheduleModal`, listbox children)

---

## 2. Computed Styles Sample

_All values inferred from source. Confidence noted per row._

| Element | Selector | Text color | Bg color | Font size | Font weight | Border radius | Padding (T R B L) | Confidence |
|---|---|---|---|---|---|---|---|---|
| Primary CTA (Publish) | `[data-testid="publish-btn"]` | `#ffffff` | `#7c3aed` | `14px` | `600` | `6px` | `10px 20px 10px 20px` | inferred — source (Tailwind `rounded-md`, `px-5 py-2.5`, `text-sm font-semibold`) |
| Caption textarea | `#caption-input` | `#111827` | `#ffffff` | `16px` | `400` | `8px` | `12px 16px 12px 16px` | inferred — source |
| AI Draft button | `[data-testid="ai-draft-btn"]` | `#7c3aed` | `#f3f0ff` | `14px` | `500` | `6px` | `8px 16px 8px 16px` | inferred — source |
| Section heading "Create Post" | `h1.page-title` | `#111827` | transparent | `24px` | `700` | `0px` | `0px` | inferred — source |
| Channel badge (active) | `.channel-badge.active` | `#ffffff` | `#7c3aed` | `12px` | `600` | `9999px` | `4px 12px 4px 12px` | inferred — source (Tailwind `rounded-full`) |

**Breakpoint at time of capture:** 1280px (inferred from `md:` class variants)

---

## 3. Token Usage

**CSS custom properties (`var(--)`) detected:** 0 references — the implementation uses Tailwind utility classes and hard-coded hex values exclusively. No CSS custom properties found in any inspected file.

**Literal color values found:**
- `#7c3aed` — found in `CreatePage.tsx` inline style override (line 47), `AiDraftButton.tsx` (line 23), `ChannelBadge.tsx` (line 18)
- `#111827` — found in `CreatePage.tsx` (line 52), `CaptionInput.tsx` (line 31)
- `#f3f0ff` — found in `AiDraftButton.tsx` (line 24)
- `rgba(0,0,0,0.4)` — found in `ScheduleModal.tsx` backdrop overlay (line 9)

**Literal spacing values found (non-token):**
- `padding: 10px 20px` — found in `CreatePage.tsx` line 47 (inline style override, contradicts Tailwind classes on the same element)
- `margin-top: 24px` — found in `CreatePage.css` line 14

---

## 4. Accessibility Findings

**Inspection method:** manual static source review (no axe-core available)

| Severity | Element | Selector | Issue | WCAG criterion |
|---|---|---|---|---|
| critical | Channel badge | `.channel-badge` | `<div>` with `onClick` has no `role`, no `tabIndex`, no `aria-label` — keyboard users cannot reach or activate channels | 2.1.1, 4.1.2 |
| serious | Schedule modal | `ScheduleModal` | No `role="dialog"`, no `aria-modal="true"`, no focus trap implementation — screen readers do not know a dialog has opened | 4.1.2 |
| serious | Listbox children | `[data-testid="channel-select"] > *` | Parent has `role="listbox"` but children have no `role="option"` — listbox relationship is broken | 4.1.2 |
| moderate | AI Draft button | `[data-testid="ai-draft-btn"]` | `aria-busy` is set but no `aria-label` change occurs during loading — users may not know generation is in progress | 4.1.2 |
| moderate | Media upload | `#media-upload` | `<input type="file">` is visually hidden and triggered by a styled `<div>` — the visual trigger has no accessible name | 1.3.1, 4.1.2 |

_Note: hover/focus visual states, screen reader live announcements, and keyboard navigation order cannot be verified in static inspection and are marked `deferred — needs live DOM`._

---

## 5. Responsiveness

| Breakpoint | Viewport | Horizontal scroll? | Primary action in top half? | Text clipped? | Notes |
|---|---|---|---|---|---|
| Desktop | 1280px | No (inferred) | Yes — Publish button in top-right of form area | No | inferred — source |
| Tablet | 768px | Unknown — deferred | Unknown — deferred | Unknown | The `md:` class variant collapses the channel selector panel but behaviour is deferred; no explicit tablet layout found |
| Mobile | 375px | deferred | deferred | deferred | `CreatePage.tsx` checks `isMobile` flag and renders `<MobileCreateRedirect />` instead of the full form — mobile path is a separate component |

**Critical observation:** On mobile, the app renders a completely different component (`MobileCreateRedirect`) that redirects to a simplified form at `/create/mobile`. This is a separate implementation, not a responsive layout. Both paths need separate spec packages or a unified responsive target must be decided.

---

## 6. Inspector Notes

- **AI draft timeout:** `AiDraftButton.tsx` line 67 contains `setTimeout(() => setError('timeout'), 3000)`. The 3-second threshold is hard-coded with no named constant. Cannot confirm whether this was a deliberate product decision or a placeholder.
- **Duplicate caption implementations:** Three files contain caption-related input logic: `CaptionInput.tsx` (used in main form), `MobileCreateRedirect.tsx` (inline textarea), and `PostPreviewCard.tsx` (read-only display). These are not shared — each manages its own character count and validation independently.
- **Color `#7c3aed`:** This value (Tailwind `violet-600`) appears in 6 places without a central token. If the brand colour changes, 6 sites need updating.

**This report contains evidence only. No judgments about correctness or severity are made here. Pass this report to `ui-redline` for evaluation against the spec.**
