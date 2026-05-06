# Visual Vocabulary

This document establishes the canonical vocabulary for describing visual UI decisions across all skills.

## Layout Archetypes
- Sidebar App
- Centered Card
- Split Panel
- Dashboard Grid
- Wizard

## Density
- Sparse
- Medium
- Dense

## Shape Language
- Sharp (0-2px radius)
- Mildly Rounded (4-8px radius)
- Pill-like (Fully rounded)

## Surface Style
- Flat
- Outlined
- Elevated (Shadows)
- Glassy
- Card-heavy

## Token Mappings (Reference)
These concepts should map to concrete design tokens (e.g., in Tailwind CSS format):

**Layout & Density**
- Sparse: `gap-8`, `p-8`, `leading-loose`
- Medium: `gap-4`, `p-4`, `leading-normal`
- Dense: `gap-2`, `p-2`, `text-sm`, `leading-tight`

**Shape Language**
- Sharp: `rounded-none` (0px)
- Mildly Rounded: `rounded-md` (6px) to `rounded-lg` (8px)
- Pill-like: `rounded-full` (9999px)

**Surface Style**
- Flat: `shadow-none`, solid background
- Outlined: `border border-gray-200`, `shadow-none`
- Elevated: `shadow-md` to `shadow-xl`
- Glassy: `bg-white/10 backdrop-blur-md border border-white/20`
