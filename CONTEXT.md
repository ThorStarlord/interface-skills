# Interface Skills Context

## Purpose

Interface Skills is a toolkit for turning fuzzy, existing, or drifting UI work into explicit, testable interface specifications.

## Philosophy

Interface failures are usually process failures, not people failures.

When an AI-built UI misses the mark, improve the contract:
- clearer intent
- named visual language
- explicit states
- evidence-based inspection
- testable acceptance
- routed documentation agents can find

## Core vocabulary

### Spec Package
The most fundamental unit of work. A folder containing the artifacts for one UI scope.

Canonical entry point:
- `00-index.md`

### Skill
A reusable instruction package that performs one step, such as `ui-brief`, `ui-redline`, or `ui-agent-routing`. Skills are producers and maintainers of spec package artifacts.

### Workflow
An ordered chain of skills for a common situation.

Main workflows:
- Minimum viable workflow
- Full documentation-first workflow
- Retrospective specification workflow

### UI Scope
The surface being specified or inspected.

Examples:
- route: `/kanban`
- app shell: sidebar navigation
- component: `PostDetailModal`
- modal/drawer/state surface

### Artifact
A single output file from a skill.

Examples:
- `02-brief.md`
- `05-screen-spec.md`
- `08-acceptance-checklist.md`
- `redlines/redline-report.md`

### Report
An artifact that audits, compares, or routes work.

Examples:
- `SPEC-LINT-REPORT.md`
- `DOCS-SYNC-REPORT.md`
- `UI-AGENT-ROUTING-SUMMARY.md`

### Fixture
A frozen example case used to validate draft skills. A fixture is not live product documentation. It is a test case for the skill system.

### Validator
A deterministic script or checklist that checks structure and metadata. Validators do not replace human judgment.

### Human Review
The judgment step that decides whether a structurally valid output is actually useful and not misleading.

### Agent Routing
The process of wiring spec packages into files like `CLAUDE.md`, `AGENTS.md`, `GEMINI.md`, `.cursor/rules`, and Copilot instructions so future agents find the right spec.

### Promotion
The process of moving a skill from draft to stable after enough fixture evidence.

## Source of truth hierarchy

1. Skill definitions in `skills/*/SKILL.md`
2. Shared references in `shared/references/`
3. Canonical package format and templates
4. Validated examples and fixtures
5. README and skill reference docs

## Draft vs stable

Draft means the behavior is defined but still being validated with real fixtures.

Stable means the output contract is reliable enough for other skills and agents to depend on.

## Process rule

Scripts enforce structure.
Skills provide judgment.
Humans approve whether the result is useful and not misleading.
