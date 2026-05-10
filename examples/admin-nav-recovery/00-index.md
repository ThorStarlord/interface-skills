# Admin Navigation Recovery Fixture

## Fixture Purpose

Tests retrospective specification on an **app-shell navigation surface** in a separate repo, with emphasis on:

- **static-source inspection** without runtime browser evidence
- **route registry contradictions** (canonical vs legacy paths)
- **partial redline behavior** (what was and was not verified)
- **target-only reconciliation** (spec stabilized, implementation awaiting refactor)
- **docs-sync failures** across nested monorepo agent files  
- **report-mode agent routing** (fail gracefully without applying patches)
- **issue slicing** from navigation redlines

This fixture is designed to validate that Interface Skills can handle not just **page/content surfaces** (like `/kanban`), but also **app-shell, navigation-map, and route-infrastructure surfaces** where:

- Route registries are sources of truth alongside source code
- Agent routing files are nested (root AGENTS.md + app-level AGENTS.md)
- Static verification is partial by nature (active states, colors, screen reader behavior cannot be verified from source alone)
- Reconciliation may result in "target-only" decisions (spec is stable, implementation awaits refactor)

---

## Fixture Layout Contract

```
admin-nav-recovery/
  fixture.yaml                     # metadata: source repo, surfaces, surfaces, workflow
  00-index.md                      # this file; fixture purpose and layout
  notes.md                         # human-review questions, fixture markers
  input/                           # curated test inputs for the skill workflow
    surface-inventory.md           # detected surfaces
    inspector-findings.md          # static inspection with confidence/partial marks
    spec-reconcile-input.md        # redlines + implementation audit
    docs-sync-input.md             # agent doc audit
  reports/                         # expected outputs from skill workflow
    SURFACE-INVENTORY-V1.md        # ui-surface-inventory output
    INSPECTOR-REPORT-V1.md         # ui-inspector output (static partial)
    SPEC-LINT-REPORT-V2.md         # ui-spec-linter output
    SPEC-RECONCILE-SUMMARY.md      # ui-spec-reconcile (target-only result)
    DOCS-SYNC-REPORT.md            # ui-docs-sync findings
    UI-AGENT-ROUTING-REPORT.md     # ui-agent-routing (report mode, fail)
    REDLINE-PARTIAL.md             # ui-redline with unverifiable items
    GITHUB-ISSUES-PLAN.md          # ui-to-issues with redline coverage
  expected/
    rubric.md                      # acceptance criteria
```

### Folder Purpose

- **fixture.yaml** — Machine-readable metadata. Pinned to source repo and commit once populated. Contains surfaces, focused skills, key_learnings.
- **00-index.md** — This file. Explains fixture's unique value vs `/kanban`. Clarifies what each output folder contains.
- **notes.md** — Human-review questions to validate fixture correctness. Fixture freeze marker and refresh markers.
- **input/** — Curated test inputs (surfaces detected, findings, inputs to spec tools). Can be auto-generated once or manually curated.
- **reports/** — Expected outputs from each skill in the retrospective-specification workflow.
- **expected/rubric.md** — Acceptance criteria. What good outputs must contain for each skill.

---

## How Agents Find This Fixture

This fixture demonstrates a **navigation/app-shell retrospective specification**, not yet validated against live agents. When ready for integration testing:

1. Agents will search for fixtures with `surface_type: app-shell-navigation` in fixture.yaml
2. fixture.yaml lists all surfaces and focused skills
3. notes.md documents human-review status and refresh markers
4. reports/ folder contains expected outputs (currently being populated)

Link in agent docs: [Admin Navigation Recovery](../admin-nav-recovery/00-index.md)

---

## Key Differences vs `/kanban` Fixture

| Aspect | `/kanban` | `admin-nav-recovery` |
|--------|-----------|----------------------|
| **Surface Type** | content page (spec for cards, modals) | app-shell navigation (route registry, active states) |
| **Inspector Type** | browser-based full screenshot | static source-code (partial coverage) |
| **Reconciliation** | full reconciliation of spec vs impl | target-only (spec stable, impl awaits refactor) |
| **Agent Docs** | single AGENTS.md | nested (root + app-level) |
| **Redline** | full visual verification | partial (unverifiable without browser) |
| **Routing** | applied/confirmed | report-mode failure (unresolved) |
| **Core Test** | Can skills handle full spec recovery? | Can skills handle nav/shell partial recovery? |

---

## Quick Start

To understand this fixture:

1. Read [fixture.yaml](fixture.yaml) for source repo and pinned commit
2. Check [notes.md](notes.md) for human-review questions and fixture status
3. Review [expected/rubric.md](expected/rubric.md) for acceptance criteria
4. Examine reports/ to see what each skill should output

To run this fixture against draft skills:

```bash
python scripts/validate-examples.py examples/admin-nav-recovery --strict-local-sources
```

---

## Status

- **Fixture Created:** 2026-05-10
- **Source Populated:** Not yet (awaiting source repo snapshot)
- **Human Review:** Pending (see notes.md)
- **Validated:** Not yet (awaiting inputs/ and reports/)
