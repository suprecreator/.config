# Report Contract

Every completed investigation must contain both `reports/report.html` and `reports/report.md`.

## Human HTML Report

Use short sections:

1. Executive summary
2. Current status
3. Reproduction
4. Key evidence
5. Root-cause or narrowing analysis
6. Code links
7. Debug timeline
8. Handoff or next actions

Keep the HTML readable without the repository open, but link every claim to raw evidence when possible.

## AI Markdown Report

Include all details needed for another agent to continue:

- exact commands and working directories
- versions, commits, and environment
- generated artifacts and run ids
- minimized and original repro locations
- hypotheses tested and outcomes
- code links with line numbers
- unresolved questions and owner handoff notes

## Link Format

Use relative links for case artifacts:

```markdown
[stderr.log](../runs/001-baseline/stderr.log)
```

Use commit-pinned remote links for repository code when possible:

```markdown
[lib/Transforms/Foo.cpp:120](https://github.com/org/repo/blob/<commit>/lib/Transforms/Foo.cpp#L120)
```

If no remote URL is available, use a local path label and line number:

```markdown
`lib/Transforms/Foo.cpp:120`
```

