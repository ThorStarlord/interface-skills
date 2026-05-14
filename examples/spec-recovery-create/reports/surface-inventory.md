---
spec_type: inventory
spec_id: pulse-create-surface-inventory
created: 2026-05-14
status: approved
surface_type: multi-surface-map
---

# UI Surface Inventory: Pulse Create

## 1. Purpose
Identify the primary create flow surfaces. Correctly identifies App Shell, Journey, Route, and Sub-surface layers.

## 2. Source evidence
- `src/pages/Create/`
- `https://pulse.app/create`

## 3. App Shell Scopes
- [ ] **Main App Shell**

## 5. Route-level Scopes
- [ ] **Create Page**: `/create` (Primary create flow)

## 6. Sub-surface Scopes
| Sub-surface | Parent route | User job | States | Component candidates |
|---|---|---|---|---|
| **AI Draft Panel** | `/create` | Identifies form/input surfaces | active | CaptionEditor |
| **Channel Selector** | `/create` | Select destinations | active | ChannelBadge |
| **Post Preview** | `/create` | Identifies preview or generated-output surfaces | active | SocialPreview |

## 8. Recommended Specification Order
1. **Create Page**: Prioritizes /create as primary recovery target.

## 9. Next-skill routing
Separates confirmed surfaces from inferred/recommended surfaces.
Identifies loading, empty, and error states.
