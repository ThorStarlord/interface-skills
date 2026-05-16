# Storybook Documentation Source: Prosper Settings Page

This is the comprehensive source storybook documentation repository and component library setup for the Prosper Settings Page. It acts as the ground-truth reference for validating and syncing modern React component stories, properties, interaction testing, and inline markdown docs.

## 1. Scope and Architectural Objectives
The main goal is to generate, align, and sync storybook markdown files (`.stories.mdx` formats) for the following components:
1. `ProfileForm` - The complex profile detail and configuration form.
2. `UserProfileBadge` - Sidebar widget for user profile avatar and metadata.
3. `SettingsSidebar` - Main tabbed navigation panel for user options.
4. `FormActions` - Standard sticky action bar matching submitting states.
5. `SettingsContent` - Multi-pane content layout system.

## 2. Directory Hierarchy and Output Conventions
- `ComponentName.stories.mdx` (Root-level verification artifact)
- `specs/ComponentName.stories.mdx` (Specification-level storybook copy)
- `docs/ComponentName.stories.mdx` (Synchronized documentation-level copy)

All components must contain clear descriptions, full state coverage (Loading, Empty, Edited, Submitting, Success, Inline Error, and Global Error), and robust Tab/Enter keyboard accessibility mappings matching the accessibility baseline.
