---
spec_type: system
spec_id: settings-account
created: 2026-05-06
status: draft
---

# System: Prosper Settings Page

Tokens follow the three-tier hierarchy from [`shared/references/token-schema.md`](shared/references/token-schema.md): primitive -> semantic -> component. Only primitive and semantic tokens are listed here. Component tokens (`button.background.default`, etc.) resolve at build time and are documented in the component specs.

## 1. Primitive (literal) tokens

### Color
```
color.gray.50  : #F9FAFB
color.gray.100 : #F3F4F6
color.gray.200 : #E5E7EB
color.gray.500 : #6B7280
color.gray.700 : #374151
color.gray.900 : #111827
color.white    : #FFFFFF
color.blue.500 : #2563EB
color.blue.600 : #1D4ED8
color.green.500: #10B981
color.red.500  : #EF4444
```

### Spacing (4px base unit)
```
space.1 : 4px     space.5 : 20px
space.2 : 8px     space.6 : 24px
space.3 : 12px    space.8 : 32px
space.4 : 16px    space.10: 40px
```

### Radius
```
radius.sm : 4px
radius.md : 6px
radius.lg : 8px
```

### Typography
```
type.family.sans : "Inter", system-ui, sans-serif
type.size.sm     : 13px
type.size.md     : 14px
type.size.lg     : 18px
type.size.xl     : 24px
type.weight.regular : 400
type.weight.semibold: 600
```

### Shadow
```
shadow.sm : 0 1px 2px rgba(0,0,0,0.05)
shadow.md : 0 4px 12px rgba(0,0,0,0.08)
```

## 2. Semantic tokens

### `color.background.*`
| Token                       | Resolves to     | Used for                                    |
|-----------------------------|-----------------|---------------------------------------------|
| `color.background.app`      | `color.white`   | Page background                             |
| `color.background.subtle`   | `color.gray.50` | Hover row background, sidebar background    |

### `color.surface.*`
| Token                       | Resolves to     | Used for                                    |
|-----------------------------|-----------------|---------------------------------------------|
| `color.surface.default`     | `color.white`   | Cards, inputs                                |
| `color.surface.elevated`    | `color.white`   | Modals, dropdowns (paired with `shadow.md`) |

### `color.text.*`
| Token                       | Resolves to     | Used for                                     |
|-----------------------------|-----------------|----------------------------------------------|
| `color.text.primary`        | `color.gray.900`| Body text, headings                          |
| `color.text.secondary`      | `color.gray.500`| Helper text, meta, labels of read-only data  |
| `color.text.on-action`      | `color.white`   | Text on a primary action button              |
| `color.text.action`         | `color.blue.500`| Inline links                                 |

### `color.border.*`
| Token                       | Resolves to     | Used for                                     |
|-----------------------------|-----------------|----------------------------------------------|
| `color.border.default`      | `color.gray.200`| Input borders, card borders, dividers         |
| `color.border.focus`        | `color.blue.500`| Input focus ring (with 2px outline)           |

### `color.action.*`
| Token                       | Resolves to     | Used for                                     |
|-----------------------------|-----------------|----------------------------------------------|
| `color.action.primary`      | `color.blue.500`| Primary buttons, active sidebar item indicator|
| `color.action.primary-hover`| `color.blue.600`| Hover state of primary action                 |

### `color.status.*`
| Token                       | Resolves to     | Used for                                     |
|-----------------------------|-----------------|----------------------------------------------|
| `color.status.success`      | `color.green.500`| Success toasts, autosave confirmation dot   |
| `color.status.error`        | `color.red.500` | Inline error text, error toast border        |

### Typography (semantic)
| Token                  | Definition                                                      |
|------------------------|-----------------------------------------------------------------|
| `type.heading.lg`      | family `sans`, size `xl`, weight `semibold`, line-height 1.3    |
| `type.heading.md`      | family `sans`, size `lg`, weight `semibold`, line-height 1.4    |
| `type.body.md`         | family `sans`, size `md`, weight `regular`, line-height 1.5     |
| `type.body.sm`         | family `sans`, size `sm`, weight `regular`, line-height 1.5     |

## 3. Layout rules

- **Container**: max-width 720px for the main form panel, centered.
- **Form vertical rhythm**: `space.4` between rows of one logical group; `space.6` between groups; `space.8` between top-level sections.
- **Touch target minimum**: 40px (matches default input height; meets WCAG 2.2 SC 2.5.8 Target Size (Minimum), Level AA).
- **Focus ring**: 2px outline at `color.border.focus`, offset 2px from the element. Never removed without a `focus-visible` replacement.

## 4. What this system does *not* define

Animation/motion tokens are not part of this spec — the brief did not require any custom motion. Default browser transitions on hover/focus apply.
