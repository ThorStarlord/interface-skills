---
spec_type: screen-spec
spec_id: admin-sidebar-nav
based_on: blueprint.md
created: 2025-05-22
status: draft
---

# Screen Spec: Admin Sidebar Navigation

## 1. Implied or referenced upstream docs
- **Brief:** `02-brief.md`
- **Blueprint:** `04-blueprint.md`
- **Calibration:** `03-visual-calibration.md`

## 2. Region map

### Region: Sidebar Header (`div`)
| Component | Data / props needed | Source | Needs component-spec? |
|---|---|---|---|
| `<BrandSection>` | `projectName`, `projectSlug` | Registry | No |
| `<HomeLink>` | — | Static | No |

### Region: Top Navigation (`nav`)
| Component | Data / props needed | Source | Needs component-spec? |
|---|---|---|---|
| `<PortalSwitcher>` | `roles` | Session | No |
| `<DashboardTab>` | `currentPath` | URL | Yes |

### Region: Module Navigation (`nav > section`)
| Component | Data / props needed | Source | Needs component-spec? |
|---|---|---|---|
| `<SectionToggle>` | `sectionLabel`, `isExpanded` | State | Yes |
| `<ModuleTab>` | `href`, `label`, `icon`, `isActive`, `badge` | Registry | Yes |

**State handling:**
| State | Responsible component | Behavior |
|---|---|---|
| Ideal | `<AdminSidebar>` | Renders sections and modules. |
| Loading | — | N/A (Static registry). |
| Error | — | N/A (Static registry). |
| Empty | — | N/A (Admin always has routes). |

---

## 3. Data dependencies
- `ADMIN_PRODUCT_SURFACE_ROUTES` (Static Registry)
- `usePathname` (Next.js Hook for active state)

## 4. Permission variants
- `admin` role only (other roles use different sidebar component).

## 5. Responsive composition changes
| Breakpoint | Region / component | Change | Reflow verb |
|---|---|---|---|
| Tablet / Mobile | Entire Sidebar | Replaced by Burger + Drawer | hide / swap |

## 6. Component-spec checklist
- [ ] `<AdminSidebar>` — Complex state (expansion, active mapping).
- [ ] `<ModuleTab>` — Precise visual and active state logic.

## 7. Open questions
- Redirection mapping for `/admin/financeiro`.

## 8. Assumptions made
- ⚠️ ASSUMED: Sidebar expands parent section on deep-link match.
