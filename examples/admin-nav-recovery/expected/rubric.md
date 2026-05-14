# Admin-Nav Fixture Rubric

## Acceptance Criteria

This rubric defines what constitutes a "good" output for each skill in the admin-nav retrospective-specification workflow. Outputs are validated against these criteria.

---

## 1. ui-surface-inventory

### Required Fields

- [ ] `surface_type` field includes `app-shell-navigation`
- [ ] Surfaces enumerated with explicit scope (e.g., `/admin/*`, `portal-shell.tsx`)
- [ ] Role assignments (primary-navigation-target, source-of-truth-for-active-routes, etc.)

### Content Requirements

- [ ] Admin Sidebar identified as primary navigation surface
- [ ] Route registry identified as infrastructure surface (not content)
- [ ] Agent docs surfaces listed with monorepo scope notation
- [ ] Journey map includes sidebar active-state lifecycle
- [ ] Sub-surfaces: Brand, Dashboard, Section Accordion, Nav Tab

### Completeness Check

- [ ] At least 5 distinct surfaces enumerated
- [ ] Each surface has explicit `type` and `scope`
- [ ] Navigation is distinguished from content in terminology

---

## 2. ui-inspector

### Static-Only Report Requirements

- [ ] Header includes: `inspection_method: static source-code`
- [ ] Header includes: `runtime_verified: false`
- [ ] Header includes: `partial: true`
- [ ] Confidence marker on each finding (e.g., "verified by source", "inferred from source", "requires live DOM")

### Findings Must Include

- [ ] Active state logic (hardcoded vs computed — verifiable in source)
- [ ] ARIA accessibility markers (missing `aria-current`, `aria-hidden` — verifiable in source)
- [ ] Route registry inspection (finance path inconsistency — verifiable in source)
- [ ] Color specifications (hardcoded rgba vs token reference — verifiable but hard to verify accuracy)
- [ ] Hover/transition logic (marked as "requires live DOM")

### Completeness Check

