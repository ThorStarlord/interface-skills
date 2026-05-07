# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed
- `ui-brief` — output save instruction updated to canonical spec-package filename (`brief.md` inside feature folder) instead of `brief-<slug>.md`.
- `ui-inspector` — output save path updated to `redlines/inspector-report.md` to match canonical spec-package layout.
- `ui-orchestrator` — routing table updated to canonical filenames; split the two-skill `ui-inspector → ui-redline` row into two separate rows, preserving the one-gap-one-skill rule.
- `ui-screen-spec` — rewritten from a 33-line stub to a full first-class skill with when-to-use, pre-flight check, workflow, output template, examples, anti-patterns, and acceptance criteria.
- `ui-redline` — updated to explicitly consume `redlines/inspector-report.md` as primary evidence.
- `ui-generate-code` — updated to recommend `ui-spec-linter` as a preferred gate before code generation.
- `README.md` — "Recommended First Workflow" renamed to "Minimum viable workflow"; added "Full documentation-first workflow" showing all 13 steps.
- `CONTRIBUTING.md` — added "Frontmatter compatibility" note explaining that `status` is a repo-internal key; added a "Public Safety & Privacy" note.
- `openai.yaml` — propagated richer `interface` metadata (display name, short description) to all skills.

### Added
- `scripts/package-skill.py` — utility script to package skills for distribution; now bundles shared references, uses local paths in `SKILL.md`, returns proper exit codes, and future-proofs by preserving all skill-local resources.
- `SECURITY.md` — added public safety and privacy guidelines; updated contact info to GitHub Security Advisories.
- `README.md` — added "Packaging a skill" usage instructions; added "Retrospective specification" (Spec Recovery) workflow.
- `.github/workflows/validate.yml` — added packaging smoke test to CI.
- `CONTRIBUTING.md` — added guidelines for Spec Recovery and the "Observed vs Target" protocol.
- `ui-brief`, `ui-blueprint`, `ui-screen-spec` — updated to explicitly support Spec Recovery with the Observed vs Target pattern.

---

## [0.1.0] - 2026-05-01

Initial public release of the Interface Skills toolkit.

### Added

**Skills (15 total)**

Nine stable skills covering the core UI specification workflow:
- `ui-brief` — converts a vague UI idea into a structured, constraint-based product and design brief.
- `ui-flow` — produces a user journey graph for multi-screen features from an approved brief.
- `ui-blueprint` — generates a layout and wireframe spec from an approved brief.
- `ui-system` — defines a design token set (colors, spacing, typography) from brand and visual direction.
- `ui-component-spec` — documents component anatomy, state matrix, keyboard map, and accessibility spec.
- `ui-microcopy` — produces approved copy for all UI text (labels, errors, empty states, toasts).
- `ui-acceptance` — converts an approved spec into a testable implementation checklist with severity levels and A/M tags.
- `ui-redline` — audits an implementation against its spec and produces a mismatch report with refactor prompts.
- `ui-generate-code` — produces implementation code from an approved spec package.

Six additional skills in draft (output format may change between versions):
- `ui-visual-calibration` — translates vague visual taste words ("clean", "modern") into concrete layout, density, and shape decisions.
- `ui-screen-spec` — produces a screen-level contract from a blueprint and system spec.
- `ui-spec-linter` — checks a full spec package for completeness and cross-spec consistency.
- `ui-inspector` — generates a DOM and accessibility evidence report from a live implementation.
- `ui-storybook-docs` — generates MDX documentation, stories, and prop tables from a component spec.
- `ui-orchestrator` — recommends the next skill to run given the current state of a spec package.

**Shared references (8 files)**

Cross-cutting reference documents used by multiple skills:
- `shared/references/visual-vocabulary.md` — canonical list of layout archetypes, density levels, shape language, and surface styles.
- `shared/references/state-taxonomy.md` — standardised names for UI states (default, hover, focus, error, disabled, loading, empty, success).
- `shared/references/vague-language-translator.md` — banned vague adjectives and their concrete translation questions.
- `shared/references/token-schema.md` — the token naming schema (`color.*`, `space.*`, `type.*`) that all skills and system specs must follow.
- `shared/references/severity-scale.md` — definitions for the four acceptance severity levels (blocker, major, minor, polish) and their mapping to common bug-tracker priorities.
- `shared/references/accessibility-baseline.md` — WCAG AA requirements and keyboard interaction defaults applied across all component specs.
- `shared/references/responsive-patterns.md` — standard breakpoint names and reflow verb vocabulary (stack, collapse, hide, move, resize, swap).
- `shared/references/spec-package-format.md` — the canonical definition of a spec package: which files are required, their names, and their order of creation.

**Examples**

- `examples/settings-page/` — a complete spec package demonstrating every skill output for a settings page. Includes: `brief.md`, `visual-calibration.md`, `flow.md`, `blueprint.md`, `system.md`, `screen-spec.md`, `microcopy.md`, `acceptance.md`, `manifest.md`, and `component-specs/profile-form.md`.

**Templates**

- `templates/spec-package/` — a blank spec package directory with a README explaining the quick-start workflow and canonical file names.

**CI / validation**

- `scripts/validate-skill.py` — validates every skill in `skills/` for: presence of `SKILL.md`, valid YAML frontmatter, `name` matching the folder name, non-empty `description` ≥20 characters, presence of `agents/openai.yaml`, absence of unresolved `TODO` markers in stable skills, and existence of any `shared/references/` files explicitly cited in the skill. Also validates that no file in `shared/references/` contains an unresolved `TODO (Human Review Required)` marker.
- `.github/workflows/validate.yml` — GitHub Actions workflow that runs `validate-skill.py` on every push and pull request to `main`.

**Documentation**

- `README.md` — project overview, core workflow diagram, skill map table with draft/stable status indicators, installation options, and contributing pointer.
- `CONTRIBUTING.md` — guide covering skill status definitions, how to write a new skill, how to resolve draft TODO sections, how to test a skill, PR requirements, and shared reference update rules.
- `LICENSE` — MIT license.
