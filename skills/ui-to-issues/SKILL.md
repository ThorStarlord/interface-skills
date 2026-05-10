---
name: ui-to-issues
description: Slice a UI spec package, redline audit, or acceptance checklist into independently implementable GitHub issues or markdown drafts. This skill ensures that UI work is broken down into vertical slices that deliver observable user outcomes.
status: draft
---

# UI to Issues

A skill for converting high-level UI specifications and audit findings into a set of discrete, actionable implementation tasks (issues). It prioritizes vertical slices of behavior over horizontal technical layers to ensure that every task results in a user-verifiable outcome.

## When to use this skill

Use this skill:
- When a new spec package is approved and ready for implementation.
- After a `ui-redline` audit to break down the required fixes into manageable tasks.
- To convert a `ui-spec-reconcile` report into a punch-list of remaining gaps.
- When you need to plan a sprint or milestone for a UI feature.

## Core principles

1. **Vertical Slices:** Prioritize issues that deliver one observable UI outcome end-to-end. Avoid "edit file X" or "add styles for Y" unless the change is truly isolated.
2. **User-Verifiable:** Every issue should have a "How to verify" section that describes what a user (or agent) will see or do to confirm the task is complete.
3. **Spec-Linked:** Every issue must link back to the specific part of the UI spec it implements or fixes.
4. **Actionable:** Issues must contain enough detail (props, tokens, microcopy) that an agent or developer can implement them without re-reading the entire spec package.

## Modes

This skill produces one of two outputs depending on context:

| Mode | When to use | Output |
|---|---|---|
| **Markdown** | Default. Safe and portable. | Markdown issue drafts. |
| **Tracker** | Only when explicitly requested and tracker is configured (e.g. `gh` CLI). | Creates issues in the tracker + produces a summary report. |

Default to **Markdown** mode unless the user explicitly says to create the issues in a tracker.

## Workflow

### Step 1 — Consume Inputs

Gather the source documents:
- **Primary:** `acceptance.md`, `redlines/redline-audit.md`, or `ui-spec-reconcile` report.
- **Context:** The full spec package (`brief.md`, `screen-spec.md`, etc.).

### Step 2 — Identify Slices

Analyze the requirements/findings and group them into vertical slices. A slice usually covers:
- A specific user journey step.
- A meaningful state transition.
- A coherent sub-surface or component (if it has its own verifiable behavior).

**Grouping Priority:**
1. **User behavior / Interaction** (e.g., "Implement Reel generation success state")
2. **State / Edge case** (e.g., "Add error handling for empty carousel")
3. **Component-level polish** (only if the component is complex enough to merit its own issue)

### Step 3 — Draft Issues

For each slice, produce an issue draft. Do not create the issues in a tracker yet unless explicitly requested.

**Each draft must include:**
- **Title:** Clear, outcome-oriented (e.g., "Add Reels support to /create carousel")
- **Scope:** Which files and components are likely involved.
- **Requirements:** Bulleted list of what must be built/fixed.
- **Acceptance Criteria:** Derived directly from `acceptance.md`.
- **References:** Links to the relevant spec files and redline items.

### Step 4 — Review and Refine

Review the set of issues with the user. Check for:
- **Dependencies:** Are the issues in a logical order?
- **Sizing:** Is any issue too large? (If it takes more than 1–2 agent turns, slice it thinner).
- **Completeness:** Is every item in the `acceptance.md` or redline report covered?

### Step 5 — Export

Output the final set of issues as a Markdown block. Do not create tracker issues unless the user explicitly asks and the tracker is configured.

## Output template

Include metadata about the export mode in the frontmatter:
```yaml
tracker_mode: markdown | github-cli | linear | local-files
```

Produce the issues as a single Markdown document:

```markdown
# UI Implementation Plan: <scope>

## Issue 1: <Outcome-oriented Title>
- **Labels:** `ui`, `frontend`, `<severity>`
- **Spec:** `<path-to-spec>#section`
- **Description:** <What and why>
- **Task List:**
  - [ ] Requirement 1
  - [ ] Requirement 2
- **Acceptance Criteria:**
  - [ ] <Criterion from acceptance.md>
- **Verification:** <How to verify visually or via test>

---

## Issue 2: ...
```

## Acceptance criteria for this skill's output

- [ ] Issues are vertical slices of behavior, not horizontal architectural layers.
- [ ] Every issue contains a specific verification step.
- [ ] All items from the input (acceptance checklist or redline) are mapped to an issue.
- [ ] No "vague" tasks (e.g., "clean up code", "make it look modern") are included.
- [ ] Issues include direct links to the relevant UI specifications.
