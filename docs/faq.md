# FAQ

## Q: Do I need to run every skill in the pipeline?

**A:** No. The pipeline is a menu, not a checklist. Start with `ui-brief` and `ui-blueprint` — those two cover most of the decisions that cause code rework. Add other skills when you have a specific need: `ui-visual-calibration` if aesthetic direction is unclear, `ui-component-spec` if you need precise state and accessibility coverage, `ui-redline` if the generated code doesn't match the spec. The recommended minimum path is brief → blueprint → acceptance → code → redline.

---

## Q: What's the difference between a blueprint and a screen spec?

**A:** A blueprint defines what is on the screen and how elements are ranked and laid out — it is a structural document. A screen spec (`ui-screen-spec`) adds the behavioral layer: state ownership, which states exist, what triggers transitions between them, error and empty states, and loading behavior. Blueprint answers "what is here and where". Screen spec answers "how does it behave and what happens when things go wrong".

---

## Q: Can I use these skills with my own design system?

**A:** Yes. The `ui-system` skill produces a `system.md` file that defines your design tokens (colors, spacing, type scale, radii). If your team already has a design system, you can either run `ui-system` to transcribe your existing tokens into this format, or write a `system.md` manually. Once a `system.md` exists in the spec package, all downstream skills reference it instead of inventing token values.

---

## Q: What happens if I skip ui-visual-calibration?

**A:** The model defaults to its priors for all visual decisions — spacing density, shape language, surface style, color usage. Those priors are usually reasonable but rarely match your actual intent. If you have a strong visual direction in mind, skipping calibration means re-correcting those decisions at the blueprint or code stage, which is more expensive. Calibration is most valuable when you have a reference product in mind ("make it feel like Linear") or when vague adjectives ("clean", "modern") have been used — those words need translation before layout work begins.

---

## Q: The model keeps ignoring my output template. What do I do?

**A:** Repeat the template at the end of your message, immediately before asking for output. System prompt instructions are deprioritized when the model is generating long content — putting the template at the end of the user turn keeps it fresh in the generation context. If the problem persists, explicitly state: "Produce output in exactly the structure shown below. Do not add, remove, or rename any section." See `docs/integrations.md` for more troubleshooting steps.

---

## Q: When should I use ui-spec-linter?

**A:** Use it when you have a complete or near-complete spec package and want a consistency check before handing off to code generation. It is particularly useful if multiple people worked on the spec, if the spec was built across many sessions, or if the brief changed after other artifacts were written. The linter catches contradictions between spec files (e.g. a component spec that references a state the blueprint doesn't define) and missing required sections. It is a draft skill — its output format may change.

---

## Q: What does the ⚠️ next to a skill name mean?

**A:** It means the skill is in draft status. The core behavior is defined and the skill is useful, but the output format has not been locked and the acceptance criteria may be incomplete. Do not depend on a draft skill's output structure across sessions — field names or section headings may change as the skill is validated. Draft skills are listed with ⚠️ in the skill map in `README.md`.

---

## Q: How do I contribute a new skill?

**A:** Create a directory under `skills/` named `ui-[skill-name]`. Add a `SKILL.md` with YAML frontmatter (name, description, status: draft) and all required sections (When-to-use, When-NOT, Core principle, Workflow, Output template, Anti-patterns, Acceptance criteria). Add an `agents/` subdirectory with an `openai.yaml` metadata file. Run `python scripts/validate-skill.py` before submitting a PR. See `CONTRIBUTING.md` and `docs/skill-authoring-guide.md` for the full requirements.

---

## Q: Can I use just one skill without the whole pipeline?

**A:** Yes. Every skill is self-contained. You can run `ui-redline` on an existing implementation without having used any other skill to build it. You can run `ui-component-spec` against a screenshot or a description without a brief. The skills are stronger when they reference each other's outputs, but they work independently. If you are running a skill without the upstream artifacts it expects, the skill will surface that as open questions or assumptions rather than failing silently.

---

## Q: How do I keep context across sessions?

**A:** Save each skill's output as a markdown file in a spec package directory (e.g. `specs/settings-page/`). At the start of a new session, reference the relevant files by path. In Claude Code, you can say "read specs/settings-page/brief.md and specs/settings-page/blueprint.md before we start". In other tools, paste the content of the relevant files into the conversation. The spec package exists specifically so that session state can be reconstructed from files — see `docs/how-it-works.md` for the full explanation.

---

## Q: What's the difference between ui-inspector and ui-redline?

**A:** `ui-inspector` gathers evidence — it examines a live implementation, captures DOM structure, computed styles, and accessibility properties, and produces a factual report of what was actually built. `ui-redline` uses that evidence (or a screenshot, or direct code review) to compare the implementation against the spec, classify each mismatch by severity, and produce a prioritized fix list with copy-paste refactor prompts. Inspector is a fact-gathering step; redline is a judgment and remediation step. Inspector is a draft skill; redline is stable.

---

## Q: The model added things I didn't ask for. Which skill prevents that?

**A:** `ui-brief` is where scope is fixed. The Non-goals section (section 8) lists what the feature explicitly does not include. If the model adds something you didn't ask for, it means either the brief didn't list it as a non-goal, or the model is not referencing the brief when generating. Check section 8 of your brief and add the unwanted feature as a non-goal. Then, when running the next skill, instruct the model to reference the brief's non-goals before generating output.

---

## Q: How do I know when a spec is good enough to generate code?

**A:** Run `ui-acceptance` against your spec package. The acceptance skill converts the spec into a testable implementation checklist. If the acceptance checklist can be written without needing to invent details (because the spec already specifies them), the spec is ready. A good signal: if you read the acceptance checklist and every item is traceable to a section in the brief, blueprint, or component spec, the spec is complete. If any acceptance item requires guessing, the corresponding spec section needs more detail. You can also run `ui-spec-linter` for a formal completeness check.

---

## Q: What if the brief changes after I've already written a blueprint?

**A:** Update the brief first, then cascade the change forward. Review the blueprint and identify every decision that was derived from the section that changed. Update those decisions in the blueprint. Then review the component spec and screen spec for decisions derived from the updated blueprint sections. The cascade stops when you reach artifacts that are not affected by the change. Do not silently update downstream artifacts without updating the brief — the brief is the root of the decision tree, and inconsistency between the brief and downstream artifacts is the most common source of spec bugs.

---

## Q: Is there a quick-start for someone who just wants to generate code?

**A:** The minimum viable path is: (1) run `ui-brief` to fix scope and the primary user, (2) run `ui-blueprint` to fix layout, (3) run `ui-acceptance` to get a checklist, (4) run `ui-generate-code` with the brief, blueprint, and acceptance checklist as context, (5) run `ui-redline` to catch deviations. This takes longer than pasting "build me a settings page" but produces output that is correct the first time and requires no rework. The full worked example in `examples/settings-page/` shows what this produces.

---

## Q: Why are the example spec files dated 2026?

**A:** The example spec package in `examples/settings-page/` was generated as a reference artifact. The dates reflect when the example was created. The dates have no significance beyond that — they are not targets or milestones.

---

## Q: Can multiple people work on a spec package at the same time?

**A:** Yes, but with care. The brief and visual calibration should be agreed on by all contributors before anyone writes a blueprint. The blueprint should be agreed on before anyone writes component specs. The pipeline is sequential by design — parallel work on dependent stages produces contradictions that have to be resolved manually. For team workflows, treat the brief approval (Step 4 of `ui-brief`) as a synchronization point that everyone must pass before downstream work begins.
