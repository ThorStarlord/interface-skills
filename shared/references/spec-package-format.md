# Spec Package Format

A spec package represents the single source of truth for a feature or component library. It groups all specification artifacts created by the UI skills together.

## Directory Structure

```text
feature-name/
  brief.md
  visual-calibration.md
  flow.md
  blueprint.md
  system.md
  screen-spec.md
  components/
    component-a.md
    component-b.md
  microcopy.md
  acceptance.md
  implementation-notes.md
  redlines/
    redline-001.md
```

## TODO (Human Review Required)
- [ ] Determine if `components/` should instead be a flat reference to a global design system or kept local to the feature.
