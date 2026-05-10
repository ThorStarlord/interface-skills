# Interface Skills

> **Visual contracts for AI-built interfaces.**

Reusable AI skills for turning fuzzy UI intent into precise, testable interface specifications.

Interface Skills is a collection of skills for designing, documenting, generating, and diagnosing user interfaces with AI. It helps transform vague requests like “make this dashboard cleaner” into structured briefs, visual calibration sheets, screen blueprints, design tokens, component specs, acceptance criteria, implementation plans, and redline audits.

The goal is simple: reduce the gap between the interface you imagine and the interface an AI model builds.

## Core workflow

```text
surface inventory → brief → visual calibration → flow → blueprint → system → screen spec → component spec → microcopy → acceptance → lint → code → inspection → redline → docs sync → agent routing
```

> `surface inventory` is only needed when the scope is ambiguous or an existing app is being documented. For brand-new, well-scoped features start at `brief`.

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

### Option C: Individual Skill ZIPs
For platforms that require single skills (e.g. ChatGPT builder), you can package any folder as a self-contained ZIP using `scripts/package-skill.py`.

### Option D: Claude Code (Recommended)
Claude Code can use these skills globally or per-project. Use the installer script to ensure all shared references are bundled correctly:

```bash
# Install globally for all projects
python scripts/install-claude-code-skill.py skills/ui-brief --scope global

# Install for the current project only
python scripts/install-claude-code-skill.py skills/ui-brief --scope project
```

See [Claude Code Installation Guide](./docs/claude-code-installation.md) for full details.

### Option E: Universal agent export (`.agents/skills`)

For agents that support the shared `.agents/skills` directory convention, use the universal installer. This is a **local export/install path** — it is not a published `skills.sh` registry integration.

```bash
# Install one or more skills into the current project
python scripts/install-agent-skills.py skills/ui-orchestrator skills/ui-brief --scope project

# Install globally for all supported agents on this machine
python scripts/install-agent-skills.py skills/ui-orchestrator skills/ui-brief --scope global

# Re-install over an existing installation
python scripts/install-agent-skills.py skills/ui-brief --scope global --force

# Use symlinks to track live repo changes (local development only)
python scripts/install-agent-skills.py skills/ui-brief --scope global --mode symlink
```

**`copy` mode** (default) produces a self-contained skill folder: shared references are bundled and repo-internal metadata is stripped. This is the safe default for all platforms.

**`symlink` mode** is for local skill development only. It points directly at this repository and does not bundle references. Symlinks require Developer Mode or Administrator privileges on Windows — if creation fails, the script exits with a clear error. Use `copy` mode when in doubt.

By default the installer skips a skill if the target folder already exists. Pass `--force` to overwrite.

### Distribution support matrix

| Install mode        | Script                              | Target               | Best for                          |
| ------------------- | ----------------------------------- | -------------------- | --------------------------------- |
| ZIP package         | `scripts/package-skill.py`          | ChatGPT Skill upload | single-skill import to ChatGPT    |
| Claude Code         | `scripts/install-claude-code-skill.py` | `.claude/skills`  | Claude Code (global or project)   |
| Universal agents    | `scripts/install-agent-skills.py`   | `.agents/skills`     | multi-agent local workflows       |
| skills.sh registry  | not yet                             | —                    | future public distribution        |

All three active install methods use the same bundling logic: shared references are inlined and `status` is stripped before export.

### Minimum viable workflow
For small, well-scoped features where visual tone is already agreed:
1. Run `ui-brief`
2. Run `ui-blueprint`
3. Run `ui-component-spec`
4. Run `ui-acceptance`
5. Run `ui-generate-code`
6. Run `ui-inspector`
7. Run `ui-redline`

> For very small one-off changes, `ui-redline` can accept a screenshot or code snippet directly without a full inspector run. For any audit you intend to act on, run `ui-inspector` first — it replaces opinion with measured evidence.

