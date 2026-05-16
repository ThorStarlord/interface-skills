# ADR 0009: Mandatory Workflow Certification

## Status
Proposed

## Context
ADR 0007 established Workflow Promotion as the "gold standard" for stability, requiring real handoff evidence and zero-manual-repair criteria. However, enforcement was initially warning-only. 

As we scale to complex multi-skill chains, we must guarantee that any workflow marked as `stable` has been formally certified and is locked against drift.

## Decision
We enforce mandatory workflow certification for all production-grade workflows.

1. **Registry Status**: Workflows in `workflow-registry.yaml` must include a `status` field.
2. **Certification Requirement**: Any workflow marked `status: stable` MUST have an entry in `workflow_reference_record.json`.
3. **Run Validation**: The referenced `source_run_id` must point to a valid, approved promotion run in `promotion-runs/` with a passing `HUMAN-WORKFLOW-REVIEW.md`.
4. **CI Blocking**: The `verify_certification_authority.py` script will treat missing or invalid workflow certification for `stable` workflows as a blocking failure (Exit 1).
5. **Lock Enforcement**: The `enforce_promotion_lock.py` script will protect `workflow-registry.yaml` and `workflow_reference_record.json` from unauthorized modifications.

## Consequences
- Workflows cannot be claimed as `stable` without generating and approving real-world evidence.
- Repository integrity is hardened against "hallucinated stability" in autonomous chains.
- Maintainers have a clear audit trail for the current gold-standard execution of every stable workflow.
