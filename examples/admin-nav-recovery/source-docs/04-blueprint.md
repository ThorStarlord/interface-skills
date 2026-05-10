---
spec_type: blueprint
spec_id: admin-sidebar-nav
based_on: brief-admin-sidebar-nav
created: 2025-05-22
status: draft
---

# Blueprint: Admin Sidebar Navigation

## 1. Referenced brief
- **File:** `docs/saas-frontend/specs/admin-nav/02-brief.md`
- **Goal:** Persistent, reliable, "Calm Mission Control" navigation frame.
- **Primary user:** School directors/secretaries (Desktop-first).
- **Primary action:** Navigate between sections and modules.

## 2. Visual direction
- **Reference:** Linear (Density/Grouping), Stripe (Precision).
- **Archetype:** Sidebar App.
- **Density:** Medium (`px-7`, `space-y-9`).
- **Shape:** Rounded (`rounded-[28px]`, `rounded-full`).

## 3. Information hierarchy

| Rank | Element | Why it ranks here |
|---|---|---|
| 1 | **Active Tab Highlight** | Critical "You are here" feedback. |
| 2 | **Module Labels** | Primary navigation targets. |
| 3 | **Section Groups** | Cognitive grouping for task areas. |
| 4 | **Brand Identity** | School name and dashboard link. |
| 5 | **Section Toggle** | Manage density via expansion/collapse. |
| 6 | **Badges** | Status feedback for roadmap items. |

## 4. Wireframe — Desktop (1280px)

```
+------------------------------------------------------------+
| [Zap] Colégio Modelo          (Sidebar Header/Brand)       |
|       Gestão Escolar                                       |
+------------------------------------------------------------+
| [Home] Voltar aos Portais                                  |
| [Grid] Painel de Gestão       (Active if on /admin)        |
+------------------------------------------------------------+
|                                                            |
| SECRETARIA                                           [v]   |
|   [Sec] Atendimento           (Target: /admin/secretaria)  |
|   [Doc] Matrículas                                         |
|                                                            |
| FINANCEIRO (Active/Exp)                              [^]   |
|   [$] Dashboard Financeiro    (Target: /admin/finance)     | <-- RANK 1
|   [Up] Capturar (Inbox)                                    |
|                                                            |
| ACADÊMICO                                            [v]   |
|   [Gr] Turmas                                              |
|                                                            |
+------------------------------------------------------------+
```

### Reading order
1. **Active Highlight:** High-contrast indicator (`#28346c`).
2. **Section Titles:** BOLD UPPERCASE labels.
3. **Module Tabs:** Icons and labels within the active section.

## 5. Responsive behavior

| Breakpoint | Behavior | Reflow verb |
|---|---|---|
| Desktop (≥1024px) | Persistent Sidebar (420px). | — |
| Tablet (768–1023px) | Hidden by default; Drawer via Burger. | hide / swap |
| Mobile (<768px) | Same as Tablet; Full-width Drawer. | hide / swap |

## 6. What is NOT decided yet
- Exact color transitions for hover.
- Specific icon assignments for every future module.

## 7. Open questions
- Consolidating Brand and Dashboard links.

## 8. Assumptions made
- ⚠️ ASSUMED: Target canonical path `/admin/finance` is prioritized over `/admin/financeiro`.
