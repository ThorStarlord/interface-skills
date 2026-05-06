---
name: ui-visual-calibration
description: Directly solves the “mental picture mismatch” problem by defining density, layout archetypes, etc.
status: draft
---

# UI Visual Calibration

This skill translates fuzzy visual taste into concrete properties, replacing vague words with specific structural and aesthetic decisions (density, layout archetype, shape language, surface style, etc.).

## Vague Language Translation
When users provide vague terms, immediately map them to concrete properties before proceeding. Reference `vague-language-translator.md` to translate words like "Clean", "Modern", "Professional", etc. into specific Layout Archetype, Density, Shape Language, and Surface Style decisions. Always confirm these translations with the user.

## Output Format
The skill produces a `visual-calibration.md` file (or section) with the following structure:

```markdown
# Visual Calibration Sheet

## Translation Log
- **User intent:** "Make it look clean and modern"
- **Translation:** Minimalist (Max whitespace, monochrome), Modern (Flat surfaces, large radius)

## Concrete Visual Decisions
- **Layout Archetype:** Centered Card
- **Density:** Sparse (`gap-8`, `p-8`)
- **Shape Language:** Mildly Rounded (`rounded-md` to `rounded-lg`)
- **Surface Style:** Flat (solid backgrounds, no shadows)
- **Palette Guidance:** Monochrome with a single vibrant accent color
```
