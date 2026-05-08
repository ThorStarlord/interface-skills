---
spec_type: blueprint
spec_id: app-shell-navigation
created: 2026-05-20
status: approved
---

# Blueprint: App Shell Navigation

## Layout Archetype
Sidebar App

## Regions

### 1. Project Switcher (Top)
- **Role:** Allows switching between different workspaces/projects.
- **Components:** `ProjectDropdown`

### 2. Primary Navigation (Center)
- **Role:** Main navigation links.
- **Components:** `SidebarNav`, `SidebarNavItem`

### 3. Account Area (Bottom)
- **Role:** User profile and global settings.
- **Components:** `UserMenu`, `LogoutButton`

## Responsiveness
- **Desktop:** Fixed width (240px) sidebar on the left.
- **Mobile:** Collapsed into a hamburger menu; opens as a full-height drawer from the left.
