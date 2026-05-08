---
spec_type: index
spec_id: settings-account
created: 2026-05-06
status: draft
---

# Spec Package Manifest: Prosper Settings Page

This package contains the complete set of specifications for the Settings page feature. It is the canonical worked example referenced by the Interface Skills toolkit.

## Contents and sign-off

| # | File                                                  | Skill                  | Status   | Last updated |
|---|-------------------------------------------------------|------------------------|----------|--------------|
| 1 | [`brief.md`](brief.md)                                | `ui-brief`             | approved | 2026-05-06   |
| 2 | [`visual-calibration.md`](visual-calibration.md)      | `ui-visual-calibration`| approved | 2026-05-06   |
| 3 | [`flow.md`](flow.md)                                  | `ui-flow`              | approved | 2026-05-06   |
| 4 | [`blueprint.md`](blueprint.md)                        | `ui-blueprint`         | approved | 2026-05-06   |
| 5 | [`system.md`](system.md)                              | `ui-system`            | approved | 2026-05-06   |
| 6 | [`screen-spec.md`](screen-spec.md)                    | `ui-screen-spec`       | approved | 2026-05-06   |
| 7 | [`component-specs/profile-form.md`](component-specs/profile-form.md) | `ui-component-spec` | approved | 2026-05-06   |
| 8 | [`microcopy.md`](microcopy.md)                        | `ui-microcopy`         | approved | 2026-05-06   |
| 9 | [`acceptance.md`](acceptance.md)                      | `ui-acceptance`        | approved | 2026-05-06   |

## Open questions still unresolved

Tracked here so they remain visible after the brief itself is closed. See `brief.md §9`:

1. Maximum avatar file size — currently assumed 2 MB in `microcopy.md` and `component-specs/profile-form.md`. Engineering must confirm before code generation.
2. Notifications autosave vs. explicit save — resolved in this package as **autosave with debounced PATCH** (see `flow.md §3`).
3. Display name length cap — resolved as **60 characters max** with inline error (see `microcopy.md §3`).
4. Billing CTAs — resolved as **single external "Manage subscription" link**, no in-app upgrade CTA (see `flow.md §3`).
5. Mobile sidebar reflow — resolved as **collapse to hamburger sheet** at `< md` (see `blueprint.md §4`).

## Change log for this package

| Date       | Change                                                                              |
|------------|-------------------------------------------------------------------------------------|
| 2026-05-06 | Initial draft of all artifacts.                                                     |