- [ ] At least 4 findings documented
- [ ] At least 2 findings explicitly marked "requires live DOM"
- [ ] No overclaiming (findings don't claim runtime verification without browser evidence)

---

## 3. ui-spec-linter

### V2 Report Requirements

- [ ] Header includes: `spec_consistency: pass` OR `spec_consistency: fail`
- [ ] Header includes: `implementation_alignment: [not_checked | partial | ready]`
- [ ] If `spec_consistency: pass` and `implementation_alignment: not_checked`, output says:
  ```
  Spec package passes internal consistency checks.
  Implementation may still require redline fixes.
  ```

### Supersession Rule

- [ ] If SPEC-LINT-REPORT.md exists, V2 header must include:
  ```yaml
  supersedes: SPEC-LINT-REPORT.md
  ```

### Completeness Check

- [ ] No ambiguous "ready for implementation" claims
- [ ] Distinction between spec consistency and implementation alignment is clear
- [ ] If V1 existed and was a FAIL, V2 explicitly cites what was fixed

---

## 4. ui-spec-reconcile

### Result Categories

- [ ] Result is one of: `fully reconciled`, `target-only reconciled`, `implementation-only reconciled`, `partially reconciled`, `blocked by product decision`
- [ ] For admin-nav, result should be: **`target-only reconciled`**

### Required Content

- [ ] Spec stabilized decision for each contradiction
- [ ] Finance path decision documented (canonical route chosen)
- [ ] Implementation gaps explicitly listed (code still uses legacy path, polish items deferred)
- [ ] Clear statement: "Spec is stable; implementation awaits refactor"

### Completeness Check

- [ ] At least 2 contradictions identified and resolved
- [ ] Finance path contradiction explicitly addressed
- [ ] No contradiction left unresolved in the "target-only" decision set

---

## 5. ui-docs-sync

### Monorepo Scope Requirement

- [ ] Report checks: root AGENTS.md
- [ ] Report checks: metamorfose-platform/AGENTS.md (app-level)
- [ ] Report checks: root CONTEXT.md
- [ ] Report checks: metamorfose-platform/CONTEXT.md (if it exists)

### Link Audit Results

- [ ] For each checked file, findings show:
  - [ ] Links found to the admin-nav package (if any)
  - [ ] Links that SHOULD exist (based on surface.yaml or routing)
  - [ ] Gaps identified (missing links)

### Completeness Check

- [ ] At least 2 agent doc files checked
- [ ] At least 1 gap identified (missing link in AGENTS.md)
- [ ] Clear guidance on what needs to be added to agent docs

---

## 6. ui-agent-routing

### Report-Mode Output

- [ ] Mode is explicit: `mode: report` (not applying patches)
- [ ] Status is explicit: `agent_routing: partial` or `agent_routing: fail`
- [ ] Result must be FAIL for admin-nav (unresolved items OK in report mode)

### Status Field Requirements

- [ ] Each item uses explicit status: `done` | `missing` | `planned` | `not_applicable`
- [ ] No checkboxes or ambiguous "planned" appearance
- [ ] Unresolved items clearly listed

### Findings Must Include

- [ ] root AGENTS.md wiring status (missing or incomplete — expected)
- [ ] metamorfose-platform/AGENTS.md wiring status
- [ ] CLAUDE.md reference status (if checked)
- [ ] 00-index.md "How agents find this" section status

### Completeness Check

- [ ] At least 2 items marked `missing`
- [ ] At least 1 item marked `done` (partial success)
- [ ] Final result is FAIL (unresolved items expected in report mode)

---

## 7. ui-redline

### Partial Redline Requirements

- [ ] Header includes: `redline_mode: static partial`
- [ ] Header includes: `partial: true`
- [ ] Confidence breakdown included:
  ```
  verified by source: [count]
  inferred from source: [count]
  requires live DOM: [count]
  ```

### "What I Could Not Verify" Section

- [ ] Explicitly lists unverifiable items:
  - [ ] Hover transition timing (requires live browser)
  - [ ] Color accuracy at runtime (shadows, opacity, blending)
  - [ ] Screen reader prosody and announcement order
  - [ ] Focus visible indicators (varies by browser)

### Findings Format

- [ ] Each finding includes: `[K-#] [Category] Issue | Verified by | Next Step`
- [ ] Example: `[K-3] Accessibility | missing aria-current on active link | source code | add aria-current`

### Completeness Check

- [ ] At least 5 findings documented
- [ ] At least 2 findings marked "requires live DOM"
- [ ] Clear separation between verified and unverifiable findings

---

## 8. ui-to-issues

### Redline-to-Issue Coverage Map

- [ ] Table showing each redline item mapped to 0..n issues
- [ ] Format:
  ```markdown
  | Redline | Issue | Status |
  |---------|-------|--------|
  | [K-1] Finance path | issue#2 | covered |
  | [K-2] Active state | issue#1 | covered |
  | ...
  | [K-6] Duplicate links | deferred-polish | known |
  ```

### Issue Requirements

- [ ] At least 3 issues created from redlines
- [ ] Each issue has acceptance criteria from corresponding redline item(s)
- [ ] Deferred/known-polish items explicitly marked (not silently dropped)

### Completeness Check

- [ ] Coverage map accounts for all redline items
- [ ] No redline dropped without explicit justification
- [ ] Issue titles reference specific redline item numbers ([K-#])

---

## Overall Fixture Validation

### Minimum Passing Set

A fixture passes if:

- [ ] All 8 skill outputs are present in reports/
- [ ] Each output includes required fields listed above
- [ ] No critical contradictions between outputs
- [ ] Human-review questions in notes.md are answered

### Critical Validations

- [ ] Surface inventory and inspector outputs agree on surfaces found
- [ ] Lint V2 does not overclaim readiness vs reconcile findings
- [ ] Redline coverage accounted for in issue plan
- [ ] Agent routing failure is expected and documented

### Quality Thresholds

- [ ] ≥80% of checklist items completed = valid
- [ ] <80% = needs more work before integration testing
- [ ] Any missing required field = fixture incomplete

---

## Learnings This Rubric Validates

- **ui-surface-inventory:** app-shell surfaces need explicit type distinction from content
- **ui-inspector:** static reports must bound their confidence
- **ui-spec-linter:** spec pass ≠ implementation ready; explicit distinction required
- **ui-spec-reconcile:** target-only is a valid result; not all contradictions need full reconciliation
- **ui-docs-sync:** monorepo docs require nested file checks
- **ui-agent-routing:** report mode can fail; unresolved items are acceptable outputs
- **ui-redline:** partial redlines must document what is unverifiable
- **ui-to-issues:** every redline item must have a fate (covered, deferred, or justification)


## ui-surface-inventory
- [ ] Identifies app-shell/navigation-map scope.
- [ ] Identifies route registry as relevant evidence.
- [ ] Flags route contradiction risk.
- [ ] Accounts for nested or monorepo agent docs.
- [ ] Does not treat the surface as a simple standalone screen.
