# Dependency Handoff

Use this when the investigation cannot proceed locally because another team owns the compiler layer, hardware backend, proprietary dependency, missing environment, or upstream source.

## Handoff Checklist

- State the blocker in one sentence.
- Include the smallest reproducer and exact command.
- Include expected vs actual behavior.
- Include environment and versions.
- Include the strongest narrowed evidence.
- Include raw logs and generated IR/artifacts.
- Include exact source links and suspected files/functions if known.
- Include what has already been ruled out.
- Ask one to three concrete questions of the dependency owner.

## Export Hygiene

Before bundling:

- remove credentials and tokens
- remove private datasets unless required and approved
- replace absolute home paths in reports when they are not needed
- exclude large build directories unless they contain required artifacts
- verify the bundle contains `reports/report.md`, `reports/report.html`, and `checksums.txt`

