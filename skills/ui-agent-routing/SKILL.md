---
name: ui-agent-routing
description: Use when a UI spec package is complete or recovered and AI coding agents need to find it before editing implementation code. Also use when old spec paths have been deprecated, replaced, or moved. Symptoms: agents edit UI code without consulting the spec; agents use stale docs; multiple spec folders exist for the same route.
status: stable
---

# UI Agent Routing

A skill for wiring completed UI spec packages into the project's AI-agent-facing routing layer so coding agents reliably discover and use the active spec before touching implementation code.

This skill does not create the spec package. It runs after a package exists and has been accepted. Its job is to update — or produce an exact plan to update — the routing files that AI coding agents consult when starting work on a UI scope.

## When to use this skill

Use this skill when:
- A new or recovered UI spec package has been created and you want future agents to find it automatically.
- An old spec path has been deprecated, moved, or replaced by a recovery package.
- An agent was observed editing UI code without consulting the spec.
- CLAUDE.md, AGENTS.md, GEMINI.md, `.cursor/rules`, or `llm-docs/` do not yet point to the active spec package.
- `ui-docs-sync` identified missing links between repo docs and a spec package, and you are now applying those fixes.

Do **not** use this skill when:
- No spec package exists yet. Create one first.
- You only need a consistency report. Use `ui-docs-sync` for that.
- You need to validate the spec internally. Use `ui-spec-linter`.
- You need to compare the implementation against the spec. Use `ui-redline`.

## Core principle

**A spec package is only useful to agents if the routing layer points to it.** A perfectly written spec that no agent finds is passive documentation. This skill makes it operational.

## What counts as an agent-facing routing file

Search for all of these, in priority order:

| File | Agent served |
|---|---|
| `CLAUDE.md` | Claude Code |
| `AGENTS.md` | Generic AI coding agents |
| `GEMINI.md` | Gemini CLI |
| `.cursor/rules` | Cursor |
| `.github/copilot-instructions.md` | GitHub Copilot |
| `llm-docs/*.md` | Model-facing product/route contracts |
| `docs/routes.md`, route maps | Any agent reading route documentation |
| Per-directory `CONTEXT.md` or `folder_context.md` | Agents browsing source trees |

Do not assume only CLAUDE.md and AGENTS.md exist. Check all of them.

Also check for **per-directory** variants of these files alongside the root-level ones. For example, a `src/pages/create/CLAUDE.md` or `src/components/AGENTS.md` may exist and take precedence over root-level files for agents browsing those directories.

## Modes

This skill produces one of two outputs depending on context:

| Mode | When to use | Output |
|---|---|---|
| **Report** | Agent cannot or should not apply edits (read-only session, needs human review) | Markdown routing report + exact edit plan |
| **Patch** | Agent has write access and user has approved applying edits | Applies edits directly using section markers + produces a routing report |

Default to **Report** mode unless the user explicitly says to apply the edits.

### Patch mode rules
When running in Patch mode, use **bounded section markers** to ensure edits are surgical and do not disrupt other repository instructions:

```md
<!-- interface-skills:start -->
## Interface Skills routing

[Routing entries go here]
<!-- interface-skills:end -->
```

1. **If marker block exists:** Replace the entire block (including markers) with the updated routing content.
2. **If marker block does not exist:** Append the block to the end of the file.
3. **Preservation:** Never rewrite or delete content outside the markers. Never delete other tool-specific instruction blocks.

## Workflow

### Step 1 — Locate the active spec package

Read `00-index.md` from the spec package. Extract:

| Field | Where to read |
|---|---|
| Scope / route | Frontmatter `spec_id` or package directory name |
| Package path | Absolute path to directory containing `00-index.md` |
| Status | Frontmatter `status` |
| Recovery flag | Frontmatter `recovery: true` if present |
| Deprecated paths | Any "Supersedes" or "Replaces" notes in the index |
| Required read order | Contents table — ordered list of spec files |

