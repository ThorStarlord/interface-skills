# ADR 0003: Separate Structural Validation from Human Review

## Status
Accepted

## Context
Promotion of skills requires high confidence in output quality. However, "quality" is often conflated between "does this file have the right headers?" and "is this UI brief actually smart?".

## Decision
We split verification into two distinct gates:
1. **Validators**: Scripts or checklists that check **Deterministic Structure** (metadata, file existence, naming, schema compliance).
2. **Human Review**: The judgment step that checks **Intent and Usefulness** (subjective quality, tone, strategic fit).

## Consequences
- A skill cannot be promoted to Stable if its output is structurally invalid (fails Validator).
- A structurally valid output may still be rejected by a human if it is misleading or low-value.
- This prevents "Correctness-Theater" where agents produce perfectly formatted trash.
