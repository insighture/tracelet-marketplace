---
name: agents-md-standard
description: Shared AGENTS.md template for teams using Codex and other multi-agent systems.
kind: agents_md
---

# AGENTS.md Standard

Shared AGENTS.md template for organizations running Codex, Claude Code, and other multi-agent systems. Covers tool permissions, context length, escalation paths, and safe defaults.

## Tool Permissions

Agents may freely use:
- Read, Write, Edit (file operations on the working tree)
- Bash (non-destructive commands: grep, find, ls, cat, git log, git diff, git status)
- WebFetch, WebSearch (read-only web access)

Agents must pause and confirm before:
- Destructive Bash operations: `rm`, `git reset --hard`, `git push --force`, `DROP TABLE`
- Writing to files outside the repository root
- Running commands that create or modify external resources (cloud, databases, CI)
- Committing or pushing to remote

Agents must never:
- Store secrets, tokens, or credentials in files or logs
- Bypass pre-commit hooks (`--no-verify`)
- Modify `.env` files or secrets managers without explicit instruction
- Send messages, emails, or notifications without explicit instruction

## Context Length

- Keep system prompt under 4 000 tokens when possible.
- Summarize long file reads rather than including raw output.
- Use subagents for tasks that span more than 10 files.
- Evict stale context: re-read only files that have changed.

## Escalation Paths

When an agent is blocked or uncertain:
1. State the blocker clearly in one sentence.
2. Offer two or three concrete options with trade-offs.
3. Wait for user selection before proceeding.
4. Never silently skip a step or substitute a different approach.

## Commit Conventions

- Conventional Commits: `feat:` `fix:` `docs:` `chore:` `refactor:` `test:` `ci:`
- One concern per commit.
- Co-authored-by footer:
  ```
  Co-Authored-By: Claude <noreply@anthropic.com>
  ```

## Output Format

- Code blocks for all code, commands, and file paths.
- Plain prose for explanations — no bullet-point overuse.
- Confirm destructive actions before executing, not after.
- No hallucinated file paths or function names — verify before referencing.
