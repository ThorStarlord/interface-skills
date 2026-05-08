---
spec_type: acceptance
spec_id: failing-package
created: 2026-05-08
status: approved
---

# Acceptance Criteria: Post Composer Widget

Severity: **[B]** Blocker | **[M]** Major | **[m]** Minor
Type: A = Automated | M = Manual

## Layout

| ID | Criteria | Sev | Type |
|---|---|---|---|
| L-01 | The widget renders in two columns on desktop (compose left, preview right). | M | M |
| L-02 | On mobile (< 768px) the layout stacks vertically. | M | M |

## Post submission

| ID | Criteria | Sev | Type |
|---|---|---|---|
| AC-01 | The submit button has a minimum click target size of 44×44px. | m | A |

<!-- DEFECT FD-08: AC-01 (click target size) is not traceable to brief §6 success criteria.
     Brief §6 states: (1) submit in under 45 seconds, (2) button shows loading state.
     Click target size is not mentioned. ui-spec-linter should flag this as a Warning
     because untraceable criteria may indicate scope creep or a missed brief update. -->

<!-- DEFECT FD-09: No criterion covers the error state from brief §7 ("Must work on mobile and desktop").
     More critically, brief §6 explicitly requires a loading state on submit but no
     acceptance criterion verifies the loading state. ui-spec-linter should catch this
     as a Blocker because a stated success criterion has no corresponding test. -->

## Image attachment

| ID | Criteria | Sev | Type |
|---|---|---|---|
| IMG-01 | Clicking "Attach image" opens a file picker. | M | M |
| IMG-02 | After selecting an image, a thumbnail preview appears. | M | M |
