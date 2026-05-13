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
_Avoid_: "random docs," "output folder," "spec dump," "docs bundle."

### Skill
A reusable instruction package that performs one step, such as `ui-brief` or `ui-redline`. Skills are producers and maintainers of spec package artifacts.
_Avoid_: "function," "script," "prompt," "agent task."

### Workflow
An ordered chain of skills for a common situation (e.g., Spec Recovery).

### UI Scope
The surface being specified or inspected (e.g., `/kanban` route or `Sidebar` component).
_Avoid_: "page," "screen," "module," "UI part."

### Artifact
A single output file from a skill (e.g., `02-brief.md`).
_Avoid_: "document," "file," "template," "output."

### Report
An artifact that audits, compares, or routes work (e.g., `SPEC-LINT-REPORT.md`).

### Fixture
A frozen example case used to validate draft skills.
_Avoid_: "live product docs," "current source of truth," "test data."

### Validator
A deterministic script or checklist that checks structure and metadata.
_Avoid_: "reviewer," "judge," "quality oracle."

### Human Review
The judgment step that decides whether a structurally valid output is actually useful and not misleading.

### Agent Routing
The process of wiring spec packages into agent discovery files (e.g., `CLAUDE.md`).

### Promotion
The process of moving a skill from draft to stable after enough fixture evidence.

## Relationships

- A **UI Scope** is the target for one **Spec Package**.
- A **Workflow** is an ordered chain of **Skills**.
- A **Skill** produces or updates **Artifacts** within a **Spec Package**.
- A **Report** audits, compares, reconciles, or routes a **Spec Package**.
- A **Fixture** freezes a real **Spec Package** so draft skills can be validated.
- A **Validator** checks structure; **Human Review** checks usefulness and intent.
- **Promotion** moves a **Skill** from draft to stable after fixture evidence confirms the output format is locked.

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

## Example dialogue

> **User:** "I ran the retrospective workflow on `/kanban`. Should I keep generating more outputs?"
>
> **Maintainer:** "No. First freeze the `/kanban` output as a **Fixture**. The live product docs remain in the product repo; the copied fixture in `interface-skills/examples/` becomes a test case for draft skills."
>
> **User:** "The validator failed on my **Artifact** even though the content is good."
>
> **Maintainer:** "The **Validator** checks for deterministic structure (like metadata). If the structure is correct, use **Human Review** to decide if the content is actually helpful."

## Flagged ambiguities

- **Skill vs. Spec Package**: While Skills are the visible tools, the Spec Package is the fundamental unit of the system contract. Skills exist to maintain the package, not the other way around.
- **Audit**: Avoid using "Audit" generically. Use **Validator** for structural checks and **Redline** or **Report** for content-based diagnostics.
