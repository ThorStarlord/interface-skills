---
spec_type: brief
spec_id: app-shell-navigation
created: 2026-05-20
status: approved
---

# Brief: App Shell Navigation

## 1. Goal
Provide a persistent, reliable frame for the application that allows users to navigate between product areas and manage their account context.

## 2. Primary user
- **Role / context:** Multi-tenant SaaS user performing various content creation and management tasks.
- **Technical literacy:** Intermediate; familiar with standard SaaS navigation patterns.
- **Primary device:** Desktop (web browser) is primary; must also support mobile via a drawer.
- **Accessibility considerations:** Must be fully keyboard navigable with clear focus indicators.

## 3. Primary action
Navigate between product areas.

## 4. Secondary actions
- Switch projects/tenants.
- Access user settings.
- View notifications (badges).
- Log out.

## 5. Why it matters
The app shell is the "anchor" for the user. Without a clear and persistent navigation frame, users feel lost and the relationship between different product features becomes opaque.

## 6. Success criteria
- Users can switch between any two top-level product areas in two clicks or less.
- 100% of primary navigation items have clear, descriptive labels.
- Active state is visually distinct and matches the current route.

## 7. Constraints
- **Brand:** Use the "Muted Neutral" palette defined in global brand guidelines.
- **Platform:** Web (React).
- **Regulatory / compliance:** WCAG 2.1 AA.

## 8. Non-goals (what this is NOT)
- This is NOT for page-specific actions (e.g., "Save", "Export").
- This is NOT for multi-step creation wizards.

## 9. Open Questions
None.

## 10. Assumptions made in this brief
- ⚠️ ASSUMED: The sidebar is the preferred navigation pattern over a top bar.
