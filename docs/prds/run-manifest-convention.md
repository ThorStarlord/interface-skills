# PRD: Run Manifest Convention

## Problem Statement

Agents often consume "stale reports"—documents like redline reports or lint reports that were generated against an older version of the code or spec. This causes agents to waste effort fixing issues that no longer exist or making decisions based on outdated information. There is no standard way to track which reports are currently valid and which have been superseded.

## Solution

Implement a **Run Manifest** convention, integrated into the `00-index.md` of every Spec Package. This manifest will explicitly list active, historical, and superseded reports, along with a log of recent skill runs. This provides a clear "checkpoint" for agents to verify the freshness of the documentation they are reading.

## User Stories

1. As a developer agent, I want to see which reports are currently active, so I don't act on stale data.
2. As a human maintainer, I want to see the history of skill runs in a spec package, so I can understand how the current state was reached.
3. As a skill (e.g., `ui-redline`), I want a standard place to register my output, so that I can automatically mark previous outputs as superseded.
4. As a validator, I want to check if a spec package has a valid run manifest, so I can ensure documentation quality.

## Implementation Decisions

- **Location**: Required location is `00-index.md` (canonical package index). The convention does not use a standalone `RUN-MANIFEST.md`.
- **Required Sections**:
  - `## Run history`: A table of skill executions.
  - `## Active reports`: Links to currently valid report artifacts.
  - `## Historical reports`: Links to archived reports that are still relevant for context.
  - `## Superseded reports`: Links to reports that have been explicitly replaced by newer versions.
- **Renaming Convention**: When a report is superseded, it should be moved or renamed to include a timestamp or version identifier to avoid filename collisions and clearly indicate its status.
- **Template Update**: `templates/spec-package/00-index.md` will be updated to include these sections by default.

## Testing Decisions

- **Template Verification**: Ensure the template renders correctly and includes the new sections.
- **Example Migration**: Update an existing example and verify it passes structural validation (if any).
- **Linter Check**: Add a rule to `ui-spec-linter` (or equivalent) to validate these sections in `00-index.md`, and warn if they are missing or empty in any package that contains reports.

## Out of Scope

- Automated cleanup of old files (for now, we just rename/move and track).
- Centralized repo-wide manifest (this focus is per Spec Package).
