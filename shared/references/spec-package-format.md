# Spec Package Format

A spec package represents the single source of truth for a feature. It groups all specification artifacts created by the UI skills together so that any AI session can reconstruct the full decision history by reading the directory.

## Directory Structure

```text
feature-name/
  00-index.md                # Package index and sign-off sheet (required; canonical)
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

> **Canonical index: `00-index.md`.** Older packages may use `manifest.md` instead. When no `00-index.md` is present, tools fall back to `manifest.md` for compatibility.

## File-naming rules

- Use the canonical file names above. Downstream skills look for these exact names — renaming `blueprint.md` to `layout.md` will cause the next skill in the pipeline to fail to find it.
- The package index is `00-index.md`. It sorts first alphabetically, is obvious to humans, and is the preferred discovery signal used by `ui-docs-sync` and `ui-orchestrator`.
- If you are migrating an older package that uses `manifest.md`, rename it to `00-index.md`. Tools will still read `manifest.md` as a fallback, but `00-index.md` is authoritative when both are present.
- Component specs live in `component-specs/` (with the hyphen). One file per component, named after the component (`ProfileForm.md`, `MetricCard.md`).
- A feature that is single-screen does not need `flow.md`.
- A feature that does not yet have a built implementation does not need `redlines/`.

## Component specs vs. shared design system

Component specs in `component-specs/` are scoped to the feature. They describe the variant of a component used in this spec package. If a component is genuinely shared across many features (a global Button, a global Modal), put its spec at the repo root in a `design-system/` directory and reference it from the feature's spec package — do not duplicate it inside every feature folder.

A canonical worked example is in [`examples/settings-page/`](../../examples/settings-page/). Its package index is [`00-index.md`](../../examples/settings-page/00-index.md).
