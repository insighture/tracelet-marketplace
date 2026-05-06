---
name: code-review-checklist
description: Rules file instructing AI to review for security loopholes, edge cases, bypass paths, breaking points, and scalability.
kind: rules
---

# Code Review Checklist

When reviewing code, work through these five categories in order. Report findings grouped by category. Each finding should include: file + line, severity (critical / high / medium / low), description, and suggested fix.

## 1. Security Loopholes

- Missing authentication or authorization on endpoints?
- SQL built with string interpolation or format strings?
- Secrets, tokens, or credentials committed or logged?
- Input not validated at the boundary (type, length, allowlist)?
- CORS set to `*` for authenticated endpoints?
- Error responses leaking internal details (stack traces, DB errors)?
- Missing audit row for a state-changing action?
- Broken access control: can a lower-privileged user reach data belonging to another?

## 2. Edge Cases

- What happens with empty input? Null/nil? Zero-length arrays?
- What happens at maximum input size (1 MB body, 10 000 items, max int)?
- What happens on retry? Is the operation idempotent?
- What happens if an external service returns 429, 500, or times out?
- Unicode edge cases: RTL text, zero-width characters, emoji in identifiers?
- Timezone edge cases: DST transitions, leap seconds, UTC vs local?

## 3. Ways Around Things

- Is there another code path that bypasses this check?
- Can a stale cache serve an outdated response after a permission change?
- If this middleware is skipped (wrong router group), what's exposed?
- Can an attacker supply a specially crafted input that short-circuits validation?
- Is there a race condition between check-then-act operations?

## 4. Breaking Points

- What breaks if this service restarts mid-operation?
- Is there a DB transaction wrapping all-or-nothing state changes?
- If the migration is run twice, does it fail gracefully or corrupt data?
- What's the rollback plan if this deploy is bad?
- Are there undocumented invariants that callers depend on silently?
- Does removing this code break any other module that imports it?

## 5. Scalability

- What happens at 10× current event volume?
- Are there N+1 queries? (Loop calling DB per item instead of one batch query.)
- Missing database index on a column used in WHERE or ORDER BY?
- Unbounded in-memory accumulation (growing slice/map without eviction)?
- If an upstream service is slow, does it cascade to degrade everything?
- Is there a rate limit protecting expensive operations?

## Severity Guide

| Severity | Meaning |
|----------|---------|
| **Critical** | Security breach or data loss possible. Block merge. |
| **High** | Likely production incident under realistic load. Block merge. |
| **Medium** | Bug that will surface; doesn't block but must be tracked. |
| **Low** | Style / best practice. Advisory only. |
