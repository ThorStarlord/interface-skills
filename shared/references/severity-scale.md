# Severity Scale

This scale is used in redline audits (`ui-redline`) to prioritize UI fixes.

| Severity | Definition | Examples |
|----------|------------|----------|
| **Blocker** | Prevents core user task or severely violates accessibility. | Broken form submission, invisible text, focus trap missing on modal. |
| **Major** | Confusing UX, significant visual layout break, or missing state. | Button looks disabled but isn't, text clipping out of container, wrong breakpoint triggered. |
| **Minor** | Functional but rough — task is completable, but the result looks unfinished. | Wrong shade of gray, animation missing, hover state absent. |
| **Polish** | Subjective or extremely subtle divergence from spec, not in spec but worth raising. | Border radius is 6px instead of 8px, icon stroke inconsistency, subtle alignment improvement. |

## Mapping to common bug-tracker priorities

When integrating with an external tracker, map severities as follows:

| This scale | Jira / Linear priority | GitHub label suggestion |
|------------|------------------------|--------------------------|
| Blocker    | P0 / Urgent            | `bug:blocker`            |
| Major      | P1 / High              | `bug:major`              |
| Minor      | P2 / Medium            | `bug:minor`              |
| Polish     | P3 / Low               | `polish`                 |

Only Blocker and Major findings should gate a release. Minor and Polish findings are tracked but do not block.
