# Contributing to Interface Skills

Thank you for your interest in improving the Interface Skills toolkit!

## Adding a New Skill
1. Create a new directory under `skills/` named `ui-[skill-name]`.
2. Add a `SKILL.md` file with YAML frontmatter containing the `name` and `description`.
3. Ensure your skill adheres to the shared references in `shared/references/`.
4. Update the `README.md` to include your new skill in the core workflow if applicable.

## Improving Shared References
If you add new taxonomy items (e.g., a new layout archetype), update `shared/references/visual-vocabulary.md` and test the validation script.

## Validation
Run the validation script before submitting a Pull Request:
```bash
python scripts/validate-skill.py
```
