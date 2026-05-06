---
name: claude-code-best-practices
description: Opinionated CLAUDE.md covering commit hygiene, tool use etiquette, and context-window discipline.
kind: claude_md
---

# Claude Code Best Practices

Shared CLAUDE.md for teams using Claude Code. Enforces commit hygiene, tool use discipline, and context-window awareness across all agents in the organization.

## Commit Hygiene

- Always use Conventional Commits: `feat:`, `fix:`, `docs:`, `chore:`, `refactor:`, `test:`, `ci:`
- One concern per commit. Never bundle unrelated changes.
- Co-authored-by footer required for AI-assisted commits:
  ```
  Co-Authored-By: Claude <noreply@anthropic.com>
  ```
- Never amend published commits. Create a new commit instead.
- Never force-push to main/master.

## Tool Use Etiquette

- Prefer dedicated tools over Bash when available (Read over cat, Edit over sed).
- Run independent tool calls in parallel in a single message.
- Never skip hooks (`--no-verify`) unless explicitly requested.
- For destructive operations (rm -rf, reset --hard, force-push), confirm with user first.
- Avoid unnecessary sleep commands — use background tasks instead.

## Context-Window Discipline

- Read only the files you need. Avoid reading entire directories.
- Summarize findings in text before calling more tools.
- When a task spans many files, use subagents to keep main context clean.
- Don't re-read files that haven't changed since the last read.
- State results and decisions directly — no running commentary.

## Code Quality

- No comments that explain WHAT the code does. Only WHY (hidden constraints, workarounds).
- No `// TODO` without a tracking issue.
- No hardcoded palette colors. Use semantic tokens only.
- Default to writing no tests for exploratory code; always test production paths.
- Bug fix → failing-then-passing test in the same PR.

## Security

- Never log auth headers, tokens, prompts, or PII.
- No `fmt.Sprintf` into SQL. Use parameterized queries.
- Validate all input at system boundaries (user input, external APIs).
- CORS: never `*` for authenticated paths.
- For new endpoints: document who can call it, auth boundary, input validation, audit row.

## Response Style

- Responses should be short and concise.
- End-of-turn summary: one or two sentences. What changed and what's next.
- No trailing summaries after diffs — the user can read the diff.
- Use Github-flavored markdown for formatting.
