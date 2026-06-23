# Visual Patterns

Use this reference to choose a visual form quickly.

## Problem Diagnosis

- **Root-cause tree**: Use for "why is this happening?" Start with the symptom, branch into people/process/tool/data/context causes, and mark the most likely causes.
- **Fishbone diagram**: Use when many contributing factors must be grouped. Keep branches short and label each branch with a category.
- **Issue heatmap**: Use when several areas must be scored by severity and urgency. Use two axes or a table with color intensity.
- **Evidence ladder**: Use when the answer depends on confidence. Stack observation -> interpretation -> implication -> action.

## Explanation And Teaching

- **Concept map**: Use for abstract ideas and relationships. Put the core concept in the center and connect parts with labeled lines.
- **Step-by-step flow**: Use for procedures, algorithms, workflows, or "how it works" explanations.
- **Before/after contrast**: Use when the user needs to understand the change, fix, or tradeoff.
- **Layered model**: Use for systems with levels such as user interface, service, database, policy, or business operations.

## Analysis And Decisions

- **Decision matrix**: Use when comparing options. Columns are options; rows are criteria; include weights when criteria are not equal.
- **Tradeoff frontier**: Use when choices optimize two competing dimensions such as speed vs. quality or cost vs. accuracy.
- **Pareto bars**: Use when a few causes likely dominate the outcome. Sort descending and highlight the top contributors.
- **Timeline**: Use for events, milestones, causal sequences, or project plans.

## Answer Structure

For most artifacts, use this layout:

1. **Header**: question, short answer, confidence.
2. **Visual diagnosis**: the primary chart or diagram.
3. **Key findings**: 3-5 bullets tied to the visual.
4. **Reasoning detail**: evidence, assumptions, edge cases.
5. **Action plan**: next steps, owners, timing, or decision.

## HTML Implementation Notes

- Use inline SVG for diagrams that need arrows, nodes, timelines, or custom chart geometry.
- Use CSS grid tables for matrices and heatmaps.
- Use native `<details>` sections for optional reasoning.
- Add `aria-label` to important diagrams and ensure text labels duplicate any color-only meaning.
- Prefer 2-4 accent colors with neutral backgrounds. Avoid making every component the same hue.
