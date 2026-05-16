# Interface Skills Context

## Purpose

Interface Skills is a toolkit for turning fuzzy, existing, or drifting UI work into explicit, testable interface specifications.

## Philosophy

Interface failures are usually process failures, not people failures.

When an AI-built UI misses the mark, improve the contract:
- clearer intent
- named visual language
- explicit states
- evidence-based inspection
- testable acceptance
- routed documentation agents can find

## Core vocabulary

### Skill Certification System
The long-term system for making skill and workflow stability precise, auditable, and repeatable.

### Validator Ecosystem
The modular trust layer inside the Skill Certification System. Validators produce structured findings about structural validation, behavioral evidence, human review, handoff verification, reference evidence, and workflow continuity.

### Spec Package
The most fundamental unit of work. A folder containing the artifacts for one UI scope.
_Avoid_: "random docs," "output folder," "spec dump," "docs bundle."

### Skill
A reusable instruction package that performs one step, such as `ui-brief` or `ui-redline`. Skills are producers and maintainers of spec package artifacts.
_Avoid_: "just a prompt," "one-off agent task."

### Workflow
An ordered sequence of Skill Steps for a common situation (e.g., Spec Recovery).
_Avoid_: "Skill Chain" as formal terminology.

### Skill Step
One skill invocation inside a Workflow.
_Avoid_: "mini skill," "sub-agent," "chain link."

### UI Scope
The surface being specified or inspected (e.g., `/kanban` route or `Sidebar` component).
_Avoid_: "page," "screen," "module," "UI part."

### Artifact
A single tracked output produced or updated by a skill inside a spec package (e.g., `02-brief.md`).
_Avoid_: "random output," "loose document," "untracked file."

### Report
An artifact that audits, compares, reconciles, or routes work (e.g., `SPEC-LINT-REPORT.md`). Reports are classified as **Active**, **Historical**, or **Superseded** in the Run Manifest to prevent agents from acting on stale data.

### Run Manifest
A convention within `00-index.md` (or a standalone `RUN-MANIFEST.md`) that tracks the lifecycle of reports and the sequence of skill executions. It is the primary defense against "stale report" bugs.

### Redline
A report that compares implementation evidence against a target spec and identifies mismatches, severity, verification status, and recommended fixes.
_Avoid_: "bug list," "design critique," "QA notes."

### Run History
A record of which skills ran, what inputs they used, what artifacts they produced, and which reports supersede earlier reports.
_Avoid_: "chat history," "misc notes."

### Run Manifest
The concrete artifact/file that records Run History for a Spec Package.

### Fixture
A frozen example case used to validate draft skills.
_Avoid_: "live product docs," "current source of truth."

### Validator
A deterministic script or checklist that checks structure and metadata.
_Avoid_: "reviewer," "judge," "quality oracle."

### Human Review
The judgment step that decides whether a structurally valid output is actually useful and not misleading.

### Canonical Package Format
The current expected structure/template for a Spec Package.
_Avoid_: "canonical spec package" unless referring to a Spec Package that conforms to this format.

### Agent Routing
The process of wiring spec packages into agent discovery files (e.g., `CLAUDE.md`).

### Promotion
The process of moving a skill or workflow from draft to stable after enough fixture evidence confirms the output format is locked and behavioral judgment is verified.

### Individual Skill Promotion
The process defined in ADR 0006 where a skill is promoted based on its own output contract and simulated handoff.

### Workflow Promotion
The process defined in ADR 0007 where an entire sequence of skills is promoted based on real handoff evidence and zero-manual-repair criteria.

### Structural Validation
The automated verification of **Contract Adherence**. Confirms that required files exist, metadata is valid, schemas pass, paths are repo-relative, and the output has the expected shape.

### Behavioral Evidence
Proof that a skill can apply its intended **Judgment Fidelity** to realistic, non-trivial inputs and produce outputs that are useful, bounded, and handoff-ready. This is the qualitative gate for Promotion.

### Judgment Fidelity
The ability of a skill to correctly apply domain heuristics and interpret messy or incomplete input without hallucinating or violating project boundaries.

### Handoff Utility
A dimension of Behavioral Evidence confirming that an artifact contains enough discrete, actionable detail for a downstream human or skill to perform the next step without re-reading source evidence.

### Promotion Harness
The orchestration layer that runs promotion checks, collects evidence, and delegates validation logic to validators. Current entrypoints include `scripts/run_promotion_suite.py` and `scripts/run-promotion-suite.py`.

### Promotion Evidence
The generated artifacts used to support a promotion decision, including behavioral result records, narrative reviews, invocation records, human review artifacts, reference evidence, workflow manifests, continuity audits, and regression outputs.

### Human Review Governance Validation
Deterministic validation that a required human review artifact exists and contains complete, explicit, scope-compatible approval metadata. It verifies that the Human Review gate was completed and authorized for the requested promotion scope, but does not judge behavioral evidence itself.

