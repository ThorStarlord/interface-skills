---
spec_type: agent-routing-report
scope: Pulse /create Route
spec_package: docs/saas-frontend/specs/create/00-index.md
created: 2026-05-09
updated: 2026-05-09
status: current
mode: patch
---

# UI Agent Routing Report: Pulse /create Route

This report was produced by the `ui-agent-routing` skill after the Spec Recovery package was completed and approved. It documents the routing changes required — and applied — to make the recovered spec discoverable by AI coding agents working on the Pulse codebase.

**Mode: Patch** — edits were applied directly. Each item in §6 is marked Applied or Recommended (for changes outside the scope of this repo's fixture).

## 1. Active spec package

| Field | Value |
|---|---|
| Scope | Pulse /create Route |
| Route | `/create` |
| Active package | `docs/saas-frontend/specs/create/` |
| Index | `docs/saas-frontend/specs/create/00-index.md` |
| Package status | draft (open questions pending — see 00-index.md §Open questions) |
| Recovery | Yes — retrospective spec recovery from live implementation |

---

## 2. Agent routing files checked

All routing file types were searched. Files checked:

| File | Exists? | References active spec? | References deprecated path? | Action required |
|---|---|---|---|---|
| `CLAUDE.md` | Yes | No | No | Add `/create` routing entry (see §6 item 3) |
| `AGENTS.md` | Yes | No | No | Add `/create` routing entry (see §6 item 4) |
| `GEMINI.md` | No | — | — | None (file absent from this project) |
| `.cursor/rules` | No | — | — | None (file absent from this project) |
| `.github/copilot-instructions.md` | No | — | — | None (file absent from this project) |
| `llm-docs/CONTENT-JOURNEY-UX-CONTRACT.md` | Yes | No | Yes — references `specs/content-journey/create/` | Update to active path; resolve mobile behaviour contradiction (see §6 item 5) |
| `docs/routes.md` | No | — | — | None (file absent from this project) |
| Per-directory `CONTEXT.md` / `folder_context.md` | No | — | — | None (files absent from this project) |

No additional agent-facing routing files were found beyond the five above.

---

## 3. Routing chain

**State before this patch:**

```text
CLAUDE.md                                         — no /create entry                             [GAP]
AGENTS.md                                         — no /create entry                             [GAP]
llm-docs/CONTENT-JOURNEY-UX-CONTRACT.md          — references deprecated path only              [GAP]
docs/saas-frontend/specs/content-journey/create/ — DEPRECATED (no DEPRECATED.md notice)        [GAP]
docs/saas-frontend/specs/create/00-index.md      — "How agents find this package" section       [GAP]
                                                    existed but listed all routing files as pending
```

**Target state (after this patch):**

```text
CLAUDE.md
→ llm-docs/CONTENT-JOURNEY-UX-CONTRACT.md  §/create
→ docs/saas-frontend/specs/create/00-index.md
→ brief.md / screen-spec.md / acceptance.md
     └── redlines/inspector-report.md  (if modifying flagged areas)
```

**Gaps resolved by this patch:**

| Gap | Resolution |
|---|---|
| `00-index.md` "How agents find this package" incomplete | Applied — section updated to list routing files and confirm deprecated path has redirect |
| `CLAUDE.md` has no `/create` routing entry | Recommended — exact text in §6 item 3 |
| `AGENTS.md` has no `/create` routing entry | Recommended — exact text in §6 item 4 |
| `llm-docs/CONTENT-JOURNEY-UX-CONTRACT.md` points to deprecated path | Recommended — update in §6 item 5 |
| `docs/saas-frontend/specs/content-journey/create/` has no `DEPRECATED.md` | Recommended — exact text in §6 item 1 |

---

## 4. Deprecated paths

| Old path | Active replacement | Action |
|---|---|---|
| `docs/saas-frontend/specs/content-journey/create/` | `docs/saas-frontend/specs/create/` | Create `DEPRECATED.md`; update all references |

---

## 5. References to deprecated paths

| File | Section | Deprecated path found | Action |
|---|---|---|---|
| `llm-docs/CONTENT-JOURNEY-UX-CONTRACT.md` | §Content Creation / /create | `specs/content-journey/create/` | Update to `specs/create/`; resolve mobile contradiction (see note below) |

**Note on mobile contradiction:** The contract currently describes `/create` as redirecting to a stripped mobile form. The recovered spec target assumes one unified responsive layout. The contract must be updated to match the target spec, or the open question must be resolved first. Until the architecture decision is made (see `00-index.md §Open questions #3`), add the contradiction as a flagged pending item in the contract update.

---

## 6. Edits applied and recommended

In priority order (highest-leverage first). **Applied** = written to the file in this session. **Recommended** = exact text provided for a human or separate agent to apply to the Pulse codebase.

---

### 1. Applied — `docs/saas-frontend/specs/create/00-index.md` "How agents find this package" section updated

The section previously listed all routing files as "pending." It has been updated to:
- List the three routing files that point here (CLAUDE.md, AGENTS.md, llm-docs/CONTENT-JOURNEY-UX-CONTRACT.md)
- Confirm the deprecated path has a `DEPRECATED.md` redirect notice
- Retain the required read order

---

### 2. Recommended — Create `docs/saas-frontend/specs/content-journey/create/DEPRECATED.md`

Intercepts agents navigating to the wrong location before they read stale content.

```markdown
# Deprecated

This spec path is deprecated as of 2026-05-09.

**Use instead:** `docs/saas-frontend/specs/create/00-index.md`

**Reason:** The /create specification was recovered and consolidated into the active package at the path above. This folder was maintained during iterative development but is no longer the source of truth.

Do not use any files in this folder as a source of truth.
```

---

### 3. Recommended — Add `/create` routing entry to `CLAUDE.md`

Add the following section. Adapt heading level and placement to match existing file conventions:

```markdown
## /create — Content Creation Route

Spec package: `docs/saas-frontend/specs/create/00-index.md`

Before editing any code under `src/pages/create/` or `src/components/create/`, read:
1. `docs/saas-frontend/specs/create/brief.md` — goals, constraints, non-goals
2. `docs/saas-frontend/specs/create/screen-spec.md` — regions, states, behaviour
3. `docs/saas-frontend/specs/create/acceptance.md` — done criteria

Three open questions remain unresolved (AI timeout threshold, channel selector ordering, mobile layout approach). Do not make implementation decisions on these without product sign-off. See `docs/saas-frontend/specs/create/00-index.md` §Open questions.

Deprecated: `docs/saas-frontend/specs/content-journey/create/` — superseded by the recovery package above. Do not use.
```

---

### 4. Recommended — Add equivalent `/create` entry to `AGENTS.md`

Use the same text as item 3 above, adapting heading level to match existing `AGENTS.md` conventions.

---

### 5. Recommended — Update `llm-docs/CONTENT-JOURNEY-UX-CONTRACT.md` §Content Creation

Replace any reference to `specs/content-journey/create/` with `specs/create/`. Add a pending-decision notice for the mobile layout question:

```markdown
<!-- UPDATE: spec path changed from specs/content-journey/create/ to specs/create/ as of 2026-05-09 -->

**Active spec:** `docs/saas-frontend/specs/create/00-index.md`

> **Pending architecture decision:** The recovered spec targets a single responsive layout for `/create`. The observed implementation redirects to a stripped mobile form. This contradiction must be resolved before `screen-spec.md` can be promoted to approved. See `00-index.md §Open questions #3`.
```

---

## 7. Verification

- [ ] At least one agent-facing routing file names the active spec package path.
  - **Status:** OPEN — CLAUDE.md and AGENTS.md entries have not yet been applied to the Pulse codebase. Apply §6 items 3 and 4.
- [ ] No agent-facing routing file names only the deprecated path without a redirect.
  - **Status:** OPEN — `llm-docs/CONTENT-JOURNEY-UX-CONTRACT.md` still references the deprecated path. Apply §6 item 5.
- [x] `docs/saas-frontend/specs/create/00-index.md` has a "How agents find this package" section.
  - **Status:** PASS — section updated in this session (§6 item 1, Applied).
- [ ] `docs/saas-frontend/specs/content-journey/create/DEPRECATED.md` exists with redirect notice.
  - **Status:** OPEN — `DEPRECATED.md` has not yet been created. Apply §6 item 2.
- [ ] No unresolved references to deprecated paths in non-deprecated files.
  - **Status:** OPEN — `llm-docs/CONTENT-JOURNEY-UX-CONTRACT.md` contains a reference to `specs/content-journey/create/`. Apply §6 item 5.

**References to deprecated path found in non-deprecated files (Step 7 repo-wide search):**

| File | Match | Action |
|---|---|---|
| `llm-docs/CONTENT-JOURNEY-UX-CONTRACT.md` | `specs/content-journey/create/` | Update to `specs/create/` (§6 item 5) |

No other non-deprecated files contain unresolved references to `specs/content-journey/create/`.

## 8. Result

**FAIL** — 4 items remain unresolved pending application to the Pulse codebase.

1 item was resolved in this session: `00-index.md` "How agents find this package" section is now complete and accurate (§6 item 1).

To reach PASS, apply §6 items 2–5 to the Pulse codebase, then re-run verification.
