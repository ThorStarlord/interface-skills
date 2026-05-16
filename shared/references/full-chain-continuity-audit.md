# Full-Chain Continuity Audit Template

This audit is performed after a **Workflow Promotion** run to verify that the "Semantic Thread" was preserved from the starting evidence to the final implementation issues.

## Metadata
- **Workflow ID**: 
- **Run ID**: 
- **Starting Artifact**: 
- **Terminal Artifact**: 

## Audit Criteria

### 1. Intent Preservation
- [ ] Does the terminal artifact address the primary goal defined in the source evidence/brief?
- [ ] Were any critical "Must-Have" requirements lost during handoff?

### 2. Surface Traceability
- [ ] Can every issue/component in the terminal artifact be traced back to a specific surface identified in the `ui-surface-inventory`?
- [ ] Are there any "Ghost Surfaces" (hallucinated surfaces not in the source)?

### 3. Context Continuity
- [ ] Does the final artifact preserve the domain-specific terminology established in the `ui-brief`?
- [ ] Were ambiguity notes from earlier steps correctly resolved or explicitly carried forward as "Unknowns"?

### 4. Zero-Manual-Repair Verification
- [ ] Did any step require manual "label repair" to satisfy a downstream validator?
- [ ] Were any paths manually corrected to allow skill discovery?

## Verdict
- **Classification**: [Pass / Pass with Caveats / Blocked]
- **Summary of Drift**: 
- **Continuity Rating (1-5)**: 
