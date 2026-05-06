# Integrations

How to use Interface Skills with specific AI tools.

## 1. Claude Code (primary integration)

Claude Code has file access, which makes it the most natural fit for this toolkit.

**Basic setup:**

Copy the contents of the relevant `SKILL.md` into your conversation context, or reference the file path directly:

```
Please read skills/ui-brief/SKILL.md and then run the skill against my input.
```

Claude Code can also read your spec package files directly. If you have a `specs/settings-page/brief.md`, you can reference it by path and Claude will read it as context for the next skill.

**Workflow tips:**

- Run one skill per session. Each skill is designed as a focused task with a specific input and output. Stacking multiple skills in a single context ("run brief, then blueprint, then component spec") produces worse results than running them in separate sessions because the model has to track multiple conflicting workflows simultaneously.
- Follow the recommended workflow order from `README.md`. Skills reference each other's outputs — a blueprint that can't reference an approved brief will produce weaker output.
- After each skill run, save the output as a markdown file in your spec package directory before starting the next session. The output is only in context for the current session. If you don't save it, it's gone.

**Referencing spec files in a session:**

At the start of a new session, reference the relevant spec files explicitly:

```
I'm about to run ui-component-spec. The brief is at specs/settings-page/brief.md
and the blueprint is at specs/settings-page/blueprint.md. Please read both files
before we start.
```

This reconstructs the context the model needs without you having to re-explain decisions made in earlier sessions.

## 2. ChatGPT / Custom GPTs

Each skill folder includes an `agents/openai.yaml` file with metadata for creating a Custom GPT.

**Creating a Custom GPT for a skill:**

1. Open the ChatGPT GPT editor (chat.openai.com → Explore GPTs → Create).
2. Set the GPT name to the skill name (e.g. `ui-brief`).
3. Paste the full contents of `SKILL.md` into the **Instructions** field.
4. Set the description from the `description` field in `agents/openai.yaml`.
5. Save the GPT.

The skill will then run as a specialized GPT that enforces the workflow steps and output template.

**Limitations:**

ChatGPT does not have access to your local file system. Output must be copied out of the chat manually and saved as a markdown file. There is no automatic way to pass the output of one skill session directly into the next.

**Recommended setup for multi-session work:**

Use ChatGPT Projects to keep spec files accessible across conversations. Create a project for each feature, upload your spec files as attachments, and reference them at the start of each session. This is a manual equivalent of the Claude Code file-referencing workflow.

## 3. Cursor / Windsurf / Copilot (file-aware editors)

File-aware editors can read spec files directly, which makes the spec package pattern work well. The setup is slightly different because these editors use rule files or system prompt injections rather than direct skill invocation.

**Cursor setup:**

1. Copy the contents of the relevant `SKILL.md` into a `.cursorrules` file at your project root (or a project-level `.cursor/rules/` file if you're using Cursor's newer rules system).
2. Put your spec package in a `specs/` directory at your project root.
3. Reference spec files in your prompt: `Using the brief in specs/settings-page/brief.md, run ui-blueprint and produce output as specs/settings-page/blueprint.md`.

**Windsurf setup:**

Same approach. Paste the skill content into the project-level system prompt or a `.windsurfrules` file.

**Copilot setup:**

Use a `.github/copilot-instructions.md` file or paste the skill instructions as a comment at the top of your chat session.

**Limitations:**

In-editor AI tools have shorter effective context windows than dedicated AI assistants. Keep the skill instructions lean: paste only the workflow steps, output template, and anti-patterns — skip the examples and detailed explanations if the context window is a constraint. The output template and anti-patterns are the highest-priority sections to include.

**Best setup:**

Put your spec package in a `specs/[feature-name]/` directory and reference it in the rule file. The editor can then read brief.md, blueprint.md, and component specs directly when generating code. This is the closest approximation of automatic spec-to-code traceability in a file-aware editor.

## 4. Any other AI (generic integration)

These skills work with any model that accepts a system prompt or a long initial user message.

**Setup:**

Copy the full contents of the relevant `SKILL.md` into the system prompt field (if your interface has one), or paste it as the first message in the conversation before describing your input.

**Workflow:**

Follow the steps in the skill's Workflow section manually. After each step, check whether the model's output matches the expected structure before proceeding. If it doesn't, correct it before moving on — errors at step 2 compound into larger errors at step 5.

**Saving outputs:**

Save each skill's output as a markdown file. Name it according to the spec package format (`brief.md`, `blueprint.md`, etc.) and keep all files for one feature in the same directory. Without this discipline, each AI session starts with no context and you will repeat the same decisions in every session.

---

## Troubleshooting

**The model ignores the output template.**

The most reliable fix is to make the instruction explicit in your user message, not just in the system prompt:

```
Produce your output using exactly the template defined in the Output template
section of the skill. Do not deviate from the section headings or frontmatter fields.
```

If the model still deviates, paste the template again at the end of your message immediately before asking for output.

**The model uses banned vague language (clean, modern, intuitive, etc.).**

Invoke the vague-language-translator reference directly. Paste the relevant row from `shared/references/vague-language-translator.md` into your message and ask the model to translate the vague word before proceeding.

Example:
```
"Clean" is a banned vague word in this system. Before continuing, translate
it using this rule: "clean" usually means low information density and minimal
chrome — confirm this is what the user means, or ask for a concrete alternative.
```

**The model skips steps.**

Re-send the workflow steps as a numbered checklist and ask the model to confirm which step it is currently on:

```
The workflow has the following steps:
1. Pre-flight check — confirm inputs are present
2. Draft the output
3. Validate against acceptance criteria
4. Confirm with user

Which step are you on? Do not proceed to the next step until I confirm.
```

This forces the model to work through the workflow sequentially rather than jumping to the output it expects you want.
