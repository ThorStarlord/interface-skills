# How Interface Skills Works

## The core problem

AI models build UIs from assumptions. When a user says "make a settings page", the model fills in every unspecified detail from its own priors — layout, hierarchy, density, component choices, copy, color. Those priors are invisible. They don't appear in any file. They can't be reviewed or approved. They are just baked into the output.

The result is a UI that looks plausible but doesn't match what the user imagined. The mismatch only becomes visible after code has been written. At that point, correcting it means describing the problem in vague terms ("it doesn't feel right", "something's off with the layout") and hoping the model guesses the right fix. Most of the time it doesn't.

The underlying issue is not model quality. It's that the decisions were never made explicitly. The model had to invent them because nobody specified them first. Interface Skills is a system for making those decisions before code is written, not after.

## The pipeline model

The pipeline is ordered to defer irreversible decisions for as long as possible.

```
brief → visual calibration → flow → blueprint → system → screen spec →
component spec → microcopy → acceptance → code generation → inspection → redline
```

Each stage forces a different class of decision. Brief forces product decisions (who is this for, what is the primary action, what is out of scope). Visual calibration forces aesthetic decisions (what density, what shape language, what reference products). Blueprint forces layout decisions (what is on screen, in what order, how does it reflow). System forces token decisions (exact colors, spacing units, type scale). Component spec forces anatomy decisions (what states exist, what the DOM structure is). Acceptance forces verification decisions (what passes, what fails).

The ordering matters because each artifact is a constraint on everything downstream. A blueprint that contradicts the brief is a defective artifact. A component spec that contradicts the blueprint is a defective artifact. The pipeline catches contradictions at each stage, before they propagate into code.

Each stage produces a locked artifact. Once a brief is approved, you do not revise it without understanding what changes downstream. If the brief changes, the blueprint may need to be re-derived. If the blueprint changes, the component spec may need to be revised. Changes are always possible — they just have to be acknowledged as changes, not smuggled in as assumptions.

Brief changes cascade forward. Redline findings cascade backward. A redline report that says "primary action button is not visually privileged" is pointing at a failure in the blueprint, not in the CSS. The fix belongs at the blueprint level, not the code level. Following the cascade back to the right artifact is what prevents the same problem from recurring.

## Spec packages

A spec package is a directory that contains every artifact for one feature. Brief, calibration, flow, blueprint, system, component specs, microcopy, acceptance criteria, redlines — all in one place.

The purpose is context reconstruction. AI sessions are stateless. A session in week 6 has no memory of the decisions made in week 1. Without a spec package, the developer has to re-explain the feature from scratch every session, and each re-explanation introduces drift. "Make the button bigger" in week 6 may contradict the sizing decision made in week 2. Nobody catches the contradiction because nobody has the week-2 decision in context.

A spec package solves this by being the single source of truth. At the start of any session, you reference the relevant spec files and the model has the full decision history. The brief tells it why the feature exists. The blueprint tells it what the layout is. The component spec tells it what states are required. There is nothing left to invent.

The spec package format is defined in `shared/references/spec-package-format.md`. The `examples/settings-page/` directory contains a complete worked example.

## The output contract

A well-written spec is a contract. On one side is the user, who has a mental picture of a UI. On the other side is the model, which will build that UI. The spec is the agreement between them about what that UI contains, how it behaves, and what "done" means.

Every decision that is left out of the spec will be decided by the model. The model will not leave it blank. It will fill in the gap with its priors — its training data, its defaults, its best guess at what a user like this probably wants. Those guesses are often reasonable. They are almost never exactly right.

The acceptance criteria section at the end of each skill's output template is a checklist of verifiable claims about the spec itself. If the acceptance criteria pass, the spec is complete enough to build from. If they fail, the spec has gaps that will become implementation bugs.

The discipline the pipeline enforces is: decide everything that can be decided before code runs. Accept that some things will be discovered late. But do not pretend to have decided things you haven't decided — that is where silent assumptions live, and silent assumptions are the root cause of most UI rework.

## Draft vs stable skills

Skills in this toolkit have one of two statuses: stable or draft.

A stable skill has a locked output format. Two different AI models running the same stable skill against the same input will produce outputs with the same structure, even if the specific content differs. The output template is precise enough to be a contract. The acceptance criteria are well-defined, with clear pass/fail conditions. The skill has been tested against multiple real scenarios and the output format has not needed to change.

A draft skill has a defined core behavior, but some implementation details are still being validated. The output format may change. The acceptance criteria may be incomplete. The skill may produce structurally inconsistent output across different sessions.

This matters practically: do not reference a draft skill's output format in other documents. Do not write acceptance criteria against fields that a draft skill produces, because those fields may be renamed or removed. A draft skill is useful — it produces better output than no skill at all — but its output is not a stable artifact. Once a skill is validated against two or three real scenarios with consistent output, it can be promoted to stable.

Draft skills are marked with ⚠️ in the skill map in `README.md`.
