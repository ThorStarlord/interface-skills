---
spec_type: lint-report
spec_id: admin-sidebar-nav
based_on: All docs in docs/saas-frontend/specs/admin-nav/
created: 2025-05-22
status: draft
---

# Spec Lint Report: Admin Sidebar Navigation

**Package:** admin-sidebar-nav
**Date:** 2025-05-22
**Result:** FAIL (2 issues found)

## Issues

| Severity | Category | File | Issue | Suggested Fix |
|---|---|---|---|---|
| blocker | Consistency | 02-brief.md | Path mismatch: Brief targets `/admin/finance` but registry uses `/admin/financeiro`. | Confirm redirect shim logic. |
| major | Completeness | (Package) | Missing `system.md`. Token definitions are currently inline in Calibration. | Create a `system.md` to consolidate tokens. |

## Summary

- **Blockers:** 1
- **Major:** 1
- **Minor:** 0
- **Passed checks:** 15

## Next step
Resolve the **Finance Path blocker** by confirming the migration strategy. Create the `system.md` file.
