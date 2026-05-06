---
name: code-reviewer
description: Structured code review skill — correctness, security, performance, style, and test coverage.
kind: skill
---

# Code Reviewer

Structured code review skill for AI agents. Produces actionable findings grouped by severity. Use when reviewing a PR, a diff, or any code change.

## How to Review

1. Read the PR description first. Understand the intent before reading the diff.
2. Build a mental model: what should change, and what should stay the same?
3. Read the diff. Flag anything that contradicts the intent or violates the rules below.
4. Group findings by category and severity. Report all before suggesting fixes.

## Review Categories

### 1. Correctness

- Does the code do what the PR description says?
- Are there logic errors (off-by-one, wrong operator, incorrect condition)?
- Are edge cases handled: empty input, null/nil, zero, max value, concurrent access?
- Are error paths handled and not swallowed silently?
- Is the behavior correct under retry? Is this operation idempotent?

### 2. Security

- Any SQL built with string interpolation?
- Any input accepted without validation?
- Any secrets, tokens, or PII logged?
- Any new endpoint missing an auth check?
- Any new endpoint missing an authorization (permission) check?
- Any error response leaking internal details?
- See [Security Guidelines] for the full checklist.

### 3. Performance

- Any N+1 query pattern? (loop calling DB per item)
- Any missing index on a new column used in WHERE/ORDER BY?
- Any unbounded in-memory accumulation (growing slice/map)?
- Any synchronous operation that could be async?
- Any cache invalidation that's too broad (clears too much on every write)?

### 4. Test Coverage

- Is there a test for the new behavior?
- Is there a test for the main error path?
- Does the bug fix include a failing-then-passing test?
- Are tests asserting behavior (inputs → outputs) or just calling functions?
- Do tests hit real dependencies (DB, file system) or do they mock at the right level?

### 5. Maintainability

- Are names accurate and self-explanatory?
- Are there comments explaining WHAT the code does (unnecessary) vs WHY (necessary)?
- Is any function longer than ~50 lines and doing more than one thing?
- Is there dead code, commented-out code, or debug logging left in?
- Are there `// TODO` items without tracking issues?

### 6. Design & Architecture

- Does this follow the existing patterns in the codebase?
- Is there new abstraction that's premature or unnecessary?
- Is there duplication that would be better shared?
- Does this introduce a new global variable or global state?
- Does this introduce a circular dependency?

## Finding Format

Report each finding as:

```
[SEVERITY] Category — Short title
File: path/to/file.go:42
Issue: <what's wrong>
Risk: <what could go wrong>
Fix: <concrete suggestion>
```

## Severity Guide

| Severity | Meaning |
|----------|---------|
| **Critical** | Security breach, data loss, or incorrect behavior that will definitely be triggered. Block merge. |
| **High** | Likely production incident or security issue. Block merge. |
| **Medium** | Bug that will surface; track and fix before next release. |
| **Low** | Code quality, naming, style. Advisory only. |

## Reviewer's Mindset

- **Critique the code, not the author.** Every finding is about the code.
- **Be specific.** "This could be cleaner" is not a finding. "Line 42: variable `x` is unused after this assignment" is.
- **Suggest, don't command.** "Consider using X here because Y" leaves room for dialogue.
- **Acknowledge good work.** If something is done especially well, say so.
- **Technical correctness beats social comfort.** If something is wrong, say so clearly.

## When to Approve vs Request Changes

**Approve** when:
- All Critical and High findings are resolved
- Medium findings are tracked (issue created)
- Code does what it says it does

**Request changes** when:
- Any Critical or High finding exists
- The PR does not match its description
- Tests are missing for a non-trivial change

**Block** (escalate) when:
- Security vulnerability that could be exploited in production
- Data loss risk
- Breaking change without migration path
