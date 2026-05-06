# Blueprint: Settings Page

## Layout Hierarchy
- **App Shell**
  - **Sidebar (Left Navigation - 250px fixed width)**
    - User Profile Badge (Avatar, Name, Email)
    - Navigation Menu (Profile, Notifications, Billing)
  - **Main Content Panel (Right - fluid width, max 800px)**
    - Header (Page Title: e.g., "Profile Settings")
    - Content Area (Form fields or billing details depending on active route)
    - Form Actions Footer (Sticky to bottom if scrolling: Save / Cancel)

## Breakpoints
- **Mobile (< 768px):** Sidebar becomes a top horizontal scrollable tab menu.
- **Desktop (>= 768px):** Split panel layout as described above.
