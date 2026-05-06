# Screen Spec: Settings Page

## Component Instantiation and Region Mapping

### Region: Sidebar (`<aside>`)
- **`NavigationMenu`**: Receives `activeItem` from page context.
- **`UserProfileBadge`**: Requires user object (avatar, name).

### Region: Main Content (`<main>`)
- **`DashboardHeader`**: Contains page title.
- **`ProfileSettingsForm`**: Renders inputs for Name and Avatar.
- **`FormActions`**: Contains Save and Cancel buttons.

## State Ownership and Taxonomy
- **Ideal State:** Form fields populated with current user data.
- **Loading State:** Skeleton loaders for input fields while fetching user profile.
- **Error State:** Global error banner if fetching fails ("Could not load settings"). Inline validation errors for form fields.
- **Pending State:** Save button shows spinner and is disabled while submitting.
