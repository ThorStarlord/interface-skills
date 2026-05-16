## Problem Statement

The `interface-skills` repository relies on monolithic promotion scripts (e.g., `run_promotion_suite.py`) that mix orchestration, structural validation, and human governance. This tight coupling makes the promotion process difficult to audit, test, and evolve without risking authority ambiguity or regression. We need a modular **Validator Ecosystem** that acts as a deterministic trust layer within the **Skill Certification System**.

## Solution

Extract a modular, staged **Validator Ecosystem** from the Promotion Harness. This system will enforce structural, configuration, and governance integrity through a sequence of deterministic validators that return structured results to the harness.

## User Stories

1. **As a maintainer**, I want validation responsibilities extracted from `run_promotion_suite.py` so that promotion behavior remains understandable and testable.
2. **As a maintainer**, I want validators to return structured results so the Promotion Harness does not parse stdout or ad-hoc Markdown.
3. **As a reviewer**, I want approval scope to be explicit so that restoration confirmation, individual stable promotion, and workflow full-chain stability cannot be confused.
4. **As a reviewer**, I want promotion evidence to clearly separate fixture defects from skill behavior defects.
5. **As an auditor**, I want to trace a stable promotion from promotion plan to fixture integrity, behavioral evidence, handoff verification, human approval, reference evidence, and regression results.
6. **As an auditor**, I want to verify that individual skill stability and workflow full-chain stability are never overclaimed.

## Implementation Decisions

### 1. Staged Extraction Roadmap
The Validator Ecosystem will be extracted in six discrete steps:
1.  **human_review.py (Governance)**: Validates explicit approval authority. Rejects pending/rejected reviews and restoration confirmations as stable promotion authority. Requires `stable_promotion_authorized` for stable promotion.
2.  **promotion_plan.py (Configuration)**: Validates `promotion-plan.yaml` as the configuration authority. Checks structure and semantic coherence before evidence generation.
3.  **handoff_verification.py (Contract Continuity)**: Validates required handoff evidence against the configured mode. Prevents simulated handoff from claiming Full-Chain Stable status.
4.  **fixture_integrity.py (Input Integrity)**: Pre-flight validation for fixtures. Separates input defects (Fixture Repair Brief) from behavioral failures (Skill Improvement Brief).
5.  **behavioral_result.py (Behavioral Shape)**: Validates result shape, completeness, and traceability. Distinguishes behavioral evidence from human review.
6.  **reference_evidence.py (Curation Integrity)**: Validates curated reference evidence for cleanliness and traceability. Rejects automatic "latest pass" selection rules.

### 2. JSON-Second Result Contract
Validators will first expose a structured in-process Python result object. The Promotion Harness will consume these objects directly. No per-validator `validation-result.json` artifacts will be introduced in this phase. The contract will include:
- `status` (pass/fail/error)
- `findings` (list of findings)
- `failure_modes` (detected defects)
- `artifact_path` (related artifact)
- `validator_name`
- `checked_scope` (scope of validation)

### 3. Architectural Boundaries
- **No Registry Changes**: `skills.json` and other registries remain unchanged.
- **No Automatic Promotion**: Validators do not perform promotions; they provide evidence for the harness.
- **Path Hygiene**: Preserves repo-relative paths; avoids `file:///` links.
- **Compatibility**: Maintains support for `python scripts/run_promotion_suite.py`.

## Testing Decisions

- **Structural Testing**: Validators will be tested against positive and negative fixture sets to ensure contract enforcement.
- **In-Process Integration**: Test the Promotion Harness's ability to aggregate results from multiple extracted validators.

## Out of Scope

- Automated behavioral judgment (judgment remains a human task).
- Introduction of `PROMOTION-REGISTRY.yaml`.
- Certification of new workflows.
- Workflow-level continuity auditing.

## Further Notes

This PRD formalizes the **Skill Certification System** architecture and replaces the "Promotion OS" metaphor. It establishes the foundations for auditable, stable skill promotion.
