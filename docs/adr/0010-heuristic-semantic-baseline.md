# ADR 0010: Heuristic Semantic Baseline for Certification

## Status

Accepted

## Context

The Skill Certification System (Phase 3) requires a way to verify behavioral evidence and handoff continuity without the cost, latency, and "judge-drift" of using a full LLM-as-a-Judge for every intermediate step. 

We need a deterministic, repeatable baseline that can be run in CI/CD environments to filter out obvious failures (hallucination, scope drift, parroting) before triggering Human Review.

## Decision

We will use a **Heuristic Semantic Baseline** as the primary mechanical proof for Behavioral Validation and Handoff Verification.

1. **Keyword/Phrase Density**: Behavioral derivation is proved through the propagation of unique domain terms (IDs, proper nouns, technical terms) from input to output.
2. **Fragment Matching**: Handoff continuity is proved through the detection of 4-6 word phrasal fragments from upstream artifacts in downstream outputs.
3. **Complexity Rubrics**: Quality is enforced through header/item density counts against skill-specific thresholds.
4. **Mechanical Proofs**: Hash-based **Zero-Manual-Repair** verification remains the hard floor for stability.

## Consequences

### Positive
- **Deterministic**: Results are repeatable and auditable.
- **Fast**: Can run in standard CI pipelines without API keys or LLM calls.
- **Convergent**: Forces skills to use Canonical Terminology from `CONTEXT.md`.

### Negative
- **Parroting Risk**: A sophisticated agent can "game" the density checks by echoing input terms without analysis.
- **Synonym Friction**: Skills that use valid synonyms instead of canonical terms will fail validation.
- **Heuristic False Positives**: A "pass" in the heuristic kernel is a *suggestion* of validity, not a guarantee.

## Compliance

1. **Human Review Gate**: All heuristic "passes" must still be signed off in `HUMAN-REVIEW.md` to verify actual Judgment Fidelity.
2. **Messy Fixtures**: Adversarial tests must trigger heuristic *failures* to be considered successful.
3. **Minimum Complexity**: Fixtures must exceed the "Minimum Behavioral Complexity" thresholds to prevent trivial passes.
