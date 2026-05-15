# Interface Skills

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Skills](https://img.shields.io/badge/Skills-21-blue.svg)](#skill-catalog)
[![Validate Skills](https://github.com/vibe-sh/interface-skills/actions/workflows/validate.yml/badge.svg)](https://github.com/vibe-sh/interface-skills/actions/workflows/validate.yml)
[![Universal Agent Export](https://img.shields.io/badge/Universal%20Agent%20Export-Supported-green.svg)](#option-e-universal-agent-export-agentsskills)

> **Visual contracts for AI-built interfaces.**

Interface Skills is a collection of reusable AI skills for building and maintaining **Spec Packages**—visual contracts that turn fuzzy UI intent into precise, testable interface specifications.

The goal is to reduce the gap between the interface you imagine and the interface an AI model builds by treating the specification as the primary source of truth.

## Why Interface Skills exists

The fundamental unit of work in Interface Skills is the **Spec Package**. Skills are simply the producers and maintainers of the artifacts within that package.

AI can produce UI quickly, but speed creates new failure modes:

1. **Vague intent:** The model builds from ambiguous descriptions.
2. **Implicit visual taste:** Design preferences stay in the human's head.
3. **Missing specs:** Existing UI has no recoverable source of truth.
4. **Spec drift:** Documentation and implementation quickly move out of sync.
5. **Agent routing:** Coding agents ignore documentation because they can't find it.

Interface Skills turns UI work into explicit, testable contracts so humans and agents can share the same target.

## Philosophy

**Interface failures are usually process failures, not people failures.**

If an AI-built UI misses the mark, the fix is not to blame the model or the developer. The fix is to improve the contract:
- Clearer intent through structured briefs.
- Named visual language instead of "vibes."
- Explicit states and behaviors.
- Evidence-based inspection and redlines.
- Routed documentation that agents actually discover.

## What you can do with it

- **Design a UI from vague intent** → Start with `ui-brief`
- **Recover specs from an existing UI** → Use the [Retrospective Specification workflow](#retrospective-specification-workflow)
- **Compare implementation to spec** → Use `ui-inspector` ⚠️ + `ui-redline`
- **Reconcile specs after fixes** → Use `ui-spec-reconcile` ⚠️
- **Route agents to the right docs** → Use `ui-docs-sync` + `ui-agent-routing`
- **Turn redlines into work** → Use `ui-to-issues`

## Quickstart

### New UI feature
Ask your agent to run:
1. `ui-brief`
2. `ui-visual-calibration` ⚠️
3. `ui-blueprint`
4. `ui-screen-spec` ⚠️
5. `ui-acceptance`

### Existing UI with no spec
Ask your agent to run:
1. `ui-surface-inventory`
2. `ui-inspector` ⚠️
3. `ui-brief`
4. `ui-blueprint`

### Repo setup
Run once to prepare your repository for Interface Skills:
`setup-interface-skills` ⚠️

*Note: If installed in Claude Code or another slash-command environment, these may appear as slash commands. Otherwise, invoke them by name in your agent.*

## Which workflow should I use?

| Situation | Start here |
|---|---|
| I have a vague UI idea | `ui-brief` |
| I have an existing UI but no spec | `ui-surface-inventory` ⚠️ |
| I have a spec and code, but they differ | `ui-redline` |
| I fixed code and need to update specs | `ui-spec-reconcile` |
| I created specs but agents cannot find them | `ui-agent-routing` |
| I need GitHub issues from a redline | `ui-to-issues` |

## Example spec package

A "Spec Package" is a directory containing the collective evidence and specifications for a UI scope.

```text
docs/saas-frontend/specs/create/
├── 00-index.md
├── 01-inspector-evidence.md
├── 02-brief.md
├── 03-visual-calibration.md
├── 04-blueprint.md
├── 05-screen-spec.md
├── 06-component-spec-*.md
├── 07-microcopy.md
├── 08-acceptance-checklist.md
├── 09-redlines.md
├── SPEC-LINT-REPORT.md
├── SPEC-RECONCILE-SUMMARY.md
├── DOCS-SYNC-REPORT.md
└── UI-AGENT-ROUTING-SUMMARY.md
```

> *Note: Some older examples in the repository may use legacy filenames while draft skills are being stabilized.*

## Skill Catalog

Grouped by the UI lifecycle. For a detailed technical reference with inputs and outputs, see [Skill Reference](./docs/skill-reference.md).

### Setup & Discovery
| Skill                    | Use when                      | Produces                     |
| ------------------------ | ----------------------------- | ---------------------------- |
| `setup-interface-skills` | Starting in a repo            | Repo conventions and routing |
| `ui-surface-inventory` | Existing app or unclear scope | Recoverable UI scope map     |
| `ui-orchestrator`         | Unsure what to run next       | Next-skill recommendation    |

### Intent & Visual Language
| Skill                   | Use when                      | Produces                  |
| ----------------------- | ----------------------------- | ------------------------- |
| `ui-brief`              | Vague product/design idea     | Product/design brief      |
| `ui-visual-calibration` ⚠️ | Visual taste is unclear       | Visual language decisions |
| `ui-flow`               | Multiple screens are involved | Journey graph             |

### Specification
| Skill               | Use when                         | Produces                  |
| ------------------- | -------------------------------- | ------------------------- |
| `ui-blueprint`      | Layout needs structure           | Wireframe/layout contract |
| `ui-system`         | Tokens/rules are needed          | Design system rules       |
| `ui-screen-spec` ⚠️    | Screen behavior must be explicit | Screen contract           |
| `ui-component-spec` | Component behavior matters       | Component state/a11y spec |
| `ui-microcopy`      | Copy must be approved            | Copy contract             |
| `ui-acceptance`     | Ready for QA                     | Checklist                 |

### Implementation & Inspection
| Skill               | Use when                  | Produces                          |
| ------------------- | ------------------------- | --------------------------------- |
| `ui-generate-code`  | Ready to build            | React/CSS/HTML implementation     |
| `ui-inspector` ⚠️      | Inspect implementation    | DOM/a11y evidence report          |
| `ui-redline`        | Compare code to spec      | Mismatch report + refactor prompt |

### Maintenance & Planning
| Skill               | Use when                  | Produces               |
| ------------------- | ------------------------- | ---------------------- |
| `ui-spec-linter`         | Validate Spec Package     | Lint report            |
| `ui-spec-reconcile` ⚠️ | Code/spec changed         | Reconciled spec        |
| `ui-docs-sync`         | Docs may be stale         | Sync report            |
| `ui-agent-routing`     | Agents cannot find specs  | Routing report/patches |
| `ui-to-issues`         | Need implementation tasks | Markdown issues        |
| `ui-storybook-docs` ⚠️ | Component spec exists     | MDX docs and stories   |

> ⚠️ = currently a **draft** skill.

---

## Workflows

### Minimum viable workflow
For small, well-scoped features where visual tone is already agreed:
1. Run `ui-brief`
2. Run `ui-blueprint`
3. Run `ui-component-spec`
4. Run `ui-acceptance`
5. Run `ui-generate-code`
6. Run `ui-inspector` ⚠️
7. Run `ui-redline`

### Full documentation-first workflow
For new products, unfamiliar domains, or any work where misalignment is expensive:
1. Run `setup-interface-skills` *(once per repo)*
2. Run `ui-brief`
3. Run `ui-visual-calibration`
4. Run `ui-flow` *(multi-screen features only)*
5. Run `ui-blueprint`
6. Run `ui-system`
7. Run `ui-screen-spec`
8. Run `ui-component-spec`
9. Run `ui-microcopy`
10. Run `ui-acceptance`
11. Run `ui-spec-linter`
12. Run `ui-generate-code`
13. Run `ui-inspector`
14. Run `ui-redline`
15. Run `ui-spec-reconcile`
16. Run `ui-docs-sync`
17. Run `ui-agent-routing`
18. Run `ui-to-issues`

### Retrospective specification workflow
Use this when a UI already exists but no specification was created first ("Spec Recovery").

1. Run `setup-interface-skills` *(once per repo)*
2. Run `ui-surface-inventory` to map the existing UI.
3. Run `ui-inspector` on each scope's existing implementation.
4. Run `ui-brief` to reconstruct the missing product and design intent.
5. Run `ui-visual-calibration` to name the existing visual language.
6. Run `ui-blueprint` to document the as-built layout.
7. Run `ui-screen-spec` to map regions, components, data, and states.
8. Run `ui-component-spec` for each non-trivial component.
9. Run `ui-microcopy` to extract and approve existing UI text.
10. Run `ui-acceptance` to create the target checklist.
11. Run `ui-spec-linter` to check the recovered Spec Package.
12. Optionally run `ui-redline` to compare against the recovered target.
13. Run `ui-spec-reconcile` to stabilize the spec.
14. Run `ui-docs-sync` to confirm repository docs agreement.
15. Run `ui-agent-routing` to wire the package into agent discovery.
16. Run `ui-to-issues` to plan necessary refactors.

## Installation & Use

### Option A: Claude Code (Recommended)
Claude Code can use these skills globally or per-project.

```bash
# Install globally for all projects
python scripts/install-claude-code-skill.py skills/ui-brief --scope global

# Install for the current project only
python scripts/install-claude-code-skill.py skills/ui-brief --scope project
```

### Option B: Universal agent export (`.agents/skills`)
For agents that support the `.agents/skills` directory convention.

```bash
# Install one or more skills into the current project
python scripts/install-agent-skills.py skills/ui-orchestrator skills/ui-brief --scope project
```

### Option C: As ChatGPT Skills
Each folder under `skills/` includes `agents/openai.yaml` metadata for easy import into ChatGPT.

### Option D: As agent instructions
Copy the relevant `SKILL.md` into your coding agent context.

## Browser inspection policy

Browser inspection is optional, not assumed.

- Skills such as `ui-inspector` should detect whether Playwright is available in the current repository before attempting live browser checks.
- If browser tooling is unavailable, the skill should continue in static-source mode and explicitly mark runtime-only checks as deferred.
- Skills should not silently install Playwright, edit package files, or download browser binaries. Setup is optional and should happen only with explicit user approval.
- Acceptance criteria should use explicit automation labels such as `[A:playwright]`, `[A:axe]`, `[A:lint]`, `[A:unit]`, and `[M]` rather than a generic `[A]`.

Typical Playwright setup for an existing JavaScript or TypeScript frontend repository:

```bash
npm install -D @playwright/test
npx playwright install
```

### Distribution support matrix

| Install mode        | Script                              | Target               | Best for                          |
| ------------------- | ----------------------------------- | -------------------- | --------------------------------- |
| Claude Code         | `scripts/install-claude-code-skill.py` | `.claude/skills`  | Claude Code (global or project)   |
| Universal agents    | `scripts/install-agent-skills.py`   | `.agents/skills`     | multi-agent local workflows       |
| ZIP package         | `scripts/package-skill.py`          | ChatGPT Skill upload | single-skill import to ChatGPT    |

## Structure

- **`skills/`**: The individual AI skills.
- **`shared/references/`**: Common vocabulary and taxonomies used across all skills.
- **`examples/`**: Example "Spec Packages" that group outputs for a feature.
- **`templates/`**: Boilerplates for new projects.

## Contributing
See [CONTRIBUTING.md](./CONTRIBUTING.md) for how to add or improve skills.

## License
MIT License. See [LICENSE](./LICENSE) for more details.
