# Token Schema

All `ui-system` definitions must follow this token schema structure.

## Schema Hierarchy
1. **Core / Primitive Tokens**: Absolute values (`color.blue.500: #3b82f6`, `space.4: 16px`).
2. **Semantic Tokens**: Meaning-based values (`color.action.primary: {color.blue.500}`).
3. **Component Tokens**: Component-specific values (`button.background.default: {color.action.primary}`).

## Required Semantic Categories
- `color.background.*`
- `color.surface.*`
- `color.text.*`
- `color.border.*`
- `color.action.*`
- `color.status.*` (success, warning, error, info)
- `space.*`
- `radius.*`
- `typography.*`
- `shadow.*`

## Mapping to common frameworks

The schema above is framework-agnostic. When `ui-generate-code` emits implementation code, semantic tokens map onto the following targets:

| Schema name              | Tailwind config key             | CSS variable form                |
|--------------------------|----------------------------------|----------------------------------|
| `color.background.*`     | `theme.colors.background`        | `--color-background-*`           |
| `color.surface.*`        | `theme.colors.surface`           | `--color-surface-*`              |
| `color.text.*`           | `theme.colors.text`              | `--color-text-*`                 |
| `color.border.*`         | `theme.colors.border`            | `--color-border-*`               |
| `color.action.*`         | `theme.colors.action`            | `--color-action-*`               |
| `color.status.*`         | `theme.colors.status`            | `--color-status-*`               |
| `space.*`                | `theme.spacing`                  | `--space-*`                      |
| `radius.*`               | `theme.borderRadius`             | `--radius-*`                     |
| `typography.*`           | `theme.fontFamily` / `fontSize`  | `--type-*`                       |
| `shadow.*`               | `theme.boxShadow`                | `--shadow-*`                     |

Component tokens (`button.background.default`) do not need to be exposed as CSS variables - they should resolve to a semantic token at build time. Only primitive and semantic tokens are part of the public theme API.
