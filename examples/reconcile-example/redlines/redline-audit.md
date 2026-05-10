---
spec_type: redline-audit
scope: reconcile-example
status: complete
---

# Redline Audit: Reconcile Example

## 1. Mismatches Found

### [Major] #1: Primary action label is "Sync" not "Reconcile"
- **Observed:** Button says "Sync"
- **Target:** Button should say "Reconcile"
- **Fix:** Update `Brief.tsx` to use "Reconcile".

### [Minor] #2: Missing ARIA label on primary action
- **Observed:** `<button>Sync</button>`
- **Target:** `<button aria-label="Synchronize data">Sync</button>`
- **Fix:** Add `aria-label`.