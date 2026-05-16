# Skill Certification System Hardening Plan

This document outlines the transition of the Skill Certification System from a **Tracer-Bullet Architecture** to a **Production-Ready Certification Authority**.

## Goal
Establish a deterministic, auditable, and deep validation layer that proves skill and workflow stability before promotion to `stable` or `full-chain-stable`.

---

## Phase 1: Validator Depth & Governance (Hardened Gates)
**Status: In Progress**

Focus: Turn shallow "path-check" validators into "semantic-authority" validators.

### 1.1 Human Review Governance (`human_review.py`)
- [x] **Strict Field Enforcement**: Mandate `Reviewer`, `Date`, and `Decision` fields.
- [x] **Authority Normalization**: Validate approvals against explicit `Decision` inputs.
- [ ] **Rich Template Validation**: Verify the checklist completeness (e.g., specific behavioral scrutiny items).
- [ ] **Governance Audit**: Ensure the `HUMAN-REVIEW.md` is traceable to a specific `PROMOTION-RUN`.

### 1.2 Promotion Plan Authority (`promotion_plan.py`)
- [x] **Registry Grounding**: Verify skill IDs against `skills.json`.
- [x] **Semantic Completeness**: Enforce presence of `behavioral_criteria`.
- [x] **Handoff Contract**: Enforce `downstream` block coherence for required downstream skills.
- [ ] **Boundary Rules**: Enforce ADR 0006/0007 constraints (e.g., individual vs workflow scope).
- [ ] **Family Validation**: Ensure `fixture_family` matches the actual fixture directory structure.

### 1.3 Fixture Integrity (`fixture_integrity.py`)
- [ ] **Non-Triviality Check**: Enforce minimum file size/content depth for clean fixtures.
- [ ] **Input Artifact Verification**: Verify that all required inputs for the skill exist in the fixture.
- [ ] **Adversarial Intent**: Tag messy fixtures and verify they trigger expected failure modes.
- [ ] **Repair Ownership**: Trace fixture repairs back to the failing promotion run.

### 1.4 Behavioral Depth (`behavioral_result.py`)
- [ ] **Traceability**: Verify that output artifacts link back to specific input identifiers.
- [ ] **Boundedness**: Detect "hallucinated" findings outside the fixture's domain.
- [ ] **Skill-Specific Metrics**: Expand complexity thresholds for all skills in `promotion-plan.yaml`.
- [ ] **Zero-Manual-Repair Integration**: Verify output hashes match the `.zero-repair` contract.

---

## Phase 2: Workflow Generalization (Full-Chain Trust)
**Status: Partial**

Focus: Ensuring that workflow certification is as rigorous as individual skill certification.

### 2.1 Handoff Certification (`handoff_verification.py`)
- [x] **Mode Detection**: Detect "Real" vs "Simulated" handoffs.
- [x] **ADR 0007 Enforcement**: Strictly require Real handoff for `workflow` scope.
- [ ] **Consumption Contract**: Verify that downstream skills actually used the *correct* upstream artifact path.
- [ ] **Zero-Repair Proof**: Mechanically prove that no human manual edits were made between steps.

### 2.2 Workflow Continuity (`workflow_link.py`)
- [ ] **Registry-Wide Coverage**: Extend validation to all workflows in `workflow-registry.yaml`.
- [ ] **Semantic Thread Audit**: Verify that the "Intent ID" (e.g., `spec_id`) is consistent across 3+ steps.
- [ ] **Regression Integration**: Ensure all workflow steps pass their individual behavioral criteria during a full-chain run.

---

## Phase 3: Authority & Automation (Self-Healing Evidence)
**Status: Proposed**

Focus: Automating the lifecycle of "Gold Standard" evidence.

### 3.1 Reference Evidence Authority (`reference_evidence.py`)
- [ ] **Authorization Traceability**: Verify the reference snapshot is cited by a signed `HUMAN-REVIEW.md`.
- [ ] **Dirty Snapshot Detection**: Prevent unrelated or temporary files from entering `reference/` dirs.
- [ ] **Promotion Lock**: Block registry updates if reference evidence is out of sync with the latest approved run.

### 3.2 Automated Evidence Lifecycle
- [ ] **Reference Sync**: Implement `scripts/sync-reference-evidence.py` to move approved run artifacts to reference dirs.
- [ ] **Continuous Certification**: Integrate validator suite into CI/CD (GitHub Actions).
- [ ] **Stability Dashboard**: Generate an aggregated `STABILITY-REPORT.md` across all skills and workflows.

---

## Implementation Status Tracking

| Component | Status | Target |
| :--- | :---: | :--- |
| **Governance Gate** | 🟡 | Phase 1 |
| **Config Authority** | 🟡 | Phase 1 |
| **Fixture Integrity** | 🔴 | Phase 1 |
| **Behavioral Depth** | 🟡 | Phase 1 |
| **Handoff Proof** | 🟡 | Phase 2 |
| **Workflow Continuity**| 🟡 | Phase 2 |
| **Reference Authority** | 🔴 | Phase 3 |

---

## ADR Status
- [ ] **ADR 0008: Skill Certification System Architecture**
  - **Proposed**: 2026-05-16
  - **Ratification Target**: Completion of Phase 1 hardening.
