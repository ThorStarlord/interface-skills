---
spec_type: blueprint
spec_id: settings-account
created: 2026-05-06
status: draft
---

# Blueprint: Prosper Settings Page

## 1. Information hierarchy (priority order)

1. **Active section heading** — the user must immediately know which section they are on.
2. **The form fields** for the active section — that is what they came here to change.
3. **Save / Cancel actions** — the primary outcome.
4. **Section navigation (sidebar)** — secondary; only used when switching sections.
5. **User profile badge in sidebar** — reference, not action; lowest visual weight.

## 2. Text wireframe (desktop, `lg+`)

```text
┌─────────────────────────────────────────────────────────────────────┐
│ Prosper · App Header (existing global chrome)                       │
├──────────────────────┬──────────────────────────────────────────────┤
│ [Avatar] Jane Doe    │  Profile                                      │  ← <h1>
│ jane@acme.com        │  ──────────────────────────────────           │
│                      │                                                │
│ ▸ Profile  ●         │  Display name                                  │
│   Notifications      │  ┌──────────────────────────────────────┐    │
│   Billing            │  │ Jane Doe                              │    │
│                      │  └──────────────────────────────────────┘    │
│                      │  Helper text                                   │
│                      │                                                │
│                      │  Profile picture                               │
│                      │  ┌──────┐  Recommended 256×256, max 2 MB.     │
│                      │  │ IMG  │  [ Replace ]  [ Remove ]            │
│                      │  └──────┘                                      │
│                      │                                                │
│                      │  ┌──────────────────────────────────────┐    │
│                      │  │  [ Cancel ]      [ Save changes ]    │    │ ← sticky
│                      │  └──────────────────────────────────────┘    │
└──────────────────────┴──────────────────────────────────────────────┘
   240px fixed sidebar   max-width 720px main panel, centred in viewport
```

## 3. Region anatomy

| Region        | Element              | Width                          | Behavior                                                                 |
|---------------|----------------------|--------------------------------|--------------------------------------------------------------------------|
| Sidebar       | `<aside>`            | 240px fixed                    | Sticky to viewport top below app header.                                  |
| Profile badge | top of sidebar       | full sidebar width             | Avatar + name + email; non-interactive; updates live when Profile saves.  |
| Nav list      | below profile badge  | full sidebar width             | Vertical list; active item shows accent-colored left border + bold label. |
| Main panel    | `<main>`             | fluid, max 720px, centered     | Single-column form; vertically scrollable below sticky action footer.     |
| Section heading | top of main panel  | full main width                | `<h1>` with the section name.                                             |
| Form area     | below heading        | full main width                | Form fields stacked vertically with `space.6` between sections of fields. |
| Action footer | bottom of main panel | full main width                | Sticky at viewport bottom; right-aligned Cancel + Save.                   |

## 4. Responsive behavior

Per [`shared/references/responsive-patterns.md`](../../shared/references/responsive-patterns.md):

| Breakpoint  | Sidebar          | Main panel        | Action footer     |
|-------------|------------------|-------------------|-------------------|
| `< sm`      | **collapse** behind hamburger button in app header; opens as full-screen sheet | full-screen, no max-width | sticky at viewport bottom |
| `sm` – `< md`| same as above   | full-screen, padding `space.4` | sticky bottom |
| `md` – `< lg`| **swap** to top horizontal scrollable tab strip above main panel | full-width, padding `space.6` | sticky bottom |
| `lg+`       | fixed left rail (240px) | max-width 720px, centered | sticky bottom of main panel |

## 5. What is *not* in this blueprint

- The visual styling of buttons, inputs, and toggles — those live in `system.md` and the per-component specs.
- Microcopy — see `microcopy.md`.
- The Notifications and Billing section bodies — for brevity, this blueprint only diagrams the Profile section. Notifications uses the same chrome with a vertical list of labelled toggles; Billing uses the same chrome with a read-only summary card and one external-link button.

## 6. Open layout questions resolved

- The action footer is **sticky to the bottom of the main panel**, not to the bottom of the viewport. This keeps Save/Cancel discoverable on long forms but does not occlude footer content on short ones.
- The sidebar profile badge is **non-interactive**. Clicking it does not navigate anywhere (no profile detail page in scope per brief §8).
