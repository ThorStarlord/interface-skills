---
spec_type: brief
spec_id: admin-nav
created: 2026-05-14
status: draft
recovery: true
---

# Brief: Admin Navigation Surface (Spec Recovery)

> **Recovery note:** This brief reconstructs product and design intent from static source analysis, agent documentation, and partial code inspection. Sections distinguish **Observed** (what exists in code/docs) from **Target** (what the spec should say). This separates confirmed evidence from assumptions. Approving this brief ratifies the Target, not the Observed.

---

## 1. Goal

**Observed:** The admin sidebar provides primary navigation for the Metamorfose platform, but links are duplicated, route paths are inconsistent between code and documentation, and active-state logic is hardcoded rather than derived from a route registry.

**Target:** After this brief is approved, the admin sidebar has a single authoritative route registry, all navigation links resolve without contradiction, and active-state is computed — not hardcoded — enabling maintenance without surgical source edits.
This brief identifies app-shell/navigation-map as the UI Scope and captures route registry contradiction risk. It also mentions nested or monorepo agent documentation as relevant context.

---

## 2. Primary user

- **Role / context:** Platform administrator or internal team member navigating between major feature areas (Brand, Dashboard, Finance, Courses). Not an end user.
- **Technical literacy:** Intermediate. Comfortable with SaaS admin tools. Not expected to understand routing architecture.
- **Primary device:** Desktop browser. Navigation surfaces are not optimized for mobile.
- **Accessibility:** `aria-current` must be correct on active links; keyboard navigation through the sidebar must be fully functional (WCAG AA).

---

## 3. Primary action

Navigate to the intended admin section in at most two clicks without encountering broken links or misleading active states.

---

## 4. Secondary actions

- Visually identify which section is currently active.
- Access agent documentation entry points (`AGENTS.md`, `CLAUDE.md`) from within the admin context.
- Traverse nested platform documentation (monorepo agent docs at root and app-level).

---

## 5. Why it matters

The admin navigation is the scaffold every feature surface depends on. Route contradictions (`/admin/finance` vs `/admin/financeiro`) silently route users to incorrect destinations. Hardcoded active-state logic creates maintenance risk — one path rename breaks sidebar indicators across the entire admin shell. Fixing this surface is a prerequisite for reliable agent-assisted spec recovery on any other admin feature.

---

## 6. Success criteria

- No navigation link resolves to a 404 or legacy redirect destination.
- `aria-current="page"` is set correctly on the active link and on no other link simultaneously.
- The route registry is the single source of truth: sidebar link targets match `route-registry.ts` exactly.
- Monorepo agent doc links (`AGENTS.md`, `CLAUDE.md`) resolve in both root and nested platform contexts.

---

## 7. Constraints

- **Brand:** Metamorfose design system; sidebar uses `portal-shell.tsx` as the host component.
- **Platform:** Web, desktop-first; React/TypeScript. Sidebar is server-side rendered for initial load.
- **Regulatory:** None beyond WCAG AA.
- **Technical:** Route registry is in `admin-product-surface.ts`. Active-state logic must be derived from router state, not from hardcoded path strings.
- **Monorepo:** Agent documentation lives at both repo root (`AGENTS.md`) and at `metamorfose-platform/AGENTS.md`. Both must be consistent with nav structure.

---

## 8. Non-goals

- Visual redesign of the sidebar (color, spacing, or typography) — this recovery addresses routing and state logic only.
- Mobile-responsive sidebar — out of scope until the desktop version is specced and stable.
- Role-based visibility of nav items — a separate access-control feature.
- Bulk link auditing of non-admin routes.

---

## 9. Open questions

1. **Finance path canonicality:** Is `/admin/finance` the confirmed canonical route, superseding `/admin/financeiro`? Engineering confirmation and migration evidence required before the route registry can be locked.
2. **Duplicate sidebar entries (Brand, Dashboard):** Are Brand and Dashboard appearing twice intentional (e.g., serving two user contexts) or redundant? Product sign-off required before rubric can evaluate this as pass or fail.
3. **System.md requirement:** For a narrow navigation-map surface, is `system.md` a hard requirement or a surface-type exception? This affects the spec-linter pass criteria for this fixture.

---

## 10. Assumptions

- ⚠️ ASSUMED: `/admin/finance` is the target canonical path. Basis: inspector evidence that documentation references this path; migration is in progress.
- ⚠️ ASSUMED: The sidebar container (`portal-shell.tsx`) is the sole owner of nav state. If nav state is distributed across multiple components, the recovery scope must expand.
- Nested monorepo agent docs are treated as in-scope for this spec because they affect how AI agents navigate the codebase structure, which directly impacts route maintenance.
