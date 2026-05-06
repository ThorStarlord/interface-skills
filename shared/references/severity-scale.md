# Severity Scale

This scale is used in redline audits (`ui-redline`) to prioritize UI fixes.

| Severity | Definition | Examples |
|----------|------------|----------|
| **Blocker** | Prevents core user task or severely violates accessibility. | Broken form submission, invisible text, focus trap missing on modal. |
| **Major** | Confusing UX, significant visual layout break, or missing state. | Button looks disabled but isn't, text clipping out of container, wrong breakpoint triggered. |
| **Minor** | Visual polish issue that does not prevent task completion. | Padding is off by a few pixels, wrong shade of gray used, animation missing. |
| **Nit** | Subjective or extremely subtle divergence from spec. | Border radius is 6px instead of 8px. |

## TODO (Human Review Required)
- [ ] Align with any existing bug tracking terminology.