### Full documentation-first workflow
For new products, unfamiliar domains, or any work where misalignment is expensive:
1. Run `ui-brief`
2. Run `ui-visual-calibration`
3. Run `ui-flow` *(multi-screen features only)*
4. Run `ui-blueprint`
5. Run `ui-system`
6. Run `ui-screen-spec`
7. Run `ui-component-spec`
8. Run `ui-microcopy`
9. Run `ui-acceptance`
10. Run `ui-spec-linter`
11. Run `ui-generate-code`
12. Run `ui-inspector`
13. Run `ui-redline`
14. Run `ui-docs-sync` *(after creating or updating a spec package, to keep repo docs in sync)*
15. Run `ui-agent-routing` *(after docs sync, to wire the spec into agent-facing routing files so AI agents discover it automatically)*

### Retrospective specification workflow
Use this when a UI already exists but no specification was created first ("Spec Recovery").

1. Run `ui-surface-inventory` to map the existing UI into coherent, recoverable scopes.
2. Run `ui-inspector` on each scope's existing implementation.
3. Run `ui-brief` to reconstruct the missing product and design intent.
4. Run `ui-visual-calibration` to name the existing visual language.
5. Run `ui-blueprint` to document the as-built layout.
6. Run `ui-screen-spec` to map regions, components, data, and states.
7. Run `ui-component-spec` for each non-trivial component.
8. Run `ui-microcopy` to extract and approve existing UI text.
9. Run `ui-acceptance` to create the target checklist.
10. Run `ui-spec-linter` to check the recovered spec package.
11. Optionally run `ui-redline` to compare the existing UI against the recovered target spec.
12. Run `ui-docs-sync` to confirm repository docs reference and agree with the recovered spec package.
13. Run `ui-agent-routing` to wire the recovered package into CLAUDE.md, AGENTS.md, and other agent-facing routing files; create `DEPRECATED.md` redirects in superseded spec folders.

> Steps 3–13 are repeated for each scope identified in step 1.

## Skill Map

| Skill                     | Input                          | Output                            | Next                                    |
| ------------------------- | ------------------------------ | --------------------------------- | --------------------------------------- |
| `ui-surface-inventory` ⚠️ | existing app or ambiguous scope | UI scope map + recovery order    | `ui-brief`, `ui-inspector`              |
| `ui-brief`                | vague UI idea                  | product/design brief              | `ui-flow`, `ui-blueprint`               |
| `ui-visual-calibration` ⚠️ | vague visual taste             | density/layout/shape decisions    | `ui-blueprint`, `ui-system`             |
| `ui-flow`                 | brief for multi-screen feature | journey graph                     | `ui-blueprint`                          |
| `ui-blueprint`            | approved brief                 | layout/wireframe spec             | `ui-screen-spec`, `ui-system`           |
| `ui-system`               | brand/visual direction         | tokens and design rules           | `ui-component-spec`, `ui-generate-code` |
| `ui-screen-spec` ⚠️        | blueprint + system             | screen contract                   | `ui-component-spec`                     |
| `ui-component-spec`       | screen/component context       | anatomy/state/a11y spec           | `ui-acceptance`, `ui-generate-code`     |
| `ui-microcopy`            | brief/spec                     | approved copy                     | `ui-acceptance`, `ui-generate-code`     |
| `ui-acceptance`           | approved specs                 | testable checklist                | `ui-redline`                            |
| `ui-spec-linter` ⚠️        | full spec package              | completeness + consistency report | `ui-generate-code`                      |
| `ui-generate-code`        | approved specs                 | implementation                    | `ui-inspector`, `ui-redline`            |
| `ui-inspector` ⚠️          | live or static implementation  | DOM/a11y evidence report          | `ui-redline`                            |
| `ui-redline`              | spec + implementation          | mismatch report + refactor prompt | code refactor                           |
| `ui-docs-sync`            | repo docs + spec packages      | link and consistency report       | `ui-agent-routing`                      |
| `ui-agent-routing`        | accepted spec + routing files  | routing patches + routing report  | —                                       |
| `ui-storybook-docs` ⚠️     | component spec                 | MDX docs, stories, prop tables    | —                                       |
| `ui-orchestrator` ⚠️       | current project state          | recommended next skill to run     | any skill                               |

> ⚠️ = currently a **draft** skill — the core behaviour is defined but some implementation details are still being validated.

## Contributing
See [CONTRIBUTING.md](./CONTRIBUTING.md) for how to add or improve skills.

## License
MIT License. See [LICENSE](./LICENSE) for more details.
