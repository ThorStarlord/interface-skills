## Agent Brief

**Category:** enhancement
**Summary:** Extract `reference_evidence.py` for curation and traceability.

**Current behavior:**
**Promotion Reference Evidence** (in `examples/promotion/<skill>/reference/`) is often manually synced or copied from historical runs. There is a risk of loose logs, temporary files, or unauthorized evidence snapshots polluting the gold-standard reference set, which degrades the quality of future regression tests.

**Desired behavior:**
Implement `scripts/validators/reference_evidence.py` to govern the curation of reference evidence. It must ensure that any artifact in the reference directory is authorized, traceable to a specific human-approved promotion run, and free of non-canonical artifacts.

**Key interfaces:**
- `ValidatorResult` — Use the standard contract.
- `validate_reference_evidence(reference_path, authorized_run_id)` — Entrypoint.

**Acceptance criteria:**
- [ ] Rejects reference evidence that contains loose logs, scratch files, or unrelated outputs.
- [ ] Validates that the artifacts match the **Canonical Package Format** for the skill.
- [ ] Rejects "automatic syncs" that cannot be traced to a run cited in a `HUMAN-REVIEW.md`.

**Out of scope:**
- Performing the `git sync` or `rsync` operation (this is a harness task).
- Deleting historical promotion runs.
