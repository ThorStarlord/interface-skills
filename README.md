# Interface Skills

> **Visual contracts for AI-built interfaces.**

Reusable AI skills for turning fuzzy UI intent into precise, testable interface specifications.

Interface Skills is a collection of skills for designing, documenting, generating, and diagnosing user interfaces with AI. It helps transform vague requests like “make this dashboard cleaner” into structured briefs, visual calibration sheets, screen blueprints, design tokens, component specs, acceptance criteria, implementation plans, and redline audits.

The goal is simple: reduce the gap between the interface you imagine and the interface an AI model builds.

## Core workflow

```text
brief → visual calibration → flow → blueprint → system → screen spec → component spec → microcopy → acceptance → code generation → inspection → redline
```

## Structure

This repository is organized into a cohesive toolkit:
- **`skills/`**: The individual AI skills.
- **`shared/references/`**: Common vocabulary and taxonomies used across all skills to maintain consistency.
- **`examples/`**: Example "Spec Packages" that group outputs for a feature.
- **`templates/`**: Boilerplates for new projects.

## Installation & Use

### Option A: As ChatGPT Skills
Each folder under `skills/` is intended to be packaged as an individual Skill. They include `agents/openai.yaml` metadata for easy import.

### Option B: As agent instructions
Copy the relevant `SKILL.md` into your coding agent context.

### Recommended First Workflow
1. Run `ui-brief`
2. Run `ui-blueprint`
3. Run `ui-component-spec`
4. Run `ui-acceptance`
5. Run `ui-generate-code`
6. Run `ui-redline`

## Skill Map

| Skill                     | Input                          | Output                            | Next                                    |
| ------------------------- | ------------------------------ | --------------------------------- | --------------------------------------- |
| `ui-brief`                | vague UI idea                  | product/design brief              | `ui-flow`, `ui-blueprint`               |
| `ui-visual-calibration` ⚠️ | vague visual taste             | density/layout/shape decisions    | `ui-blueprint`, `ui-system`             |
| `ui-flow`                 | brief for multi-screen feature | journey graph                     | `ui-blueprint`                          |
| `ui-blueprint`            | approved brief                 | layout/wireframe spec             | `ui-screen-spec`, `ui-system`           |
| `ui-system`               | brand/visual direction         | tokens and design rules           | `ui-component-spec`, `ui-generate-code` |
| `ui-screen-spec`          | blueprint + system             | screen contract                   | `ui-component-spec`                     |
| `ui-component-spec`       | screen/component context       | anatomy/state/a11y spec           | `ui-acceptance`, `ui-generate-code`     |
| `ui-microcopy`            | brief/spec                     | approved copy                     | `ui-acceptance`, `ui-generate-code`     |
| `ui-acceptance`           | approved specs                 | testable checklist                | `ui-redline`                            |
| `ui-spec-linter` ⚠️        | full spec package              | completeness + consistency report | `ui-generate-code`                      |
| `ui-generate-code`        | approved specs                 | implementation                    | `ui-inspector`, `ui-redline`            |
| `ui-inspector` ⚠️          | live implementation            | DOM/a11y evidence report          | `ui-redline`                            |
| `ui-redline`              | spec + implementation          | mismatch report + refactor prompt | code refactor                           |
| `ui-storybook-docs` ⚠️     | component spec                 | MDX docs, stories, prop tables    | —                                       |
| `ui-orchestrator` ⚠️       | current project state          | recommended next skill to run     | any skill                               |

> ⚠️ = currently a **draft** skill — the core behaviour is defined but some implementation details are still being validated.

## Contributing
See [CONTRIBUTING.md](./CONTRIBUTING.md) for how to add or improve skills.

## License
MIT License. See [LICENSE](./LICENSE) for more details.
