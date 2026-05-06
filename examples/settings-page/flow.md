# Flow: Settings Page

## Journey Graph
- **Entry point:** User clicks "Settings" in the main app header dropdown.
- **Node 1 [Profile Settings]:** Default view. User can edit name/avatar. 
  - -> Click "Save" -> Success Toast -> Stays on Profile.
- **Node 2 [Notification Settings]:** User clicks "Notifications" in sidebar.
  - -> Toggle switches -> Auto-saves (No save button required) -> Success Toast.
- **Node 3 [Billing Settings]:** User clicks "Billing" in sidebar.
  - -> Displays current plan -> Click "Manage" -> Redirects to Stripe Portal.
