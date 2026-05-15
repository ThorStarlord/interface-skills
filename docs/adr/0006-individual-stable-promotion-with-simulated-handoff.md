# ADR 0006: Individual Stable Promotion with Simulated Handoff

## Status
Accepted

## Context
The `interface-skills` repository needs a way to promote individual skills based on behavioral evidence without waiting for the entire downstream chain to become stable. Requiring every downstream neighbor to be stable before an upstream skill can be promoted would create a "promotion deadlock."

## Decision
A skill may be promoted to **stable** individually if it passes:
1. **Structural Validation** (Contract adherence).
2. **Behavioral Validation** (Judgment fidelity on happy-path and adversarial fixtures).
3. **Downstream Handoff Verification** (Real or Simulated).

When **Simulated Handoff** is used, the promotion scope must be explicitly limited to the skill’s own output contract. The promotion must not claim full-chain stability.

## Consequences
- Skills can be promoted incrementally and independently.
- **Stable** status means the skill’s own output contract is trustworthy, not necessarily that every downstream workflow is stable.
- Promotion artifacts must record whether handoff verification was real or simulated.
- Full-chain stability requires separate end-to-end evidence and a broader "Workflow" promotion.
