# Source Snippet Map: Kanban Recovery

This folder records which real source files from `ViralFactory` produced the fixture evidence.

Pinned source commit: `bc815b38d7245ffec42016306b486e48c2896681`

## Primary implementation files

- `saas_frontend/src/pages/KanbanPage.tsx`
- `saas_frontend/src/components/kanban/KanbanCard.tsx`
- `saas_frontend/src/components/kanban/PostDetailModal.tsx`
- `saas_frontend/src/hooks/useKanban.tsx`
- `saas_frontend/src/lib/kanbanReviewMode.ts`
- `saas_frontend/src/index.css`

## Routing and policy context files

- `CLAUDE.md`
- `AGENTS.md`
- `INTERFACE_SKILLS.md`
- `docs/saas-frontend/specs/kanban/00-index.md`
- `llm-docs/CONTENT-JOURNEY-UX-CONTRACT.md`

## Why snippets are mapped (not vendored)

To avoid duplicating a large application inside this repository, this fixture pins exact source paths and commit SHA. Reproduction tooling should load these files from `ViralFactory` at the pinned commit.

## Re-run recipe

1. Checkout `ViralFactory` at commit `bc815b38d7245ffec42016306b486e48c2896681`.
2. Read the files listed in `examples/kanban-recovery/fixture.yaml` (`source_files` and `routing_files`).
3. Run the retrospective workflow for `/kanban` (`ui-inspector` -> `ui-spec-linter` -> `ui-spec-reconcile` -> `ui-docs-sync` -> `ui-agent-routing` -> `ui-to-issues`).
4. Compare generated outputs against `examples/kanban-recovery/expected/rubric.md`.
5. Record subjective judgments in `examples/kanban-recovery/notes.md` under "Human review required".