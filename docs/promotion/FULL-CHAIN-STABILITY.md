# Full-Chain Stability Standard

This document defines the **Full-Chain Stability** standard for the `interface-skills` repository. It establishes the criteria for certifying that a multi-step workflow is reliable, composable, and ready for production-grade use.

## Definition

**Full-Chain Stability** is a higher-order certification than individual skill stability. While a skill might be stable for its own input/output contract (ADR 0006), a **Workflow** is only certified once it has proven end-to-end integrity across all handoff boundaries.

### Core Principles

1.  **Zero-Manual-Repair**: The non-negotiable requirement that every artifact in the chain must be consumed by the next skill exactly as produced. Any manual fix, even a minor label correction, disqualifies the chain from stability.
2.  **Real Handoff**: Stability must be proven using *real* outputs from previous steps, not simulated or "gold standard" handoff artifacts.
3.  **Semantic Threading**: The "intent" of the user must be preserved from the first step (e.g., surface inventory) to the final artifact (e.g., implementation issues).

## Certification Process

The certification process is managed by the promotion harness and follows these steps:

1.  **Fixture Creation**: A dedicated full-chain fixture is created in `examples/fixtures/full-chain/<workflow-id>/`.
2.  **Execution**: The harness is run with the `--workflow` flag:
    ```bash
    python scripts/run-promotion-suite.py --workflow <workflow-id>
    ```
3.  **Continuity Audit**: The harness generates a `CONTINUITY-AUDIT.md` checklist. A human reviewer must audit the semantic integrity of the run.
4.  **Final Approval**: A `HUMAN-WORKFLOW-REVIEW.md` is signed, certifying the workflow as **Full-Chain Stable**.

## The Handoff Ladder

- **Simulated Handoff (ADR 0006)**: Used to promote individual skills by testing them against "ideal" inputs.
- **Real Handoff (ADR 0007)**: Used to promote workflows by testing the actual composition of skills.

## Negative Fixtures

To prevent "stability hallucinations," every stable workflow must be accompanied by **negative fixtures** that prove the harness correctly detects failures, such as:
- Missing artifacts.
- Boundary drift (e.g., a surface disappearing between steps).
- Structural invalidity.
