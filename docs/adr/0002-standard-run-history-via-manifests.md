# ADR 0002: Run History is recorded via Run Manifests

## Status
Accepted

## Context
As workflows involve multiple skills over time, agents lose track of the "lineage" of artifacts. 
- Which skill created `brief.md`?
- Is `lint-report.md` current or historical?
- What was the prompt or input used for the last generation?

## Decision
We will distinguish between the **Run History** (the concept) and the **Run Manifest** (the artifact).
- Every Spec Package must eventually include a Run Manifest.
- The manifest records skill invocations, timestamps, and input hashes.
- New skill runs must append to or update the manifest to maintain traceability.

## Consequences
- Workflows can be "resumed" by reading the manifest.
- Historical reports can be identified and superseded deterministically.
- Verification scripts can audit whether the manifest matches the files on disk.
