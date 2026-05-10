---
spec_type: inventory
spec_id: admin-sidebar-nav
created: 2025-05-22
status: draft
---

# UI Surface Inventory: Admin Sidebar Navigation

## 1. App Shell Scopes
- [x] **Admin Sidebar**: Persistent left-side navigation for the admin portal. It owns section grouping, tab labels, route mapping, active-state highlighting, and visibility based on feature state.
- [ ] **Portal Header**: Persistent top bar (out of scope for this task, but part of the shell).

## 2. Journey Scopes
- [ ] **Admin Navigation Journey**: The flow of moving between different administrative modules (Secretaria -> Financeiro -> Academico) while maintaining context and clear visual feedback on the current location.

## 3. Route-level Scopes
- [ ] **Admin Dashboard** (`/admin`): The entry point that provides an overview and quick access to modules.
- [ ] **Secretaria Modules** (`/admin/secretaria/*`): Attendance, Enrollments, Students, Platforms, etc.
- [ ] **Academico Modules** (`/admin/academico/*`): Curriculum, Classes, Schedule, etc.
- [ ] **Pedagogico Modules** (`/admin/pedagogico/*`): Planning, Portfolios, Projects, etc.
- [ ] **Financeiro Modules** (`/admin/financeiro/*`): Dashboard, Inbox, Cash Flow, etc. (Targeting `/admin/finance` as canonical).
- [ ] **Administracao Modules** (`/admin/administracao/*`): HR, Procurement, Infrastructure.
- [ ] **Conciliacao Modules** (`/admin/conciliacao/*`): Data sources, Imports, Reconciliation.

## 4. Sub-surface Scopes
| Sub-surface | Parent route | User job | States | Component candidates |
|---|---|---|---|---|
| **Section Accordion** | Admin Sidebar | Toggle visibility of module groups | Expanded, Collapsed | `AdminSidebar` (button/chevron) |
| **Nav Tab** | Admin Sidebar | Navigate to specific route | Active, Inactive, Hover, Badge (Demo/Soon) | `Link`, `LucideIcon`, `Badge` |
| **Sidebar Brand** | Admin Sidebar | Quick return to home and branding | Hover | `Link`, `Zap` Icon |

## 5. Recommended Specification Order
1. **Admin Sidebar Navigation Map**: (This task) Priority #1 because it provides the structure for the entire admin experience.
2. **Financeiro Navigation Map**: Specific focus on reconciling `/admin/finance` vs `/admin/financeiro` and ensuring operator clarity in the most critical module.

## 6. Open Questions / Ambiguities
- How exactly do the legacy redirects from `/admin/financeiro` to `/admin/finance` (target) impact the sidebar's "active" state highlighting?
- When an operator is at `/admin/financeiro/inbox`, which tab and section should be highlighted given the target is `/admin/finance`?
- Are "Demo" and "Em breve" badges purely hardcoded in `admin-product-surface.ts` or can they be dynamic?