### Handoff Verification Validation
Deterministic validation that required handoff evidence exists, is complete, and matches the configured handoff mode. Simulated handoff may support individual skill promotion but must not claim workflow full-chain stability. Real handoff and zero-manual-repair evidence are required for workflow-level stability.

### Promotion Plan Validation
Deterministic validation that the promotion plan is structurally valid, semantically coherent, and executable before evidence generation begins. It verifies that configured skills, fixtures, behavioral criteria, failure modes, and handoff requirements form a valid promotion contract. It does not itself approve promotion or judge behavioral evidence.

### Fixture Integrity Validation
Deterministic pre-flight validation that a fixture is complete, coherent, non-trivial, correctly classified, and compatible with the promotion plan before it is used to generate behavioral evidence. It separates fixture defects from skill behavior defects and should produce fixture repair guidance when evidence material is invalid.

### Reference Evidence Validation
Deterministic validation that curated Promotion Reference Evidence is authorized, traceable to an approved promotion run, complete for the skill contract, and free of loose or unrelated artifacts. It validates reference evidence curation but does not itself approve promotion.

## Relationships

- A **UI Scope** is the target for one **Spec Package**.
- A **Workflow** is an ordered sequence of **Skill Steps**.
- A **Skill** produces or updates **Artifacts** within a **Spec Package**.
- A **Report** audits, compares, reconciles, or routes a **Spec Package**.
- A **Redline** compares implementation against the **Spec Package**.
- A **Fixture** freezes a real **Spec Package** so draft skills can be validated.
- A **Validator** performs **Structural Validation**.
- **Human Review** evaluates **Behavioral Evidence** to confirm **Judgment Fidelity** and **Handoff Utility**.
- **Promotion** moves a **Skill** from draft to stable only after required structural validation, behavioral evidence, handoff verification, and explicit human review are complete.
- The **Skill Certification System** uses the **Promotion Harness** to execute the **Validator Ecosystem**.
- A **Promotion Harness** run produces **Promotion Evidence**.
- **Promotion Plan Validation** validates the configured promotion contract before the **Promotion Harness** generates or evaluates evidence.
- **Fixture Integrity Validation** must pass before a fixture can be treated as valid Behavioral Evidence.
- **Promotion Reference Evidence** is curated from approved historical **Promotion Evidence** only after explicit human-approved stable promotion.

## Repository roles

- **Product repositories** contain live product specs, such as `ViralFactory/docs/saas-frontend/specs/kanban/`.
- The **`interface-skills` repository** contains skills, templates, shared references, validators, and frozen fixtures.
- A fixture copied into `interface-skills/examples/` is not the live product source of truth; it is a test case for the skill system.

## Source of truth hierarchy

1. Skill definitions in `skills/*/SKILL.md`
2. Shared references in `shared/references/`
3. Canonical package format and templates
4. Validated examples and fixtures
5. README and skill reference docs

## Skill status levels

The status of a skill reflects its validation depth and composability.

| Status | Meaning | Required Evidence |
|---|---|---|
| **draft** | Behavior defined, initial shape valid. | None (experimental). |
| **restoration baseline** | Environment-stable. | **Structural Validation** passes. |
| **beta / candidate** | Behaviorally promising but unproven in chains. | Happy path runs + **Human Review** + known caveats. |
| **stable** | Reliable for autonomous composition. | **Stable Promotion Evidence** (Happy path + adversarial + handoff). |
| **full-chain stable** | Verified end-to-end workflow reliability. | **Workflow Promotion Evidence** (Real handoff + zero-manual-repair). |

### Workflow Certification Policy (ADR 0009)

Every workflow marked as `stable` in `workflow-registry.yaml` must have an authoritative certification record.

| Status | Enforcement | Required Evidence |
|---|---|---|
| **draft** | Warn only. | None. |
| **beta** | Warn only. | 1+ successful run. |
| **stable** | **FAIL (BLOCKING)** | **Workflow Promotion Evidence** (Real handoff + zero-manual-repair) + `workflow_reference_record.json`. |
| **test** | Exempt. | None. |

### Stable Promotion Evidence

The qualitative evidence required to move a skill to **stable**. It must prove the skill is safe to compose with other skills without human "repair" turns. It requires:
1. **Happy Path:** 3+ consecutive successes on standard fixtures.
2. **Adversarial Fixture:** 1+ run against messy, conflicting, or incomplete input without hallucination.
3. **Downstream Handoff Verification:** Proof that a downstream skill can consume the output without clarification or label repair.
4. **Human Review:** Signed approval of the judgment fidelity.

## Process rule

Scripts enforce structure.
Skills provide judgment.
Humans approve whether the result is useful and not misleading.

## Example dialogue

> **User:** "I ran the retrospective workflow on `/kanban`. Should I keep generating more outputs?"
>
> **Maintainer:** "No. First freeze the `/kanban` output as a **Fixture**. The live product docs remain in the product repo; the copied fixture in `interface-skills/examples/` becomes a test case for draft skills."
>
> **User:** "The validator failed on my **Artifact** even though the content is good."
>
> **Maintainer:** "The **Validator** checks for deterministic structure (like metadata). If the structure is correct, use **Human Review** to decide if the content is actually helpful."

