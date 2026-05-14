---
spec_type: inventory
spec_id: kanban-surface-inventory
created: 2026-05-14
status: approved
surface_type: multi-surface-map
---

# UI Surface Inventory: Pulse Kanban

## 3. App Shell Scopes
- [ ] **Left sidebar navigation**: Owns nav order, labels, active states.
- [ ] **Global Header**: Owns user profile, notifications, search.

## 6. Sub-surface Scopes
| Sub-surface | Parent route | User job | States | Component candidates |
|---|---|---|---|---|
| **Approval Queue** | `/admin/kanban` | Identifies kanban status columns | active | StatusColumn, KanbanCard |
| **Review/Deck Mode Toggle** | `/admin/kanban` | Switch between kanban and deck mode | active | ModeToggle |
| **Post Detail Modal** | `/admin/kanban` | View and edit post details | active | CaptionEditor |
| **Empty Queue State** | `/admin/kanban` | Display when empty | active | EmptyState |

## 7. Surface Status Table
| Surface | Type | Status | Existing spec? | Recommended next skill |
|---|---|---|---|---|
| `/admin/kanban` | route | pending | no | ui-inspector |
