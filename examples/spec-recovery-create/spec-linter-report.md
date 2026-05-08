---
spec_type: lint-report
spec_id: pulse-create
created: 2026-05-08
status: draft
---

# Spec Linter Report: Pulse /create Route

**Result: FAIL**

3 blockers and 4 warnings. This package cannot be marked `complete` until the blockers are resolved.

---

## Summary

| Level | Count |
|---|---|
| Blocker | 3 |
| Warning | 4 |
| Info | 2 |

---

## Blockers

### B-01 — Open questions block acceptance criteria approval

**File:** `acceptance.md`  
**Section:** AI Draft (A-04), Channel Selector (CH-02), Media Upload (MU-03)

Three acceptance criteria contain `⚠️ TBD` placeholders because the underlying product decisions are unresolved:

- `A-04` depends on the agreed AI timeout threshold (open question #1 in `brief.md §9`).
- `CH-02` depends on confirmed channel ordering logic (open question #2).
- `MU-03` depends on the engineering-confirmed file size limit.

Until these are closed, `acceptance.md` cannot be promoted from `draft` to `approved`.

**Fix:** Resolve all three open questions in `brief.md §9`. Rewrite the three criteria to replace `⚠️ TBD` with the agreed values.

---

### B-02 — `screen-spec.md` mobile layout not approved

**File:** `screen-spec.md`  
**Section:** §8 Open Items #3

The unified responsive mobile layout described in `blueprint.md §3` and `screen-spec.md §2 regions` depends on removing `MobileCreateRedirect` — an architecture change requiring engineering sign-off (open question #3 in `brief.md §9`). This has not been obtained.

`screen-spec.md` is correctly marked `draft`. It cannot be promoted until open question #3 is resolved.

**Fix:** Obtain engineering sign-off on the mobile layout change. Update `brief.md §9 #3` to closed. Promote `screen-spec.md` to `approved`.

---

### B-03 — Package status is `draft` — three required files are not yet approved

**Computed package status:** `draft` (lowest maturity across required files)

| File | Status |
|---|---|
| `brief.md` | approved ✓ |
| `visual-calibration.md` | approved ✓ |
| `blueprint.md` | approved ✓ |
| `screen-spec.md` | draft ✗ |
| `microcopy.md` | draft ✗ |
| `acceptance.md` | draft ✗ |

Until `screen-spec.md`, `microcopy.md`, and `acceptance.md` all reach `approved`, the package status remains `draft` and delivery cannot begin.

---

## Warnings

### W-01 — Vague language in `visual-calibration.md` §Visual tone

**File:** `visual-calibration.md`  
**Location:** Final paragraph ("Visual tone reference")

The phrase "Linear's density" and "Notion's surface simplicity" are product-relative references that are meaningful to this team but not to a new contributor or an AI agent. When the visual calibration is used to drive component decisions, these references will not resolve to measurable values.

**Fix (optional but recommended):** Add a brief translation: "By 'Linear-dense' we mean: row height ≤ 40px, max 3 levels of visual hierarchy per view." This is a style suggestion — it does not block promotion.

---

### W-02 — `microcopy.md` error copy for media upload contains a placeholder

**File:** `microcopy.md`  
**Section:** §4 "Media upload file too large"

Target copy reads: "This file exceeds [N] MB." This placeholder must be resolved before implementation.

**Fix:** Link this to the resolution of the file size limit question. Update the copy when engineering confirms the limit.

---

### W-03 — `screen-spec.md` component map references a caption consolidation that is not tracked

**File:** `screen-spec.md`  
**Section:** §6 Component Map

"Refactor: `CaptionInput` (consolidate 3 implementations into 1)" is stated as a target but there is no acceptance criterion in `acceptance.md` that verifies the consolidation was done. The inspector report (`redlines/inspector-report.md`) identifies this as a critical code-quality issue; it should be traceable to acceptance.

**Fix:** Add an acceptance criterion verifying that there is exactly one `CaptionInput` component in the codebase after the refactor (e.g., "No more than one component named `CaptionInput` or `CaptionTextarea` exists in `src/`").

---

### W-04 — `00-index.md` lists `spec-linter-report.md` as `draft` but the linter report cannot be approved until the package is approved

**File:** `00-index.md`  
**Section:** File inventory row #9

This is a meta-issue: the linter report reflects the state of the package at time of running. Once all blockers are resolved, this document should be re-run and the result should be a PASS. The `00-index.md` entry for this file should remain `draft` until a clean PASS is recorded.

**Fix:** Re-run `ui-spec-linter` after all blockers are closed. If the result is PASS, update this file and the `00-index.md` entry.

---

## Informational

### I-01 — Recovery package (`recovery: true`)

This package was produced via the retrospective specification recovery workflow. Some divergences between Observed and Target descriptions are expected and correct. The `recovery: true` flag in frontmatter suppresses false-positive warnings about missing spec artifacts (e.g., `system.md` and `flow.md` are absent — intentional for this recovery scope).

### I-02 — `component-specs/` not yet populated

No component specs exist under `component-specs/`. The `ChannelPicker` and `ScheduleModal` components are identified in `screen-spec.md §6` as candidates for formal component specs. These are not required for recovery package approval but are recommended before implementation begins.
