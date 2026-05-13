# ADR 0004: UI Orchestrator as a Pure Routing Skill

## Status
Accepted

## Context
As the Interface Skills system grows, there is a temptation to make the `ui-orchestrator` (the meta-skill that recommends the next step) more "powerful" by allowing it to automatically fix gaps, draft missing files, or mutate the `RUN-MANIFEST.md`.

However, this creates several architectural risks:
1. **Monolithic Complexity**: The orchestrator becomes a "god skill" that needs to understand the implementation details of every other skill in the toolkit.
2. **Loss of Determinism**: If the orchestrator automatically "fixes" things, it becomes harder for users to verify its work or undo specific design choices.
3. **Violation of Composability**: The system is designed to be a collection of specialized, composable skills. A "smart" orchestrator that does everything undermines this separation of concerns.

## Decision
We will enforce a strict "Read-Only Router" constraint on the `ui-orchestrator`.

1. **Analytical Only**: The orchestrator is limited to reading the current directory state (files and their frontmatter) and comparing it against the canonical UI pipeline.
2. **Zero Mutation**: The orchestrator must never modify any file, create new files, or run other skills on behalf of the user.
3. **Explicit Recommendations**: Its only output is a structured recommendation block (Current State, Gap, Recommended Skill, Reason).
4. **Delegated Execution**: The user (or a separate execution agent) is responsible for invoking the recommended skill.

## Consequences
- **Positive**: The orchestrator remains lightweight, easy to test, and predictable.
- **Positive**: Encourages "skill-first" thinking, where each step of the UI specification is a discrete, human-verifiable unit of work.
- **Negative**: Users must manually run the next skill (though this can be automated by a separate execution loop that reads the orchestrator's recommendation).
- **Negative**: Requires the orchestrator to have perfect read access to all spec artifacts to give accurate advice.
