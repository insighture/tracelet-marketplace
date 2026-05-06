---
name: git-commit-conventions
description: Conventional Commits skill for AI agents — feat/fix/chore prefixes, scoped commits, and co-authored-by footers.
kind: skill
---

# Git Commit Conventions

Skill for AI coding agents to produce well-formed, reviewable git commits. Based on Conventional Commits 1.0.

## When to Use This Skill

Use this skill whenever you are about to run `git commit`. It governs how to structure the message, what to stage, and how to handle edge cases.

## Commit Message Format

```
<type>(<scope>): <short summary>

[optional body]

[optional footer(s)]
```

### Types

| Type | When to use |
|------|------------|
| `feat` | New feature or capability visible to users |
| `fix` | Bug fix |
| `docs` | Documentation only (README, comments, ADRs) |
| `chore` | Build, tooling, dependency updates, config |
| `refactor` | Code restructuring with no behavior change |
| `test` | Adding or updating tests |
| `ci` | CI pipeline changes |
| `perf` | Performance improvement |

### Scope (optional)

Short noun describing the module or area: `api`, `agent`, `dashboard`, `auth`, `migrations`.

### Summary line

- Lowercase, no period at the end.
- Imperative mood: "add", "fix", "remove" — not "added", "fixed", "removed".
- Under 72 characters including type and scope.
- Describes **what** the commit does, not **how**.

### Body (optional)

- Wrap at 72 characters.
- Explain **why** the change is needed. The diff shows what changed.
- Separate from summary with a blank line.

### Footer

Always include for AI-assisted commits:
```
Co-Authored-By: Claude <noreply@anthropic.com>
```

Breaking changes:
```
BREAKING CHANGE: <description of what breaks and how to migrate>
```

## What to Stage

- Stage specific files by name. Never `git add -A` or `git add .`.
- Exclude: `.env`, `*.log`, lock files that weren't intentionally changed, generated files outside of a `make generate` step.
- One concern per commit. If two unrelated things changed, make two commits.

## When Not to Commit

- When there are failing tests that weren't failing before this change.
- When the build is broken.
- When there are uncommitted secrets or credentials in staged files.
- When explicitly asked to hold off.

## Examples

```
feat(auth): add RBAC permission check on /api/v1/skills

Without this the endpoint was accessible to any authenticated user
regardless of their role. Now requires workbench:skills:write.

Co-Authored-By: Claude <noreply@anthropic.com>
```

```
fix(migrations): wrap InsertAgentPolicy in correct params struct

sqlc generated a CreateParams struct but the call site was passing
positional args, causing a compile error after sqlc regeneration.

Co-Authored-By: Claude <noreply@anthropic.com>
```

```
chore(deps): upgrade pgx to v5.7.1

Fixes CVE-2025-12345 in the pgx connection pool.

Co-Authored-By: Claude <noreply@anthropic.com>
```