## Flagged ambiguities

- **Skill vs. Spec Package**: While Skills are the visible tools, the Spec Package is the fundamental unit of the system contract. Skills exist to maintain the package, not the other way around.
- **Audit**: Avoid using "Audit" generically. Use **Validator** for structural checks and **Redline** or **Report** for content-based diagnostics.

### Behavioral Evidence

Evidence that a skill applies its intended judgment to realistic inputs and produces useful, bounded, traceable, handoff-ready artifacts. Behavioral evidence goes beyond structural validation: it evaluates whether the skill made the right distinctions, avoided hallucinated scope, and preserved downstream usability.

### Behavioral Validation

Behavioral Validation is the testing phase where a skill is run against realistic fixtures to generate Behavioral Evidence. It may include automated rubric checks and classifications, but it does not approve promotion by itself. Its purpose is to prepare evidence for Human Review.

### Promotion Reference Evidence

The curated, human-approved snapshot of successful behavioral evidence for a **stable** skill. It lives under `examples/promotion/<skill-name>/reference/` and points back to the original timestamped `promotion-runs/` directory. It is the discoverable "gold-standard" example for maintainers, not the source of truth for historical execution.
### Blocking Failure Modes

Promotion to **stable** must be blocked if any of these occur:
1. **Hallucination:** Invention of surfaces, components, or findings not present in the fixture.
2. **Scope Drift:** Performance of work outside the requested UI scope or skill responsibility.
3. **Label Friction:** Use of non-canonical terminology that breaks downstream routing.
4. **Incomplete Context:** Ignoring critical constraints, exclusions, or priorities provided in the fixture.
5. **Handoff Failure:** Downstream inability to consume the output without manual repair.
6. **Evidence Gap:** Traceability failures where claims cannot be backed by run artifacts.

### Approved with Caveats

A behavioral review may be marked **APPROVED WITH CAVEATS** only if no blocking failure modes are present and the caveats are minor, documented, and do not affect downstream handoff or judgment fidelity. This status may support **beta** status but should generally block **stable** promotion until resolved.

### Minimum Behavioral Complexity

Behavioral fixtures must include enough ambiguity, conflict, or domain pressure to test judgment fidelity. Defaults:
- **Inventory skills:** At least 3 UI surfaces/candidates with one ambiguous boundary.
- **Issue/Audit skills:** At least 5 findings with mixed severity and one prioritization conflict.

### Improvement Brief

A document (improvement-brief.md) required when a skill passes structural validation but fails Behavioral Validation. It records the failed fixture, the blocking mode, evidence excerpts, and recommended next investigation. If the fixture itself is flawed, a **fixture repair brief** is triggered instead.

### Behavioral Result Classifications

| Classification | Meaning | Promotion Eligible? |
|---|---|---|
| **pass** | Behavioral evidence is strong and traceable. | Yes (Human Review next). |
| **approved_with_caveats** | Minor quirks; no blocking modes present. | Maybe (Beta/Candidate only). |
| **blocked_skill_failure** | Skill judgment failed on a valid fixture. | No (Needs Improvement Brief). |
| **fixture_repair_required** | Fixture input is flawed/incomplete. | No (Needs Fixture Repair). |
| **inconclusive** | Evidence is too weak or fuzzy to judge. | No (Needs Investigation). |


### Simulated Handoff

A behavioral verification where a reviewer evaluates whether the skill output satisfies the documented input contract of a downstream skill, without requiring the downstream skill itself to be stable. Simulated handoff supports **individual stable promotion** for a skill's own output contract but does not claim full-chain stability.

### Real Handoff

A behavioral verification where a downstream skill actually consumes the output of an upstream skill in a live run. Real handoff is required for **Workflow Promotion** and **Full-Chain Stability**.


## Common Artifact Types

| Artifact | Purpose | Required File | Promotion Evidence | Stability Support | Common Neighbors |
|------|---------|---------------|--------------------|-------------------|------------------|
| **Plan** | Defines the work to be done. | `PLAN.md` | No | No | `ui-brief` |
| **Spec Package** | Defines expected behavior/structure. | `SPEC-PACKAGE.md` | Yes (structural) | Partial | All downstream skills |
| **Inventory** | Enumerates UI surfaces. | `INVENTORY.md` | No | No | `ui-surface-inventory` |
| **Blueprint** | Generates a new Spec Package. | `BLUEPRINT.md` | No | No | `ui-blueprint`, `ui-brief` |
| **Brief** | High-level summary + direction. | `BRIEF.md` | No | Partial | `ui-brief`, `ui-redline` |
| **Reference** | Canonical implementation sample. | `REFERENCE.md` | Yes (behavioral) | Yes (for baseline) | All skills |
| **Artifact** | Output of a single skill. | varies (e.g. `REDLINE.md`) | Yes (if approved) | Depends | Any skill |
| **Fixture** | Frozen example of inputs+outputs. | varies | No | No | All skills |
