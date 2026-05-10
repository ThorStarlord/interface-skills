# Admin-Nav Fixture Notes

## Human review

- Machine validation: pass
- Human review required: yes
- Human status: pending
- Reviewer:
- Review date:
- Notes:
  - This fixture is in construction phase. Validation of responses against real admin-nav UI surfaces from ThorStarlord/metamorfose-edutech is pending. All skill learnings documented; source files not yet snapshot.

## Downstream consumption

- `ui-redline` consumes:
  - `input/inspector-findings.md`
- `ui-spec-reconcile` consumes:
  - `input/spec-reconcile-input.md`
- `ui-docs-sync` consumes:
  - `input/docs-sync-input.md`
- `ui-to-issues` consumes:
  - `reports/REDLINE-PARTIAL.md`

- **Created:** 2026-05-10
- **Freeze Status:** ⏸️ Not frozen (awaiting source population and validation)
- **Fixture refresh marker:** `manual-refresh-awaiting-source`
- **Source snapshot refresh marker:** `awaiting-source-commit`

---

## Human Review Questions

These questions must be answered before marking fixture as validated:

### 1. Route Registry Canonicality

**Question:** Is `/admin/finance` truly the canonical route over the legacy `/admin/financeiro` path?

**Why it matters:** The inspector found both paths in the code. The reconcile decision should clarify which is the target spec.

**Evidence needed:**
- [ ] Source repo confirms `/admin/finance` is current
- [ ] Documentation or issue explains the migration path
- [ ] Active code paths only use `/admin/finance`

**Decision:** _[To be filled during fixture population]_

---

### 2. Admin Sidebar Duplicate Links Policy

**Question:** Should Brand and Dashboard appearing twice in the sidebar be accepted as intended design, or is one instance redundant polish?

**Why it matters:** The redline flags duplicate links as potential issues. The issue plan may defer them. This clarifies intent.

**Evidence needed:**
- [ ] Product spec or design system clarifies duplicate link purpose
- [ ] Accessibility reasoning (if intentional) documented
- [ ] Visual hierarchy shows intentional distinction

**Decision:** _[To be filled during fixture population]_

---

### 3. System.md Requirement for Navigation Surfaces

**Question:** Should a narrow navigation-map surface require system.md documentation, or is it acceptable to have only inventory + spec + redlines?

**Why it matters:** The first lint report marked missing system.md as a failure. The fixture should clarify whether this is a hard requirement or surface-type-dependent.

**Evidence needed:**
- [ ] Navigation surfaces CAN omit system.md (surface-type exception)
- [ ] Or: all surfaces MUST include system.md (hard requirement)

**Guideline:** For app-shell surfaces, system.md may not be necessary if the surface is narrowly scoped to navigation logic.

**Decision:** _[To be filled during fixture population]_

---

### 4. Sidebar Container Rounded Corners

**Question:** Is `rounded-[28px]` required on the sidebar container itself, or only on shell surface tokens?

**Why it matters:** The redline flags rounded corner precision as a visual polish item. The spec should clarify whether this is a must-have or deferred polish.

**Evidence needed:**
- [ ] Token system defines default radius for containers
- [ ] Design system spec includes or excludes this specific radius
- [ ] Current implementation radius measured and compared

**Decision:** _[To be filled during fixture population]_

---

## Fixture Population Checklist

### Source Snapshot (awaiting)

- [ ] Source commit pinned in fixture.yaml
- [ ] Source code files captured (portal-shell.tsx, admin-product-surface.ts, etc.)
- [ ] Spec docs from source repo copied to source-docs/

### Inputs (awaiting)

- [ ] surface-inventory.md: discovered surfaces and structure
- [ ] inspector-findings.md: static inspection with confidence notes
- [ ] spec-reconcile-input.md: redlines and implementation audit
- [ ] docs-sync-input.md: agent docs discovered and links audited

### Reports (awaiting)

- [ ] All 8 skill outputs in reports/ folder
- [ ] Each report includes required fields (status, result, findings, next_skill)

### Rubric Validation (awaiting)

- [ ] expected/rubric.md written with acceptance criteria
- [ ] All rubric items are SMART (specific, measurable, achievable, relevant, time-bound)
- [ ] Coverage gap audit completed

---

## Key Learning Artifacts

These are the specific outputs that teach draft skills:

1. **SURFACE-INVENTORY-V1.md**
   - Teaches: `ui-surface-inventory` should include `surface_type: app-shell-navigation`
   - Look for: explicit taxonomy of surfaces (admin-sidebar, route-registry, agent-docs)

