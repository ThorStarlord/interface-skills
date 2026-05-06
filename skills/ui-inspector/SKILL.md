---
name: ui-inspector
description: Turns diagnosis into evidence by gathering DOM/screenshot facts before redlining
---

# UI Inspector

This skill gathers implementation facts (DOM inventory, accessibility issues, computed styles, token usage) to provide evidence-based input for the `ui-redline` skill.

## TODO (Human Review Required)
- [ ] Define what external scripts or tools (e.g., axe-core, Playwright) the inspector is expected to trigger or mimic.
- [ ] Document the schema for the evidence report passed to `ui-redline`.
