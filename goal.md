# Goal: Repository Promotion and Certification Stability

This document defines the core mission, structural pillars, and strict definitions of stability for the `interface-skills` repository under the **Skill Certification System**.

---

## 1. Core Mission Statement

The ultimate goal of this repository is to achieve **complete autonomous execution safety and reliability** across all UI specification, generation, and inspection capabilities. 

To accomplish this, we mandate:
1. **100% Skill Promotion**: Every internal skill in the repository must be promoted from `draft` to **stable** status.
2. **100% Full-Chain Workflow Certification**: Every multi-skill execution sequence (Workflow) in the repository must be certified as **full-chain stable** with **zero manual repair** required between steps.

---

## 2. The Three Trust Pillars

To prevent "authority watering down" or "hallucinated stability" when agents promote skills, the **Skill Certification System** relies on three architectural pillars:

### Pillar 1: The Validator Ecosystem
We enforce a layered validation architecture where the promotion harness delegates to deterministic, in-process validators:
- **Governance & Approval Gate**: [human_review.py](file:///h:/GithubRepositories/interface-skills/scripts/validators/human_review.py) validates signed, human-reviewed [HUMAN-REVIEW.md](file:///h:/GithubRepositories/interface-skills/docs/agents/HUMAN-REVIEW.md) artifacts.
- **Contract & Plan Validation**: [promotion_plan.py](file:///h:/GithubRepositories/interface-skills/scripts/validators/promotion_plan.py) enforces canonical defaults, minimum behavioral complexity, and explicit blocking failure modes from [CONTEXT.md](file:///h:/GithubRepositories/interface-skills/CONTEXT.md).
- **Handoff Verification**: [handoff_verification.py](file:///h:/GithubRepositories/interface-skills/scripts/validators/handoff_verification.py) verifies existence, type, and coherence of upstream-to-downstream inputs and outputs.
- **Structure & Shape**: [fixture_integrity.py](file:///h:/GithubRepositories/interface-skills/scripts/validators/fixture_integrity.py) and [behavioral_result.py](file:///h:/GithubRepositories/interface-skills/scripts/validators/behavioral_result.py) verify the mechanical shape and density of output reports against skill-specific rubrics.

### Pillar 2: The Promotion Plan Contract
Every promotion run is governed by an authoritative contract file: `promotion-plan.yaml`. 
- A plan must pass semantic validation before it can be run.
- It must explicitly list all domain-specific failure modes.
- It defines the complexity thresholds required for the target status level.

### Pillar 3: The Drift Lock & Reference System
Once a skill is certified as **stable**:
- Its certified reference evidence (inputs, outputs, and hashes) is synchronized into a "Gold Standard" reference in `references/reference_record.json`.
- A strict **Drift Lock** ([enforce_promotion_lock.py](file:///h:/GithubRepositories/interface-skills/scripts/enforce_promotion_lock.py)) blocks pull requests and registry changes if the skill's instruction files drift from the certified gold-standard state without a new, approved promotion plan.

---

## 3. Strict Definitions of Stability

### Individual Skill "Stable" Status
A skill is promoted to **stable** if and only if:
1. It has an approved, structural `promotion-plan.yaml` containing valid complexity thresholds.
2. Its latest execution run passes all deterministic **Structural Pre-flight Checks** with zero errors or critical warnings.
3. It passes the **Heuristic Semantic Baseline** (keyword propagation density, phrasal fragment matching, and complexity rubrics) defined in [ADR 0010](file:///h:/GithubRepositories/interface-skills/docs/adr/0010-heuristic-semantic-baseline.md).
4. A human has explicitly verified its **Judgment Fidelity** and signed off on the run in a [HUMAN-REVIEW.md](file:///h:/GithubRepositories/interface-skills/docs/agents/HUMAN-REVIEW.md) file.

### Workflow "Full-Chain Stable" Status
A workflow is certified as **full-chain stable** if and only if:
1. Every individual skill within the workflow is already promoted to **stable**.
2. It has documented, real-world evidence from a **Real Handoff** run across the entire skill chain.
3. It passes **Zero-Manual-Repair** verification (meaning every downstream skill consumed the upstream output without any human or automated modification).
4. The workflow has been audited to confirm that the final outputs preserve the original intent and context from the starting brief (Continuity Audit).
5. It is registered with a `source_run_id` pointing to an approved workflow run and recorded in `workflow_reference_record.json`.
