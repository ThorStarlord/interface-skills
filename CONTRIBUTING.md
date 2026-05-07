# Contributing to Interface Skills

Thank you for your interest in improving the Interface Skills toolkit.

---

## Skill status: what "draft" and "stable" mean

Every skill has a `status` field in its YAML frontmatter. The two values in use are:

**`draft`**
The skill's core behaviour is defined and it produces useful output, but the output format is still being validated through real usage. A draft skill may break compatibility between versions — the template structure, section names, or frontmatter keys can change. Draft skills are suitable for experimentation and feedback but should not be depended on in a production pipeline. Draft skills may contain `TODO (Human Review Required)` sections (see below).

**`stable`**
The skill's output format is locked. The template structure and all frontmatter keys are considered a public contract — changes require a version bump and a CHANGELOG entry. Acceptance criteria are defined and passing. Stable skills are suitable for production use and for downstream skills to reference.

The validation script (`scripts/validate-skill.py`) will fail if a `TODO (Human Review Required)` marker is found in a skill whose status is `stable`.

---

## How to write a new skill

1. **Create the directory.** Under `skills/`, create a new folder named `ui-<skill-name>` using lowercase and hyphens only (e.g. `ui-redline`, `ui-screen-spec`). The folder name must match the `name` field in the SKILL.md frontmatter exactly.

2. **Create `SKILL.md`.** Copy the structure from an existing skill (e.g. `skills/ui-brief/SKILL.md`) and replace the content. The frontmatter must contain exactly three keys:
   ```yaml
   ---
   name: ui-<skill-name>
   description: <one-sentence description, at least 20 characters>
   status: draft
   ---
   ```
   New skills always start as `draft`. Do not set `status: stable` until the acceptance criteria section passes and a reviewer has confirmed the output format.

   > **Frontmatter compatibility note.** The `status` key is a repo-internal field used by `scripts/validate-skill.py` and the README skill map. It is not part of the ChatGPT Skill specification. If you intend to upload a skill directly to a platform that only accepts `name` and `description` in frontmatter, strip the `status` key before packaging. The easiest approach is to copy the `name` and `description` values from `SKILL.md` into the platform's upload form rather than uploading the file directly.

3. **Write the `## When to use this skill` section.** Include both a "Use when" list and a "Do not use when" list. Be specific about what upstream artifacts the skill requires (e.g. "requires an approved brief") and what it produces.

4. **Write the `## Workflow` section.** Number the steps. Each step should describe what the model does, what it checks, and what it produces. If a step depends on user input or confirmation, say so explicitly.

5. **Write the `## Output template` section.** Put the template inside a fenced code block. Every field the model is expected to fill must have a `<placeholder>` so it is clear what is required. If the output is a markdown document, include a YAML frontmatter block with at minimum `spec_type`, `spec_id`, `created`, and `status`.

6. **Write the `## Acceptance criteria for this skill's output` section.** This is a checklist of properties that a correct output must satisfy. Each item is a `- [ ]` checkbox. At minimum: all template sections are present, no banned vague language appears, every required field is filled. This section is what makes the skill self-validating.

7. **Create `agents/openai.yaml`.** The validation script checks for this file. Copy it from an existing skill's `agents/` directory and update the `name` and `description` fields. This file is required for the skill to pass CI.

8. **Run the validation script.**
   ```bash
   python scripts/validate-skill.py
   ```
   Fix any failures before opening a PR. The script checks: SKILL.md exists, frontmatter is valid, `name` matches the folder name, `description` is non-empty and ≥20 characters, `agents/openai.yaml` exists, and any `shared/references/` files cited in the skill actually exist.

9. **Add the skill to the README skill map.** The table in `README.md` under `## Skill Map` lists every skill with its input, output, and recommended next skill. Add a row for the new skill. If it is a draft, add `⚠️` after the name per the existing convention.

---

## How to improve a draft skill

Draft skills may contain sections marked `TODO (Human Review Required)`. This marker means a human expert needs to review that section before the skill can be promoted to stable — the content may be plausible but has not been validated against real usage.

To resolve a `TODO (Human Review Required)`:

1. Run the skill against at least one realistic test scenario (see "How to test a skill" below).
2. Compare the output against the acceptance criteria section of the skill itself.
3. If the output passes, replace the `TODO` marker with the validated content and update the section.
4. If the output fails, revise the workflow step or template that caused the failure.
5. When all `TODO` markers in a skill are resolved and the acceptance criteria pass consistently, change `status: draft` to `status: stable` in the frontmatter.

Do not remove a `TODO` marker without replacing it with real content. Deleting the marker without resolving the underlying question is not a resolution.

---

## How to test a skill

**Automated validation**

Run the validation script to check structure and formatting:
```bash
python scripts/validate-skill.py
```
This script does not check output quality — only that the files are present and the frontmatter is well-formed.

**Manual skill run**

1. Choose a realistic test scenario — a concrete UI problem the skill is designed to handle. Use the examples in the skill's own `## Examples` section if present, or pick a case from `examples/`.
2. Load the skill's `SKILL.md` into an AI model as its instruction context.
3. Provide the test scenario as input.
4. Capture the output.
5. Check the output against the skill's `## Acceptance criteria for this skill's output` checklist. Every checkbox must pass. If any fail, the skill has a gap — open an issue or fix it in a PR.

**End-to-end chain testing**

For skills that depend on upstream output (e.g. `ui-acceptance` requires a brief and blueprint), use an existing spec package under `examples/settings-page/` as the upstream input. This ensures the skill handles real, well-formed upstream documents rather than idealised inputs.

---

## PR requirements

Every pull request must include a description that covers:

1. **What changed** — which files were added or modified and why.
2. **Skill status** — if a skill status changed from `draft` to `stable`, state which acceptance criteria were validated and how (manual run, test scenario used).
3. **Validation result** — confirm `python scripts/validate-skill.py` passes. Paste the final line of output (`All skills passed validation! [SUCCESS]`).
4. **Shared reference impact** — if you modified a file under `shared/references/`, note which skills reference that file and confirm they were checked for compatibility.
5. **Breaking changes** — if any stable skill's output format changed (template structure, frontmatter keys, section names), mark the PR as a breaking change and update `CHANGELOG.md`.

---

## Updating shared references

The files under `shared/references/` are referenced by multiple skills. Changes to them can affect many skills at once.

**`shared/references/visual-vocabulary.md`**
Add to this file when you introduce a new layout archetype, density level, shape language term, or surface style that multiple skills need to agree on. Do not add one-off terms that only one skill uses — put those in the skill itself.

**`shared/references/state-taxonomy.md`**
Add to this file when you introduce a new UI state name (e.g. a new loading variant, a new error sub-type) that should be consistently named across component specs. Check whether the new state name conflicts with any existing entry before adding.

**`shared/references/vague-language-translator.md`**
Add to this file when you identify a new banned vague word and its concrete translation. The `ui-brief` skill's anti-vague vocabulary table should stay in sync with this file.

**Creating a new reference file**
Only create a new file under `shared/references/` if the content is genuinely cross-cutting — referenced by three or more skills or examples. Single-skill reference material belongs in the skill's own `SKILL.md`. When you create a new reference file, update `README.md` to mention it under the relevant section, and check whether the validation script's shared-reference checker needs to be updated to recognise the new filename.

---

## Public Safety & Privacy

Do not commit private screenshots, customer data, API keys, proprietary brand assets, or internal company docs to this repository. All examples and test data should be fictional or thoroughly sanitized.

If you discover sensitive data in the repository or its history, please report it immediately as a security concern so we can scrub the history.
