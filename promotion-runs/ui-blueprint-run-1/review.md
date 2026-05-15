# Promotion Review: ui-blueprint

## Summary
The downstream contract (`ui-system`) is stable. However, when evaluating the `ui-blueprint` fixture (`examples/promotion/ui-blueprint/blueprint.md`) against its own acceptance criteria, several critical gaps were identified. Since the fixture does not meet the skill's output format, the fixture fails validation.

## Fixture Evaluation

The fixture was evaluated against the following Acceptance Criteria from `SKILL.md`:

| Acceptance Criteria | Status | Notes |
| --- | --- | --- |
| Frontmatter links to a brief | ❌ Fail | Missing `based_on: brief-<slug>` in the frontmatter. |
| At least one named reference product appears | ❌ Fail | No "Visual direction" section with reference products exists. |
| Information density row uses dense/medium/sparse | ❌ Fail | No "Visual direction" table or properties exists. |
| Layout paradigm row uses named paradigms | ❌ Fail | No "Visual direction" table exists. |
| Every element in the hierarchy has a "why it ranks here" justification | ❌ Fail | Justifications are present, but not in the standard tabular format expected in the template. |
| Primary action appears in the top 3 hierarchy ranks | ✅ Pass | Save / Cancel actions are ranked 3. |
| ASCII or markdown table wireframe present for primary device | ✅ Pass | Text wireframe is provided for desktop. |
| Reading order is explicitly listed | ❌ Fail | Missing from the blueprint. |
| Every non-primary breakpoint has reflow behavior with specific verbs | ✅ Pass | Uses `collapse`, `swap` as expected. |
| No banned vague words appear | ✅ Pass | No vague words found. |
| "Open questions" or "assumptions" section is present | ❌ Fail | Has "Open layout questions resolved", but not unresolved questions or assumptions as required by the template. |

## Downstream Contract Evaluation
* **Downstream Skill:** `ui-system`
* **Status:** `stable`
* **Check Result:** ✅ Pass

## Recommendation
The skill itself is well-defined, and the downstream contract is stable. However, the existing fixture (`blueprint.md`) is severely out of sync with the output template and acceptance criteria specified in the `ui-blueprint` skill. The fixture lacks crucial sections like Visual Direction (reference products, density, layout paradigm) and Reading Order.

**Recommendation:** Do NOT promote at this time. Update the `examples/promotion/ui-blueprint/blueprint.md` fixture to match the expected output template, or revise the skill if the fixture is considered the source of truth. Since this evaluation required human judgment to compare the missing sections, and the fixture failed its own tests, this is flagged as `needs_human_review`.
