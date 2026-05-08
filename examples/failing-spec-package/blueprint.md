---
spec_type: blueprint
spec_id: failing-package
created: 2026-05-08
status: approved
---

# Blueprint: Post Composer Widget

## 1. Information Hierarchy

1. Post input
2. Submit button
3. Image attachment

## 2. Layout

The widget uses a clean layout with a modern feel. The compose area is on the left, with the preview on the right.

<!-- DEFECT FD-03: "clean layout" is vague language. Should be replaced with specific measurements and structure. ui-spec-linter should flag this as a Warning. -->
<!-- DEFECT FD-04: "modern feel" is vague language. Should be replaced with concrete visual direction referencing visual-calibration.md. ui-spec-linter should flag this as a Warning. -->

```
┌─────────────────────────────────────┐
│  [Compose area]      [Preview area] │
│  (textarea)          (post card)    │
│                                     │
│  [Attach image]   [Submit →]        │
└─────────────────────────────────────┘
```

## 3. Responsive Behaviour

On mobile, the layout stacks vertically. Preview appears below compose area.

## 4. Spacing

Uses standard spacing throughout.

<!-- Note: No specific spacing tokens referenced because system.md does not define space.* — another defect in this fixture. -->