If `00-index.md` does not have a "How agents find this package" section, that is a gap to fill in Step 5.

---

### Step 2 — Find all agent-facing routing files

Scan the repository for every file in the table above. For each file found, read it and record:

1. Does it mention the route or scope at all?
2. Does it link or name the active spec package path?
3. Does it link or name any deprecated or old spec path?

Do not stop at CLAUDE.md and AGENTS.md. Agents on other platforms will miss the spec if only two files are updated.

---

### Step 3 — Map the required routing chain

Define the chain from agent entry to required spec artifact:

```
<agent entry file (e.g. CLAUDE.md)>
→ <contract or route-map file (e.g. llm-docs/ROUTE-CONTRACT.md)>
→ <active spec package index (00-index.md)>
→ <first required spec artifact (e.g. brief.md, screen-spec.md)>
```

If a contract file does not exist, the chain goes directly from agent entry to spec index. Record the chain even if links are missing — the gaps are the findings.

---

### Step 4 — Add discovery rules to routing files

For each agent-facing file that does not yet reference the active spec, write a routing entry. The exact phrasing adapts to the file's existing conventions, but every entry must:

1. Name the route or UI scope explicitly.
2. Give the absolute path to the active spec package index.
3. Label any deprecated or old spec path as deprecated.
4. List what the agent must read before editing implementation code.

**Example entry (adapt to file conventions):**

```markdown
## /create — Content Creation Route

Spec package: `docs/saas-frontend/specs/create/00-index.md`

Before editing any code under `src/pages/create/` or `src/components/create/`, read:
1. `docs/saas-frontend/specs/create/brief.md` — goals, constraints, non-goals
2. `docs/saas-frontend/specs/create/screen-spec.md` — regions, states, behaviour
3. `docs/saas-frontend/specs/create/acceptance.md` — done criteria

Deprecated: `docs/saas-frontend/specs/content-journey/create/` — superseded by the recovery package above. Do not use.
```

---

### Step 5 — Add a discovery section to `00-index.md`

---

## Status Field Requirements

When reporting on routing readiness, use explicit statuses instead of checkboxes:

```yaml
done       # Link is present and correct
missing    # Link should exist but does not
planned    # Link is acknowledged but not yet added
not_applicable  # This file does not apply to this spec package
```

**Example report format:**

| Routing File | Route | Status | Notes |
|---|---|---|---|
| `CLAUDE.md` | `/admin/*` | done | Link added to admin-nav spec |
| `metamorfose-platform/AGENTS.md` | `/admin/*` | missing | App-level AGENTS.md needs update |
| `root CONTEXT.md` | `/admin/*` | planned | Will be added after platform-level routing is confirmed |
| `.cursor/rules` | `/admin/*` | not_applicable | No Cursor setup for this repo |

This prevents ambiguity where "planned" might look like "complete" in a checkbox view

Every spec package should explain its own discovery path so agents that land on the index first can orient themselves. Add or update this section in `00-index.md`.

Also add a machine-readable field to the frontmatter:
```yaml
agent_routing: wired | partial | missing | not_required
```

The markdown section should follow this format:

```markdown
## How agents find this package

This package is the active source of truth for `<scope>`.

**Agent entry points that route here:**
- `CLAUDE.md` — see §<section name>
- `AGENTS.md` — see §<section name>
- `GEMINI.md` — see §<section name>
- `.github/copilot-instructions.md` — see §<section name>
- `<folder_context.md or llm-docs file>`

**Before editing this UI, agents must read:**
1. `00-index.md` (this file)
2. `brief.md`
3. `screen-spec.md`
4. `acceptance.md`
5. `redlines/inspector-report.md` if modifying areas flagged in the redline report

**Deprecated or redirected paths:**
- `<old path>` → use `<new path>` (reason: <e.g. spec recovery consolidated this folder>)
```

---

