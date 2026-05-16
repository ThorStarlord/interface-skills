# ADR 0007: Workflow Promotion and Full-Chain Stability

## Status
Proposed

## Context
ADR 0006 established the process for **Individual Skill Promotion** using simulated handoff to avoid promotion deadlocks. However, it explicitly stated that "Full-chain stability requires separate end-to-end evidence and a broader 'Workflow' promotion." 

As the `interface-skills` library matures, we need a formal mechanism to certify that a sequence of skills (a Workflow) works reliably as a unit, without manual repair between steps. This is critical for autonomous execution and higher-order orchestration.

## Decision
We introduce **Workflow Promotion** as a higher-level certification above individual skill stability.

1. **Workflow Definition**: A workflow must be defined in `workflow-registry.yaml` with an ordered set of skill steps.
2. **Individual Prerequisites**: All skills within the workflow must be individually promoted to **stable** (per ADR 0006).
3. **Full-Chain Evidence**: Promotion to **Full-Chain Stable** requires evidence from at least one **Real Handoff** run across the entire workflow.
4. **Zero-Manual-Repair**: The evidence must prove that every downstream skill consumed the upstream output without any human "repair" or intervention.
5. **Continuity Audit**: A formal check must confirm that the final artifact (e.g., implementation issues) preserves the original intent and context defined in the starting artifact (e.g., the brief).
6. **Workflow Status**: Workflows will be marked as `stable` in the `workflow-registry.yaml` when these criteria are met.

## Consequences
- **Workflow Promotion** is the "gold standard" for repository stability.
- Promotion evidence for a workflow is stored in a `promotion-runs/` manifest that includes all intermediate artifacts.
- A failure in a workflow run does not necessarily revoke individual skill stability, but it blocks the workflow from being promoted.
- Users and agents can rely on `Full-Chain Stable` workflows for high-stakes autonomous tasks.
