---
name: ui-spec-linter
description: Prevents bad specs from reaching code by validating completeness and internal consistency.
---

# UI Spec Linter

This skill validates the entire spec package before code generation begins. It checks for undefined tokens, vague language, incomplete states, and missing acceptance criteria.

## TODO (Human Review Required)
- [ ] Determine the output format of a lint failure (e.g., Markdown table with severity).
- [ ] Decide whether the linter should auto-fix simple issues or strictly demand user intervention.
