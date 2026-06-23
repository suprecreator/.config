---
name: visual-artifact-explainer
description: Create self-contained HTML artifacts with visual diagrams, charts, maps, timelines, matrices, and interactive explanations for answering complex questions. Use when the user asks to explain, analyze, diagnose, find problems, compare options, answer a complex question, teach a concept, summarize evidence, solve a problem, or make a decision and would benefit from an artifact, HTML page, dashboard, visual chart, flowchart, cause-effect diagram, decision matrix, or other visual reasoning aid.
---

# Visual Artifact Explainer

## Goal

Transform complex answers into a clear visual HTML artifact when visuals will improve understanding. Use the artifact to find the problem, show the reasoning, answer the question, and make the recommended action obvious.

## Workflow

1. Clarify the job: identify whether the user needs explanation, diagnosis, analysis, comparison, decision support, teaching, or a concrete solution.
2. Answer first in structure: define the core question, the key finding, the evidence, and the recommended next step before designing visuals.
3. Choose a visual model:
   - Cause-effect map for root-cause analysis.
   - Flowchart or system map for processes and dependencies.
   - Decision matrix for comparing options.
   - Timeline for events, project plans, or history.
   - Funnel, Sankey-style flow, heatmap, Pareto bars, or scorecards for data analysis.
   - Before/after panels for problem and solution framing.
4. Create a self-contained HTML artifact when it adds value. Prefer one focused page over many scattered files.
5. Make the final response concise: include the direct answer, the artifact path or link, and any important caveats.

## Artifact Rules

- Write the artifact in the user's language unless the user requests otherwise.
- Keep the HTML self-contained: inline CSS and inline JavaScript; avoid remote CDNs unless the user explicitly allows internet dependencies.
- Prefer semantic HTML, CSS grid/flex, inline SVG, and small vanilla JavaScript interactions.
- Use visual hierarchy: title, one-sentence answer, diagnostic sections, evidence, diagram, and action list.
- Design for scanning: labels, legends, badges, short annotations, and progressive disclosure for details.
- Do not create an HTML artifact for a trivial answer unless the user explicitly asks for HTML/artifact output.
- For uncertain analysis, show confidence and assumptions inside the artifact instead of hiding them.
- For data-driven claims, cite or label the data source used. If data is missing, create placeholders only when clearly marked.

## Files

- Use `assets/artifact-template.html` as a starting point when creating a local HTML artifact.
- Read `references/visual-patterns.md` when choosing the best diagram or chart pattern for the problem.

## Quality Bar

Before finishing, inspect the artifact for:

- The main answer is visible in the first screen.
- The visual explains the reasoning, not just decorates it.
- Text is readable on desktop and mobile widths.
- Colors encode meaning consistently.
- The artifact includes a concrete next step or resolution path when solving a problem.