2. **INSPECTOR-REPORT-V1.md**
   - Teaches: Static-only reports need `inspection_method`, `runtime_verified`, `partial` fields
   - Look for: clear separation of "verified by source", "inferred from source", "requires live DOM"
   - Evidence: missing aria-current, hardcoded colors, finance path inconsistency (findable in source)

3. **SPEC-LINT-REPORT-V2.md**
   - Teaches: `ui-spec-linter` should distinguish `spec_consistency: pass` from `implementation_alignment: not_checked`
   - Look for: PASS but with caveat about implementation gaps
   - Evidence: V2 says PASS but reconciliation still shows gaps

4. **SPEC-RECONCILE-SUMMARY.md**
   - Teaches: `ui-spec-reconcile` needs `target-only reconciled` result category
   - Look for: spec is stable, but implementation still awaits refactor
   - Evidence: finance path decision made, but code still uses legacy path

5. **DOCS-SYNC-REPORT.md**
   - Teaches: `ui-docs-sync` must support nested monorepo agent files (root + app-level)
   - Look for: checks across root AGENTS.md, metamorfose-platform/AGENTS.md, CONTEXT.md
   - Evidence: found missing links in nested files

6. **UI-AGENT-ROUTING-REPORT.md**
   - Teaches: `ui-agent-routing` should use explicit statuses (done/missing/planned/not_applicable)
   - Look for: report-mode output that FAILS without applying patches
   - Evidence: 2 items unresolved (root AGENTS.md, CLAUDE.md wiring)

7. **REDLINE-PARTIAL.md**
   - Teaches: `ui-redline` must include "What I could not verify" section for partial redlines
   - Look for: static-only inspection with explicit confidence limits
   - Evidence: hover transitions, color accuracy, screen reader prosody marked as unverifiable

8. **GITHUB-ISSUES-PLAN.md**
   - Teaches: `ui-to-issues` should include redline-to-issue coverage map
   - Look for: explicit mapping of 6 redline items to 4 issues
   - Evidence: coverage table showing which redlines are covered/deferred

---

## Re-run Recipe

When fixture needs refresh or new data:

```bash
# 1. Update source snapshot (if source repo available)
# cp ThorStarlord/metamorfose-edutech/docs/saas-frontend/specs/admin-nav/* ./source-docs/

# 2. Run inventory/inspector to refresh inputs
# python scripts/run-surface-inventory.py ...
# python scripts/run-inspector.py ...

# 3. Re-run full workflow
# python scripts/validate-examples.py examples/admin-nav-recovery --strict-local-sources

# 4. Update human-review answers and marking as complete
```

---

## Validator Notes

This fixture is subject to these validation rules:

1. **Fixture freeze marker required:** Manual override marker must be present if fixture.yaml is modified
2. **Source snapshot presence:** Reports/ must exist; source-docs/ optional but recommended
3. **Supersession rule:** If SPEC-LINT-REPORT.md exists, SPEC-LINT-REPORT-V2.md must reference it
4. **Redline coverage:** Every critical redline item (K-*) must map to a GitHub issue or be marked deferred
5. **Nested agent docs:** DOCS-SYNC-REPORT.md must check both root and app-level AGENTS.md
6. **Report-mode handling:** UI-AGENT-ROUTING-REPORT.md can FAIL; agent routing in report mode is expected behavior

---

## Notes for Implementer

**Why this fixture matters:**

Interface Skills has proven itself on **content workflow surfaces** (/kanban spec recovery). This fixture proves it can handle:

- **Navigation and infrastructure surfaces** (route registries, active states, shell components)
- **Partial static verification** (not all UI properties are discoverable from source)
- **Monorepo documentation** (nested AGENTS.md, CONTEXT.md across platforms)
- **Report-mode operations** (agents can audit and fail to resolve without being failures)

**When to populate:**

1. After both `/kanban` and `admin-nav-recovery` fixtures are created
2. When source repo (ThorStarlord/metamorfose-edutech) is available locally
3. When draft skills have been updated with the 8 concrete improvements
4. Before marking draft skills ready for broader testing

**Expected timeline:**

- Fixture structure: ✅ Done (2026-05-10)
- Source population: In progress (awaiting source repo access and commit pinning)
- Skill improvements: In progress (applying 8 concrete changes)
- Full validation: Pending (after inputs and reports are populated)
