---
name: spec-workflow
description: Structured spec-first development — requirements, design, implementation, and review checklist.
kind: skill
---

# Spec Workflow

Structured workflow for building features spec-first. Use before writing any implementation code for non-trivial features. Prevents wasted implementation effort and misaligned scope.

## When to Use This Skill

- New feature that requires more than one file change
- Feature with unclear or ambiguous requirements
- Anything that touches auth, data model, or public API surface
- Any work estimated to take more than 30 minutes

Skip for: bug fixes with a clear root cause, pure refactors, documentation.

## Phase 1: Requirements

Before touching code, write a requirements document (markdown, in the PR or a scratch file):

```markdown
## Feature: <name>

### Problem
<1-2 sentences: what pain does this solve? who is affected?>

### Success criteria
- [ ] <observable, testable outcome>
- [ ] <another outcome>

### Out of scope (explicit)
- <thing that sounds related but we're NOT doing>

### Open questions
- <anything needing clarification before design>
```

Do not proceed until open questions are answered. If you can't answer them, surface them to the user.

## Phase 2: Design

Write a design doc covering:

**Data model changes** (if any)
- New tables/columns
- Migration strategy (expand-contract if existing data)
- Indexes needed

**API surface** (if any)
- Endpoint: `METHOD /path`
- Request shape
- Response shape
- Auth requirement
- Error cases

**Component/module structure**
- What new files are created?
- What existing files change?
- What's the dependency graph?

**Edge cases to handle**
- Empty/zero input
- Maximum input
- Concurrent operations
- Failure modes

Review the design against success criteria. If a criterion isn't addressed, design is incomplete.

## Phase 3: Implementation Plan

Break the design into ordered tasks. Each task must be:
- **Completable in one commit**
- **Independently verifiable** (a test can confirm it)
- **Non-breaking** to the state before it

```markdown
## Tasks

- [ ] 1. DB migration: add `content_url` column to `skills_catalog`
- [ ] 2. sqlc: update queries and regenerate
- [ ] 3. Store: update CreateSkillCatalog to accept content_url
- [ ] 4. Handler: pass content_url through from request
- [ ] 5. Frontend: add content_url to SkillCatalog interface and createSkill call
- [ ] 6. Tests: add test for CreateSkill with content_url
```

Identify which tasks can be parallelized (no dependencies between them).

## Phase 4: Implementation

Execute tasks in order. After each task:
1. Run tests: does the task's test pass?
2. Run full suite: no regressions?
3. Commit with a descriptive message referencing the task.

If a task reveals a flaw in the design, stop, update the design doc, then continue.

## Phase 5: Review Checklist

Before marking the feature complete:

**Functional**
- [ ] All success criteria met
- [ ] Edge cases tested
- [ ] Happy path works end-to-end

**Security**
- [ ] New endpoints authenticated + authorized
- [ ] Input validated at boundary
- [ ] No secrets in code or logs

**Quality**
- [ ] All new code has tests
- [ ] No dead code left over
- [ ] No TODO without a tracking issue

**Documentation**
- [ ] `FEATURES.md` updated if this is a new feature
- [ ] New endpoint has OpenAPI annotation
- [ ] New DB column has a comment explaining its purpose

## Anti-Patterns

| Anti-Pattern | Why |
|-------------|-----|
| "I'll figure it out as I go" | Wasted implementation when requirements clarify differently |
| Design doc after implementation | Post-hoc rationalization, not design |
| Tasks too large ("implement auth") | Can't verify, can't commit cleanly |
| Skipping edge cases in design | They appear in bugs later |
| Scope creep during implementation | Stop, update requirements, re-plan |

## Template Files

Create `docs/specs/<feature-slug>.md` for any spec that needs stakeholder review or will be referenced in future work.
