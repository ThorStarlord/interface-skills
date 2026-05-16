# ADR 0008: Skill Certification System Architecture
 
 ## Status: Accepted
Date: 2026-05-16
Deciders: Antigravity, User
Consulted: ThorStarlord
Informed: Registry Maintainers
 
 ## Context
 The `interface-skills` repository is evolving its promotion logic into a formal **Skill Certification System**. To ensure auditability and reduce authority ambiguity, the monolithic promotion scripts must be decomposed into a modular **Validator Ecosystem**.
 
 ## Decision
 We will implement a layered validation architecture where the **Promotion Harness** delegates to deterministic, in-process validators.
 
 ### 1. Validator Contract
 Validators will return structured Python result objects (e.g., `HumanReviewValidationResult`) rather than emitting standalone JSON artifacts. This prevents "authority ambiguity" between multiple result files.

### 2. Promotion Plan as Authority
The `promotion-plan.yaml` file is the **authoritative contract** for every promotion run. 
- It must pass **Structural and Semantic Validation** before execution.
- It must explicitly declare the **Blocking Failure Modes** relevant to the skill's domain.
- It defines the **Handoff Mode** required for the target status (e.g., Real Handoff for Workflow Stability).
- The validator MUST enforce **Canonical Defaults** from `CONTEXT.md` to prevent "authority watering down" where a plan defines too few failure modes or trivial complexity thresholds.
 
 ### 3. Extraction Roadmap
 To manage risk and preserve existing promotion behavior, we will extract validators in the following sequence:
 1. **human_review.py**: Validates governance authority and approval metadata.
 2. **promotion_plan.py**: Validates the semantic coherence of the promotion contract.
 3. **handoff_verification.py**: Validates existence and mode of handoff evidence.
 4. **fixture_integrity.py**: Performs structural pre-flight checks on evidence material.
 5. **behavioral_result.py**: Validates shape and classification of skill outputs.
 6. **reference_evidence.py**: Validates curated reference evidence for cleanliness and traceability.
 
 ### 4. Failure Taxonomy
 - **Fixture Defects** trigger a **Fixture Repair Brief**.
 - **Skill Behavior Defects** trigger a **Skill Improvement Brief**.
 - **Governance Defects** trigger a human review correction.
 
 ## Consequences
 - Clearer separation between structural pre-flight checks and behavioral judgment.
 - Improved auditability of the promotion lifecycle.
 - Modular validation logic that can be reused across different promotion harnesses.
 - Explicit human governance required for all "Stable" promotions.
