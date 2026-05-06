# Skill Authoring Guide

This guide is for developers who want to write a new skill or promote a draft skill to stable. It assumes you have read `README.md`, `CONTRIBUTING.md`, and at least one complete `SKILL.md` (e.g. `skills/ui-brief/SKILL.md`).

## Anatomy of a skill

A skill file is a single `SKILL.md` with YAML frontmatter and a set of required sections. Both the frontmatter and the sections are mandatory.

### Frontmatter

```yaml
---
name: ui-my-skill
description: >
  One or two sentences. This text appears in the ChatGPT skill description and
  in the skill map in README.md. It must answer: when should someone invoke this
  skill? Be specific — name the inputs, the outputs, and the moment in the
  workflow where it belongs.
status: draft
---
```

The `status` field is either `draft` or omitted (which implies stable). Set it to `draft` when you create a new skill. Remove it only when the skill meets the promotion criteria described at the end of this guide.

### Required sections

A complete skill must contain all of the following sections. Do not rename or remove them — downstream tools and other skills reference them by name.

**When to use this skill** — The conditions under which a model (or user) should invoke this skill. Write it as a bulleted list of triggers. Be specific enough that a model can make the decision autonomously. Also include a "Do NOT use this skill when" list, because knowing when not to invoke a skill is as important as knowing when to invoke it.

**Core principle** — One paragraph. The design philosophy behind the skill. This is the rule the model should fall back on when the workflow steps don't cover an edge case. It should be short enough to hold in working memory.

**Workflow** — Numbered steps the model follows, in order. Each step should produce a specific output or decision. Steps that require user confirmation must say so explicitly — a model should not proceed past a confirmation step without signaling back to the user.

**Output template** — The exact structure the skill must produce, as a fenced markdown block. See the section on output templates below.

**Anti-patterns** — A list of the most common failure modes for this skill. See the section on anti-patterns below.

**Acceptance criteria for this skill's output** — A checklist of verifiable claims about the output. See the section on acceptance criteria below.

## The output template

The output template is the most important part of a skill. It must be precise enough that two different AI models, given the same input, would produce outputs with identical structure — even if the content differs.

"Identical structure" means: same section headings, same nesting, same field names, same frontmatter keys.

### Too loose

```markdown
## Output

Produce a design summary with the main layout decisions and any open questions.
```

This is too loose. "Design summary" is undefined. "Main layout decisions" could be a paragraph, a table, a bulleted list, or headings — the model picks whichever it prefers. Two models will produce two incompatible formats. A downstream skill that needs to parse `layout.md` will fail half the time.

### Well-defined

```markdown
## Output template

Always produce output in this exact structure:

    ---
    spec_type: layout-summary
    spec_id: <short-slug>
    created: <YYYY-MM-DD>
    status: draft
    ---

    # Layout Summary: <descriptive title>

    ## 1. Primary layout archetype
    <single archetype name from the visual-vocabulary reference>

    ## 2. Breakpoints
    | Breakpoint | Width    | Behavior |
    |------------|----------|----------|
    | mobile     | <Npx     | <description> |
    | desktop    | >=Npx    | <description> |

    ## 3. Open layout questions
    - <numbered list; each item is a specific, answerable question>
```

This is well-defined. The frontmatter is specified. The headings are numbered and named. The breakpoints section has a required table format. Two models will produce the same structure.

When writing a template, test it by asking: if a model received this template and tried to fill it in wrong, what would go wrong? Each answer points at a place where the template needs more specificity.

## Anti-patterns section

Anti-patterns are the rules that prevent the most common failure modes. They are the distilled lessons from seeing the skill produce bad output.

To identify the top 3–5 failure modes for your skill, ask:

1. What is the most common thing a model does when it misunderstands this skill's purpose?
2. What is the most tempting shortcut a model takes when it has incomplete input?
3. What output looks correct but is actually defective?

Each failure mode becomes an anti-pattern rule. Write each rule as a declarative constraint, not a suggestion.

**Weak anti-pattern:**
> Try not to invent users that the brief doesn't mention.

**Strong anti-pattern:**
> Never introduce a user persona that the user did not name. If the user says "all users", ask who the primary user is. Do not substitute the user's vague answer with a specific persona of your own.

A strong anti-pattern names the exact thing the model must not do, and names what it must do instead.

## Acceptance criteria for the skill's own output

Acceptance criteria are the checklist a model uses to self-validate before delivering output. They are also the checklist a reviewer uses to validate a skill's output during a PR review.

Each criterion must be:

- **Testable** — A model can check it programmatically or by inspection, without needing to ask the user.
- **Binary** — Pass or fail. No partial credit. If it is not obvious whether a criterion passes, it is underspecified.
- **Scoped to the output** — Criteria about the world outside the output (e.g. "the feature is a good idea") are not acceptance criteria.

**Weak criterion:**
> The output is complete and well-organized.

**Strong criteria:**
> - [ ] All eight template sections are present with their original headings.
> - [ ] The `spec_type` frontmatter field is present and set to `layout-summary`.
> - [ ] The Breakpoints section is a markdown table with exactly three columns: Breakpoint, Width, Behavior.
> - [ ] At least one open layout question is listed.

The set of acceptance criteria defines what "done" means for this skill's output. If you cannot write at least five specific criteria, the output template is not specific enough yet.

## Testing your skill

A skill is not ready for use until it has been tested. Testing means: given a real input, does the skill produce output that passes all of its acceptance criteria?

### How to write a test scenario

A test scenario has three parts:

1. **Input** — The message a user would send to invoke the skill. Be realistic. Include the vague words, the missing context, the contradictions that real inputs contain.
2. **Expected output** — A sketch of what a correct output looks like. Not the full output — just the structural decisions the skill must make. Which sections exist, what goes in them, what is flagged as an open question.
3. **Acceptance run** — After generating output, check it against each acceptance criterion and record pass/fail.

### Example

**Skill under test:** `ui-brief`

**Input:**
> I want to build a clean modern settings page for a project management app. Users should be able to manage their account stuff.

**Expected output:**
- Skill does NOT immediately draft a brief. It identifies that "clean modern" is vague, "account stuff" is underspecified, and the primary user is unspecified.
- Skill asks: who is the primary user, what is the single most important action, what does "clean modern" mean in concrete terms, what platform.
- After receiving answers, the skill produces a brief with all 10 template sections.
- Sections 9 (Open questions) and 10 (Assumptions) are non-empty.

**Acceptance run:**
- [ ] All ten template sections present — PASS
- [ ] Goal is one sentence — check
- [ ] Primary action is one verb — check
- [ ] "Modern" and "clean" do not appear in the body without a concrete translation — check
- [ ] Every assumption flagged with ⚠️ — check

If any criterion fails, the skill's workflow or template needs to be revised to prevent that failure. Fix the skill, re-run the test, confirm it passes before considering the skill ready.

## Draft vs stable status

Promote a skill from draft to stable when all three of the following are true:

1. **The output format is locked.** The template is specific enough that structural deviations would be obvious failures. You have not needed to change the template's structure (headings, fields, required sections) after seeing real outputs.
2. **The acceptance criteria are complete.** Every criterion is testable and binary. There are no criteria that say "the output is reasonable" or "the content makes sense".
3. **The skill has been tested against at least two or three real scenarios.** Not toy inputs — real user requests with the vagueness, contradictions, and missing context that real users provide. Each scenario produced output that passed all acceptance criteria.

To promote: remove `status: draft` from the frontmatter and remove the ⚠️ from the skill's entry in `README.md`. Open a PR and include the test scenarios (inputs + acceptance run results) as evidence.
