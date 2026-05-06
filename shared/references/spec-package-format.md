# Spec Package Format

A spec package represents the single source of truth for a feature. It groups all specification artifacts created by the UI skills together so that any AI session can reconstruct the full decision history by reading the directory.

## Directory Structure

```text
feature-name/
  manifest.md                # Index and sign-off sheet (required)
  brief.md                   # Product/design brief (ui-brief)
  visual-calibration.md      # Visual taste → concrete decisions (ui-visual-calibration)
  flow.md                    # User journey graph (ui-flow, multi-screen features only)
  blueprint.md               # Layout/wireframe spec (ui-blueprint)
  system.md                  # Tokens and design rules (ui-system)
  screen-spec.md             # Screen contract (ui-screen-spec)
  microcopy.md               # Approved copy (ui-microcopy)
  acceptance.md              # Testable checklist (ui-acceptance)
  component-specs/           # One file per non-trivial interactive component (ui-component-spec)
    <ComponentName>.md
  redlines/                  # Optional: redline audit reports (ui-redline)
    redline-001.md
```

## File-naming rules

- Use the canonical file names above. Downstream skills look for these exact names — renaming `blueprint.md` to `layout.md` will cause the next skill in the pipeline to fail to find it.
- Component specs live in `component-specs/` (with the hyphen). One file per component, named after the component (`ProfileForm.md`, `MetricCard.md`).
- A feature that is single-screen does not need `flow.md`.
- A feature that does not yet have a built implementation does not need `redlines/`.

## Component specs vs. shared design system

Component specs in `component-specs/` are scoped to the feature. They describe the variant of a component used in this spec package. If a component is genuinely shared across many features (a global Button, a global Modal), put its spec at the repo root in a `design-system/` directory and reference it from the feature's spec package — do not duplicate it inside every feature folder.

A canonical worked example is in [`examples/settings-page/`](../../examples/settings-page/).
