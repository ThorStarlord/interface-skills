# Claude Code Installation Guide

Interface Skills are designed to be used as first-class citizens in Claude Code. Because some skills depend on shared reference files (like taxonomies and visual vocabularies), they must be installed as **self-contained folders** where these references are bundled locally.

## Why use the installer script?

If you manually copy a folder from `skills/` into your project, it may contain broken links to `shared/references/`. The installer script:
1.  **Bundles References:** Copies all required files from `shared/references/` into a local `references/` folder within the skill.
2.  **Strips Metadata:** Removes repo-internal frontmatter (like `status: draft`) that Claude Code doesn't need.
3.  **Future-proofs:** Copies all skill-local assets (scripts, resources) into the target directory.

## Installation Scopes

### 1. Project-local Installation
Install skills into the current repository. These skills will only be available when running Claude Code inside this project.

```bash
python scripts/install-claude-code-skill.py skills/ui-brief --scope project
```
*Target: `./.claude/skills/ui-brief/`*

### 2. Global (User) Installation
Install skills for your user account. These skills will be available from **any** repository you work in.

```bash
python scripts/install-claude-code-skill.py skills/ui-brief --scope global
```
*Target: `~/.claude/skills/ui-brief/`*

## Recommended Global Toolkit

For the best experience, we recommend installing the following core skills globally:

```bash
python scripts/install-claude-code-skill.py skills/ui-orchestrator --scope global
python scripts/install-claude-code-skill.py skills/ui-brief --scope global
python scripts/install-claude-code-skill.py skills/ui-inspector --scope global
python scripts/install-claude-code-skill.py skills/ui-redline --scope global
```

## Using Installed Skills

Once installed, Claude Code will automatically detect the skills. You can verify them using Claude Code's internal commands (e.g., `/skills` if supported by your version).

To run a skill, simply ask Claude Code to use it:
> "Run ui-orchestrator to see what I should do next."

## Manual Installation (Alternative)

If you prefer to install manually without the script, you must ensure the folder structure is self-contained:

1.  Create the target directory: `.claude/skills/ui-brief/`
2.  Copy `SKILL.md` into it.
3.  Create a `references/` folder inside it.
4.  Copy any files cited in `SKILL.md` from `shared/references/` into that `references/` folder.
5.  Update the links in `SKILL.md` to point to `references/filename.md` instead of `shared/references/filename.md`.

**Note:** The installer script automates all of these steps.
