---
name: software-architect
description: System design skill — trade-off analysis, ADR generation, scalability review, and component diagrams.
kind: skill
---

# Software Architect

System design and architecture review skill. Use when designing new systems, evaluating architectural decisions, or reviewing for scalability and maintainability.

## When to Use This Skill

- Designing a new service, module, or significant feature
- Evaluating multiple implementation approaches
- Reviewing a PR for architectural soundness
- Writing an Architecture Decision Record (ADR)
- Estimating scalability limits of existing design

## System Design Framework

When designing a system, work through these layers in order:

### 1. Requirements Clarity

Before designing, nail down:
- **Functional requirements**: What must the system do?
- **Non-functional requirements**: Latency, throughput, consistency, availability, durability
- **Scale**: How many users, events, records? At 10× growth?
- **Constraints**: Existing infrastructure, team expertise, time budget

### 2. High-Level Design

Identify the major components and their responsibilities:

```
[Client] → [API Gateway] → [Service A] → [DB A]
                        → [Service B] → [Cache]
                                     → [Service A] (internal call)
```

For each component, state:
- **Responsibility**: One sentence
- **Interface**: What does it expose?
- **Dependencies**: What does it need?

### 3. Data Model

Design the schema before the code:
- Entities and their relationships
- Access patterns (what queries will run?)
- Indexes needed for each access pattern
- Consistency requirements (eventual vs strong)
- Data lifecycle (TTL, archival, deletion)

### 4. Trade-Off Analysis

For any non-trivial decision, compare at least two options:

| | Option A | Option B |
|-|---------|---------|
| Complexity | Low | Medium |
| Performance | O(n) | O(log n) |
| Consistency | Eventual | Strong |
| Ops burden | Low | Higher |
| **Best for** | < 10k records | > 10k records |

State your recommendation and the key assumption it depends on.

### 5. Failure Modes

For each component, ask:
- What happens if this component is down?
- What's the blast radius?
- How does the system degrade gracefully?
- What's the recovery path?

## ADR Format

When a decision needs to be recorded:

```markdown
# ADR-NNNN: <Title>

## Status
Proposed | Accepted | Deprecated | Superseded by ADR-MMMM

## Context
<What is the situation forcing this decision?>

## Decision
<What are we doing?>

## Consequences
**Positive:**
- <benefit>

**Negative:**
- <cost or trade-off>

**Risks:**
- <what could go wrong, and mitigation>
```

## Scalability Review Checklist

For any system design, verify:

**Database**
- [ ] All query patterns have supporting indexes
- [ ] No queries that scan full tables at scale
- [ ] Write path doesn't create hot partitions
- [ ] Connection pool sized for peak load

**API**
- [ ] Pagination on all list endpoints (cursor-based for consistency)
- [ ] Rate limiting on expensive operations
- [ ] Caching for expensive read-heavy queries (with correct invalidation)
- [ ] Async for operations that don't need to be synchronous

**Dependencies**
- [ ] Timeouts on all external calls
- [ ] Circuit breaker or fallback for non-critical dependencies
- [ ] Retry with exponential backoff and jitter
- [ ] What happens if this dependency is slow? Does it cascade?

**State**
- [ ] Idempotent operations where retry is possible
- [ ] No lost updates under concurrent writes (optimistic locking or transactions)
- [ ] Event ordering preserved where required

## Component Diagram Notation

Use text-based diagrams for architecture docs:

```
┌─────────────┐     HTTP      ┌─────────────┐
│   Dashboard │ ──────────── ▶ │     API     │
└─────────────┘               └──────┬──────┘
                                     │ pgxpool
                              ┌──────▼──────┐
                              │  Postgres   │
                              └─────────────┘
```

## Review Questions (Non-trivial PRs)

1. **Security**: Any authz gaps? Missing audit? Token exfil possible?
2. **Edge cases**: Empty input? Max input? Concurrency? Retries?
3. **Bypasses**: Another code path that avoids this check?
4. **Breaking points**: Rollback risk? Undocumented invariants?
5. **Scalability**: 10× events/agents/findings? Upstream 500s?
