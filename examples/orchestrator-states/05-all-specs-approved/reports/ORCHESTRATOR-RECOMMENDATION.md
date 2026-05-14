## Orchestrator recommendation

**Current state:**
- All spec files present and approved.

**Gap identified:** No implementation exists yet, and the spec package has not been linted for internal consistency.

**Recommended next skill:** `ui-spec-linter`

**Reason:** Before handing the spec to an implementer, run the linter to catch conflicts between files (e.g. a component spec that references a token the system spec doesn't define).