### Step 6 — Deprecate old spec paths

Do not delete old spec folders. Instead, create a `DEPRECATED.md` at the root of each deprecated folder:

```markdown
# Deprecated

This spec path is deprecated as of <YYYY-MM-DD>.

**Use instead:** `<active package path>/00-index.md`

**Reason:** <e.g. The /create specification was recovered and consolidated into the active package.>

Do not use any files in this folder as a source of truth.
```

This prevents agents browsing the file tree from treating old folders as equally valid.

---

### Step 7 — Check for references to deprecated paths

Run a repository-wide search for the deprecated path string. Every occurrence in a non-deprecated file is a stale pointer that needs updating. Update each one or flag it in the report.

---

### Step 8 — Verify the routing chain end-to-end

The chain must be traversable without gaps:

```
Agent entry file → (optional) contract file → active spec index → required spec artifact
```

**Pass conditions:**
- [ ] At least one agent-facing routing file names the active spec package path.
- [ ] No agent-facing routing file names only the deprecated path (without a redirect).
- [ ] `00-index.md` has a "How agents find this package" section.
- [ ] All deprecated folders have `DEPRECATED.md` redirect notices.
- [ ] No unresolved references to deprecated paths in non-deprecated files.

If any pass condition is not met, the result is FAIL.

---

## Output template

Produce the routing report in this structure. In Patch mode, note which edits were applied vs. which were only planned.

```markdown
---
spec_type: agent-routing-report
scope: <route or feature name>
spec_package: <path to 00-index.md>
agent_routing: wired | partial | missing | not_required
created: <YYYY-MM-DD>
status: draft
mode: report | patch
---

# UI Agent Routing Report: <scope>

## 1. Active spec package

| Field | Value |
|---|---|
| Scope | <scope> |
| Route | <route> |
| Active package | `<directory path>` |
| Index | `<path>/00-index.md` |
| Package status | <draft/current/approved/complete> |
| Recovery | Yes / No |

---

## 2. Agent routing files checked

| File | Exists? | References active spec? | References deprecated path? | Action required |
|---|---|---|---|---|
| `CLAUDE.md` | Yes | No | No | Add routing entry |
| `AGENTS.md` | Yes | No | No | Add routing entry |
| `GEMINI.md` | No | — | — | None (file absent) |
| `.cursor/rules` | No | — | — | None (file absent) |
| `.github/copilot-instructions.md` | No | — | — | None (file absent) |
| `llm-docs/ROUTE-CONTRACT.md` | Yes | No | Yes — old path only | Update to active path |

---

## 3. Routing chain

```text
CLAUDE.md
→ llm-docs/ROUTE-CONTRACT.md
→ docs/saas-frontend/specs/create/00-index.md
→ brief.md / screen-spec.md / acceptance.md
```

**Gaps:**
- CLAUDE.md does not yet reference the spec package. (FAIL)
- llm-docs/ROUTE-CONTRACT.md references the deprecated path only. (FAIL)

---

## 4. Deprecated paths

| Old path | Active replacement | Action |
|---|---|---|
| `docs/saas-frontend/specs/content-journey/create/` | `docs/saas-frontend/specs/create/` | Create DEPRECATED.md |

---

## 5. References to deprecated paths

| File | Line / section | Deprecated path found | Action |
|---|---|---|---|
| `llm-docs/ROUTE-CONTRACT.md` | §Create | `specs/content-journey/create/` | Update to active path |

---

## 6. Edits applied / recommended

List in priority order (highest-leverage first):

1. **[Applied / Recommended]** Create `docs/saas-frontend/specs/content-journey/create/DEPRECATED.md` with redirect notice.
2. **[Applied / Recommended]** Add `/create` routing entry to `CLAUDE.md` (path, required reads, deprecated warning).
3. **[Applied / Recommended]** Add `/create` routing entry to `AGENTS.md`.
4. **[Applied / Recommended]** Update `llm-docs/ROUTE-CONTRACT.md` §Create to reference active package path.
5. **[Applied / Recommended]** Add "How agents find this package" section to `docs/saas-frontend/specs/create/00-index.md`.

---

## 7. Verification

- [ ] At least one agent-facing routing file names the active spec package path.
- [ ] No agent-facing routing file names only the deprecated path without a redirect.
- [ ] `00-index.md` has a "How agents find this package" section.
- [ ] All deprecated folders contain `DEPRECATED.md` redirect notices.
- [ ] No unresolved references to deprecated paths in non-deprecated files.

## 8. Result

**PASS / FAIL** — (<N> items remain unresolved)
```

