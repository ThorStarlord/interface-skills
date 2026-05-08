# Spec Package Template

Use this directory as a starting point for a new Interface Skills spec package.

## Quick start

1. Copy this directory and rename it to describe your feature:
   ```bash
   cp -r templates/spec-package examples/my-feature
   ```
2. Work through the skills in order, saving each output as the corresponding file:
   ```
   ui-brief           → brief.md
   ui-visual-calibration → visual-calibration.md
   ui-flow            → flow.md
   ui-blueprint       → blueprint.md
   ui-system          → system.md
   ui-screen-spec     → screen-spec.md
   ui-component-spec  → component-specs/<name>.md
   ui-microcopy       → microcopy.md
   ui-acceptance      → acceptance.md
   ```
3. Use `00-index.md` to record which skills have been run and sign off each deliverable.

## Canonical example

See [`examples/settings-page/`](../../examples/settings-page/) for a complete, fully populated spec package demonstrating the expected format of every file above.

## File structure

```
my-feature/
├── 00-index.md          # Spec package index and sign-off sheet
├── brief.md             # Product/design brief (ui-brief)
├── visual-calibration.md # Visual taste → concrete decisions (ui-visual-calibration)
├── flow.md              # User journey graph (ui-flow)
├── blueprint.md         # Layout/wireframe spec (ui-blueprint)
├── system.md            # Tokens and design rules (ui-system)
├── screen-spec.md       # Screen contract (ui-screen-spec)
├── microcopy.md         # Approved copy (ui-microcopy)
├── acceptance.md        # Testable checklist (ui-acceptance)
└── component-specs/
    └── <ComponentName>.md   # Component anatomy spec (ui-component-spec)
```
