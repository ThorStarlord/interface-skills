# Skill Certification System

The **Skill Certification System** is the formal architecture for promoting AI skills from `draft` to `stable`. It serves as the **Trust Layer** of the repository, ensuring that every skill meets deterministic structural requirements, behavioral quality standards, and human-approved governance before it is authorized for production use.

## 1. Overview

The system is designed to prevent "Skill Drift"—where a skill passes automated tests but produces misleading, trivial, or unconsumable artifacts. It separates the **execution** of tests from the **judgment** of results.

| Layer | Responsibility | Component |
| :--- | :--- | :--- |
| **Orchestration** | Running skills against fixtures | **Promotion Harness** |
| **Trust** | Evaluating results against contracts | **Validator Ecosystem** |
| **Authority** | Final human sign-off and promotion | **Governance Gate** |

## 2. Component Architecture

### The Promotion Harness (`scripts/run_promotion_suite.py`)
The harness is the execution engine. It parses the `promotion-plan.yaml`, identifies the necessary fixtures, orchestrates skill invocations, and collects evidence into the `promotion-runs/` directory.

### The Validator Ecosystem (`scripts/validators/`)
The ecosystem is a modular collection of "Judges" that evaluate different aspects of a promotion run. Every validator returns a standardized `ValidatorResult`.

| Validator | Phase | Responsibility |
| :--- | :--- | :--- |
| **Configuration Authority** | Pre-flight | Ensures the skill exists in the registry and fixtures are correctly mapped. |
| **Input Integrity** | Pre-flight | Validates that the test fixture is well-formed (e.g., contains a `rubric.md`). |
| **Behavioral Result** | Post-execution | Checks for trivial placeholders (TBD/TODO) and enforces complexity thresholds. |
| **Contract Enforcement** | Post-execution | Verifies that downstream skills can correctly consume the output (Handoff check). |
| **Governance Validation** | Audit | Verifies that a `HUMAN-REVIEW.md` exists with explicit approval and correct scope. |
| **Reference Snapshot** | Audit | Ensures the curated "Gold Standard" evidence in `examples/promotion/` is complete. |

## 3. The Trust Model

Certification is achieved through a multi-stage validation pipeline:

1.  **Fixture Integrity**: "Is this a legitimate test object?"
2.  **Behavioral Evidence**: "Did the skill produce useful, non-trivial, and sufficiently complex output?"
3.  **Handoff Verification**: "Does the output satisfy the contract required by the next skill in the chain?"
4.  **Human Review**: "Does a human expert agree the result is useful and not misleading?"
5.  **Reference Curation**: "Is the successful evidence preserved as a gold-standard snapshot?"

## 4. Evidence Management

The system maintains a strict boundary between historical records and curated standards.

### Promotion Runs (`promotion-runs/`)
Ephemeral directories containing the full context of a single validation run.
- `result.json`: The machine-readable summary of all validator findings.
- `review.md`: The initial automated review and checklist for humans.
- `output/`: The actual artifacts produced by the skill during the run.

### Promotion Reference Evidence (`examples/promotion/<skill>/reference/`)
Curated snapshots of **successful, human-approved runs**. This is the "Gold Standard" used to validate future versions of the skill and to onboard new agents. It is only updated after a formal stable promotion.

## 5. Implementation Roadmap

### Phase 1: Individual Skill Certification (Complete)
- [x] Extraction of modular Validator Ecosystem.
- [x] Standardized Result Contract (`ValidatorResult`).
- [x] Pre-flight Integrity and Behavioral Shape enforcement.
- [x] Governance integration for human approval gates.

### Phase 2: Workflow Stability & Full-Chain Validation (Active)
- [ ] Implementation of the **Workflow-Link Validator**.
- [ ] Formalizing "Full-Chain Stability" where multiple stable skills must pass a combined handoff test.
- [ ] Automated regression detection across the `workflow-registry.yaml`.

### Phase 3: Automated Evidence Lifecycle (Future)
- [ ] Automated syncing of `promotion-runs/` to `reference/` upon approval.
- [ ] "Dirty Reference" detection (detecting loose artifacts in curated snapshots).
- [ ] Continuous Certification: Running the suite against main on every PR.

## 6. Relationships

- **ADR 0006**: Defines the requirement for Individual Stable Promotion.
- **ADR 0007**: Defines the requirement for Workflow Promotion and Handoff Stability.
- **CONTEXT.md**: Defines the canonical vocabulary used by the validators.
