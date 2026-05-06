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

## TODO (Human Review Required)
- [ ] Align the required semantic categories with the user's preferred styling framework (e.g., Tailwind CSS, styled-components).
