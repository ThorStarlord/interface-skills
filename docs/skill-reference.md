# Skill Reference

Detailed technical reference for all Interface Skills, including their inputs, outputs, and recommended next steps in the workflow.

| Skill                     | Input                          | Output                            | Next                                    |
| ------------------------- | ------------------------------ | --------------------------------- | --------------------------------------- |
| `ui-surface-inventory`  ⚠️  | existing app or ambiguous scope | UI scope map + recovery order    | `ui-brief`, `ui-inspector`              |
| `ui-brief`                | vague UI idea                  | product/design brief              | `ui-flow`, `ui-blueprint`               |
| `ui-visual-calibration`  ⚠️  | vague visual taste             | density/layout/shape decisions    | `ui-blueprint`, `ui-system`             |
| `ui-flow`                 | brief for multi-screen feature | journey graph                     | `ui-blueprint`                          |
| `ui-blueprint`            | approved brief                 | layout/wireframe spec             | `ui-screen-spec`, `ui-system`           |
| `ui-system`               | brand/visual direction         | tokens and design rules           | `ui-component-spec`, `ui-generate-code` |
| `ui-screen-spec`  ⚠️         | blueprint + system             | screen contract                   | `ui-component-spec`                     |
| `ui-component-spec`       | screen/component context       | anatomy/state/a11y spec           | `ui-acceptance`, `ui-generate-code`     |
| `ui-microcopy`            | brief/spec                     | approved copy                     | `ui-acceptance`, `ui-generate-code`     |
| `ui-acceptance`           | approved specs                 | testable checklist                | `ui-redline`                            |
| `ui-spec-linter`  ⚠️         | full spec package              | completeness + consistency report | `ui-generate-code`                      |
| `ui-generate-code`        | approved specs                 | implementation                    | `ui-inspector`, `ui-redline`            |
| `ui-inspector`  ⚠️           | live or static implementation  | DOM/a11y evidence report          | `ui-redline`                            |
| `ui-redline`              | spec + implementation          | mismatch report + refactor prompt | code refactor                           |
| `ui-docs-sync`            | repo docs + spec packages      | link and consistency report       | `ui-agent-routing`                      |
| `ui-agent-routing`        | accepted spec + routing files  | routing patches + routing report  | —                                       |
| `setup-interface-skills`  ⚠️  | new or existing repository     | INTERFACE_SKILLS.md + folders     | `ui-surface-inventory`, `ui-brief`      |
| `ui-spec-reconcile`  ⚠️       | spec package + redline/code    | updated spec package + report     | `ui-to-issues`, `ui-docs-sync`          |
| `ui-to-issues`  ⚠️            | spec / redline / acceptance    | markdown issue drafts             | `ui-generate-code`                      |
| `ui-storybook-docs`  ⚠️     | component spec                 | MDX docs, stories, prop tables    | —                                       |
| `ui-orchestrator`  ⚠️       | current project state          | recommended next skill to run     | any skill                               |

>  ⚠️ = currently a **draft** skill — the core behaviour is defined but some implementation details are still being validated.