---

## How `ui-agent-routing` differs from adjacent skills

| Skill | What it does |
|---|---|
| `ui-docs-sync` | Reports whether repo docs and spec packages are consistent (read-only) |
| `ui-agent-routing` | Wires routing files so agents discover the active spec (applies or plans edits) |
| `ui-spec-linter` | Validates the spec package internally |
| `ui-redline` | Compares the implementation against the spec |
| `ui-orchestrator` | Recommends which skill to run next |

The clearest distinction: `ui-docs-sync` asks "do they agree?"; `ui-agent-routing` asks "will an agent find it?"

---

## Anti-pattern rules

1. **Do not assume only CLAUDE.md and AGENTS.md exist.** Check all agent-facing file types in the table. An agent on Cursor or Copilot will miss the spec if `.cursor/rules` and `copilot-instructions.md` are not updated.
2. **Do not delete deprecated spec folders.** Create `DEPRECATED.md` inside them. Deletion removes git history and may break external links.
3. **Do not silently redirect.** Every routing file that previously pointed to the old path must explicitly state why it now points elsewhere. Silent re-pointers confuse agents that read both old and new locations.
4. **Do not skip Step 5.** `00-index.md` is often the first file an agent lands on when navigating the spec directory. If it does not explain how agents should find it, the routing chain has a self-referential gap.
5. **Do not mark result as PASS if any verification item is unchecked.** Partial routing means some agents will still miss the spec.
6. **The stale-reference search (Step 7) is string-based.** It will miss references expressed as relative links, symlinks, or path aliases that resolve to the deprecated location. If the project uses symlinks or import path remapping, check those manually and note the gap in "What was not checked."

---

## Acceptance criteria for this skill's output

A routing report or patch produced by this skill is acceptable only if:

- [ ] The active spec package path is identified and confirmed to exist.
- [ ] All agent-facing routing file types were searched for (not just CLAUDE.md and AGENTS.md).
- [ ] The routing chain is shown end-to-end, with gaps named explicitly.
- [ ] `00-index.md` has or receives a "How agents find this package" section.
- [ ] All deprecated spec paths are identified and have `DEPRECATED.md` redirect notices or are flagged for them.
- [ ] All references to deprecated paths in non-deprecated files are identified.
- [ ] In Patch mode: the report distinguishes edits applied from edits recommended.
- [ ] The result is PASS only when all five verification items are satisfied.

---

## Promotion checklist

### Evidence on the spec-recovery-create fixture

- [x] Running this skill against `examples/spec-recovery-create/` produces a routing report that satisfies all acceptance criteria.
- [x] The report identifies the missing "How agents find this package" section in `00-index.md` and adds or plans it.
- [x] The report includes a `DEPRECATED.md` for any deprecated path mentioned in the example.
- [x] The routing chain is shown even if it is short (spec index → required artifact only, since the example has no CLAUDE.md/AGENTS.md).

### Skill integration

- [x] `validate-skill.py` passes with `status: stable`.
- [x] `skills.json` entry is updated to `"status": "stable"`.
- [x] README core workflow and retrospective workflow end with `ui-agent-routing` after `ui-docs-sync`.
- [x] README Skill Map table has been updated to show `ui-agent-routing`.
