# Skill Certification System

The **Skill Certification System** is the formal architecture for making skill and workflow stability precise, auditable, and repeatable. Its **Validator Ecosystem** serves as the modular trust layer of the repository, ensuring that every skill meets deterministic structural requirements, behavioral evidence requirements, handoff readiness checks, and human-approved governance.

## 1. Purpose

The system is designed to prevent "Skill Drift"—where a skill passes automated tests but produces misleading, trivial, or unconsumable artifacts. It separates the **execution** of tests from the **judgment** of results, providing a clear path from a `draft` candidate to a `stable` authorized skill.

## 2. Trust Model

Certification is achieved through a multi-stage validation pipeline that prioritizes deterministic evidence before human authorization.

| Stage | Goal | Deterministic Validator |
| :--- | :--- | :--- |
| **1. Fixture Integrity** | "Is this a legitimate test object?" | `fixture_integrity.py` |
| **2. Behavioral Evidence** | "Did the skill produce useful, non-trivial, and sufficiently complex output?" | `behavioral_result.py` |
| **3. Handoff Verification** | "Does the output satisfy the contract required by the next skill?" | `handoff_verification.py` |
| **4. Governance Approval** | "Does a human expert authorize the promotion?" | `human_review.py` |
| **5. Reference Curation** | "Is the successful evidence preserved as a gold-standard snapshot?" | `reference_evidence.py` |

## 3. Architecture: Harness, Validators, Governance

The system maintains a strict separation of roles to prevent logic creep and preserve auditability.

| Role | Component | Responsibility |
| :--- | :--- | :--- |
| **Executor / Orchestrator** | **Promotion Harness** | Executes skills against fixtures and collects evidence. |
| **Deterministic Judges** | **Validator Ecosystem** | Evaluates results against hard contracts and schemas. |
| **Authority / Approval** | **Human Review Governance** | Final judgment on usefulness and domain adequacy. |

## 4. Validator Ecosystem

The ecosystem is a modular collection of deterministic validators located in `scripts/validators/`. Every validator returns a standardized `ValidatorResult`.

*   **Configuration Authority** (`promotion_plan.py`): Ensures the skill exists in the registry and fixtures are correctly mapped.
*   **Input Integrity** (`fixture_integrity.py`): Validates that the test fixture is well-formed (e.g., contains a `rubric.md`).
*   **Behavioral Result** (`behavioral_result.py`): Checks for trivial placeholders and enforces complexity thresholds.
*   **Contract Enforcement** (`handoff_verification.py`): Verifies that downstream skills can correctly consume the output.
*   **Governance Validation** (`human_review.py`): Verifies that a `HUMAN-REVIEW.md` exists with explicit approval.
*   **Reference Snapshot** (`reference_evidence.py`): Ensures the curated "Gold Standard" evidence is complete and traceable.

## 5. Evidence Lifecycle

The system distinguishes between chronological run logs and curated reference standards.

### Promotion Runs (`promotion-runs/`)
**Historical run directories** containing the full context of a single promotion or validation run. They preserve chronology and debugging context.
- `result.json`: The machine-readable summary of all validator findings.
- `review.md`: The initial automated review and checklist for humans.
- `output/`: The actual artifacts produced by the skill during the run.

### Promotion Reference Evidence (`examples/promotion/<skill>/reference/`)
**Curated snapshots** of human-approved, successful evidence. This is the "Gold Standard" used to onboard agents and validate future iterations.
*   Reference evidence is only updated after an explicit, human-approved stable promotion.
*   The system must never select reference evidence solely because it is the latest passing run.

## 6. Stability Levels

| Level | Meaning | Criteria |
| :--- | :--- | :--- |
| **Draft** | Experimental | In development, output format may change, no stable evidence. |
| **Stable** | Production-ready | 3+ human-approved runs, failure modes tested, handoff verified. |
| **Verified** | Full-Chain Stable | All workflow steps are individually stable and pass a continuous handoff audit. |

## 7. Failure Ownership

To ensure rapid remediation, every validation failure has a clear owner.

| Failure Type | Root Cause | Remediation |
| :--- | :--- | :--- |
| **Plan/Config** | Missing registry entry or mismapped fixture | `promotion_plan.py` repair |
| **Fixture Integrity** | Fixture is missing required files or rubrics | Fixture repair brief |
| **Behavioral Weakness** | Skill output is trivial, missing, or malformed | Skill improvement brief |
| **Handoff Broken** | Downstream skill cannot parse or find output | Handoff/contract repair |
| **Governance Gap** | `HUMAN-REVIEW.md` is missing or unauthorized | Governance correction |
| **Dirty Reference** | Reference snapshot is incomplete or contains junk | Reference curation repair |

## 8. Roadmap

### Phase 1: Validator Ecosystem Extraction
**Status: Complete as of 2026-05-16, pending audit confirmation.**
- [x] Extraction of modular Validator Ecosystem from the harness.
- [x] Standardized `ValidatorResult` contract.
- [x] Integration of Governance gates and Behavioral shape enforcement.

### Phase 2: Workflow Stability Generalization (Active)
**Status: Following established ADR 0007 / spec-recovery precedents.**
- [ ] Extend full-chain validation beyond the certified `spec-recovery` workflow.
- [ ] Implement reusable workflow-level validators for zero-manual-repair handoffs.
- [ ] Expand regression coverage across `workflow-registry.yaml`.

### Phase 3: Automated Evidence Lifecycle (Future)
- [ ] Traceable reference evidence sync after explicit human-approved stable promotion.
- [ ] "Dirty Reference" detection for curated snapshots.
- [ ] Continuous Certification: Automated runs on repository pull requests.

## 9. Related ADRs and Documents

- **ADR 0006**: Individual Stable Promotion with Simulated Handoff.
- **ADR 0007**: Workflow Promotion / Full-Chain Stability.
- **CONTEXT.md**: Canonical vocabulary for the Skill Certification System.
