# Skill Promotion Review: ui-redline

## Execution Target
- Skill: `ui-redline`
- Type: Isolated Worker Task
- Promotion attempt: Rejected (enforced by rule 1: Do not promote the skill to stable).

## Summary
The `ui-redline` skill was tested using isolated static fixtures `profile-form.md` (spec) and `profile-form.tsx` (implementation code). Because the analysis used a code snippet rather than live rendered UI evidence, the recorded result must be treated as a **partial redline (static-code mode)**.

- **Input source:** Code snippet (`profile-form.tsx`).
- **Redline classification:** Partial redline (static-code mode).
- **Findings:**
  - **Finding 1 — `FormContainer` uses incorrect semantic element**
    - **Severity:** high
    - **Verification:** verified in static code
    - **Evidence:** `FormContainer` is implemented with a `<div>` instead of a `<form>`, which conflicts with the accessibility requirement for form semantics.
    - **Exact fix:** Replace the root `<div>` used by `FormContainer` with a `<form>` element and preserve the existing props/handlers on that element so submit and accessibility semantics are correctly exposed.
  - **Finding 2 — `TextInput` missing invalid state accessibility attribute**
    - **Severity:** medium
    - **Verification:** verified in static code
    - **Evidence:** `TextInput` does not set `aria-invalid={!!error}` when an error is present.
    - **Exact fix:** Add `aria-invalid={!!error}` to the input element rendered by `TextInput`.
  - **Finding 3 — `TextInput` missing disabled state styling**
    - **Severity:** medium
    - **Verification:** verified in static code
    - **Evidence:** `TextInput` does not include the required disabled-state classes `bg-gray-100 cursor-not-allowed`.
    - **Exact fix:** Update the `TextInput` class composition so the disabled branch includes `bg-gray-100 cursor-not-allowed` whenever the input is disabled.
  - **Finding 4 — `TextInput` missing required focus ring styling**
    - **Severity:** low
    - **Verification:** verified in static code
    - **Evidence:** `TextInput` does not include the required focus ring classes `ring-2 ring-action-primary`.
    - **Exact fix:** Add `ring-2 ring-action-primary` to the focus-visible or focus styling for the input element in `TextInput`.
  - **Finding 5 — `UploadButton` is not keyboard accessible**
    - **Severity:** high
    - **Verification:** verified in static code
    - **Evidence:** `UploadButton` uses a `<span>` with `onClick` and no keyboard interaction support, which does not satisfy the accessibility requirement that interactive controls be keyboard accessible.
    - **Exact fix:** Replace the clickable `<span>` in `UploadButton` with a semantic `<button type="button">`, or add equivalent keyboard handling and button semantics if replacement is not possible.
  - **Finding 6 — `UploadButton` uses non-tokenized color class**
    - **Severity:** low
    - **Verification:** verified in static code
    - **Evidence:** `UploadButton` uses the literal class `text-blue-500` instead of the design-token class `text-action-primary`.
    - **Exact fix:** Replace `text-blue-500` with `text-action-primary` in the `UploadButton` class list.

## Downstream Contract Verification
Downstream skill: `ui-spec-reconcile` (aliases to `is-ui-spec-reconcile`).
Status of `ui-spec-reconcile`: **draft**

Because the downstream skill is in `draft` status, the contract integration test MUST be classified as `needs_human_review`.

## Output Constraints Check
- Shared registries were **not** modified.
- All evidence strictly localized to `promotion-runs/ui-redline-run-1/`.
- Isolated fixture directory (`examples/promotion/ui-redline/`) and `SOURCE.md` were correctly created and utilized.
