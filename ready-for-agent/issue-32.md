## Agent Brief

**Category:** enhancement
**Summary:** Extract `handoff_verification.py` to enforce mode boundaries.

**Current behavior:**
Handoff evidence (simulated or real) is currently checked as part of a general behavioral sweep. There is no deterministic enforcement of the boundary between **Individual Stable** promotion (supported by simulated handoff) and **Full-Chain Stable** promotion (requiring real handoff). This risks overclaiming stability status for workflows.

**Desired behavior:**
Implement `scripts/validators/handoff_verification.py` to deterministically verify that the produced handoff evidence matches the requested promotion scope. It must ensure that a skill being promoted to "Stable" on the basis of simulated handoff does not erroneously claim to have verified the full-chain workflow.

**Key interfaces:**
- `ValidatorResult` — Use the standard contract.
- `validate_handoff(evidence_path, mode)` — Entrypoint. Mode is one of `simulated` or `real`.

**Acceptance criteria:**
- [ ] Verifies the existence of required handoff artifacts (e.g., downstream input packages).
- [ ] Strictly enforces the boundary: `simulated` mode fails if the evidence claims full-chain stability.
- [ ] Checks for the presence of "manual repair" notes; real handoff requires zero-manual-repair evidence.

**Out of scope:**
- Modifying ADR 0006 or ADR 0007.
- Automating the downstream skill execution itself.
