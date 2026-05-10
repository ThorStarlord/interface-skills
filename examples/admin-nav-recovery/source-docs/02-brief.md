---
spec_type: brief
spec_id: admin-sidebar-nav
created: 2025-05-22
status: draft
---

# Brief: Admin Sidebar Navigation (Retrospective)

## 1. Goal
Provide a persistent, reliable, and "Calm Mission Control" navigation frame that allows school operators to switch between administrative modules without losing context or feeling overwhelmed by technical complexity.

## 2. Primary user
- **Role / context:** School directors, secretaries, and coordinators. They are often multi-tasking and need to jump between enrollment, finance, and academic tasks quickly.
- **Technical literacy:** Novice to Intermediate. They are domain experts in school management but not technical experts; they require plain Portuguese labels and clear visual "you are here" indicators.
- **Primary device:** Desktop. While the app is responsive, the primary administrative work happens on school office computers.
- **Accessibility considerations:** High contrast for active states and keyboard navigability for power users.

## 3. Primary action
**Navigate:** Move between top-level administrative sections (Secretaria, Acadêmico, Financeiro, etc.) and their specific modules.

## 4. Secondary actions
- **Return to Dashboard:** Quick access to the "Painel de Gestão" for a high-level overview.
- **Toggle Sections:** Expand or collapse module groups to manage sidebar density.
- **Switch Portal:** Return to the portal selection screen ("Voltar aos Portais").

## 5. Why it matters
The sidebar is the "spine" of the admin experience. If the operator cannot tell which module they are currently in (broken active states) or if the navigation uses inconsistent terminology/paths (e.g., `financeiro` vs `finance`), it increases cognitive load and friction in high-stakes environments like school management.

## 6. Success criteria
- **Navigational Clarity:** 100% of "final" routes in the registry are reachable via the sidebar.
- **Active State Accuracy (Target):** The sidebar correctly highlights the active tab and expands the parent section for 100% of deep-linked sub-pages.
- **Path Consistency:** The sidebar exclusively uses the canonical `/admin/finance` path for the finance module in the "Target" state.
- **Performance:** Sidebar interaction (toggle/hover) remains fluid (< 100ms response) even with all sections expanded.

## 7. Constraints
- **Brand:** Must adhere to the "Warm Concierge" visual language and "Calm Mission Control" UX principles.
- **Platform:** Next.js App Router (Client Components for sidebar state).
- **Design Tokens:** Corner radius `rounded-[28px]` for containers; `p-8` for major internal padding.
- **Technical:** Must stay in sync with the registry in `lib/admin-product-surface.ts`.

## 8. Non-goals (what this is NOT)
- **NOT** a global search tool.
- **NOT** a place for notifications or real-time alerts.
- **NOT** responsible for navigation in Teacher, Student, or Parent portals.
- **NOT** responsible for in-page tabs or sub-navigation.

## 9. Open questions
1. **Consolidation:** Should we remove the "Painel de Gestão" link and make the "Colégio Modelo" brand logo the sole home link to reduce redundancy?
2. **Deep-link Depth:** How many levels of sub-navigation should the sidebar support before it becomes too dense? (Currently only supports one level via the registry).

## 10. Assumptions made in this brief
- ⚠️ **ASSUMED:** The target canonical path for Finance is `/admin/finance` despite the current code prioritizing `/admin/financeiro`.
- ⚠️ **ASSUMED:** The missing active state for sub-module tabs in the current implementation is an oversight/regression and not an intentional design choice.
- ⚠️ **ASSUMED:** "Calm Mission Control" implies that the sidebar should start with the relevant section expanded but others collapsed to reduce noise, unless on the dashboard.
