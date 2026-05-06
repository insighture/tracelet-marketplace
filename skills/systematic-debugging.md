---
name: systematic-debugging
description: Use when investigating any bug, unexpected behavior, or failing test — before writing any fix
---

# Systematic Debugging

## The Iron Law

```
NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST
```

Guessing at fixes without understanding root cause leads to: wrong fix, same bug under different conditions, or new bugs introduced by the patch. Always find the root cause first.

## When to Use This Skill

- A test is failing and you don't immediately know why
- A behavior is unexpected or different from what the code appears to do
- A fix was applied but the bug recurred
- "It worked before" — something changed and you need to find what

## Phase 1: Reproduce

Before investigating, reproduce the bug deterministically.

1. **Identify the minimal reproduction**: What's the smallest input/state that triggers it?
2. **Confirm the failure**: Run it. See the failure with your own eyes (or in output).
3. **Confirm the expected behavior**: What *should* happen? Write it down.

If you cannot reproduce it, you cannot fix it. Do not proceed to Phase 2 until you have a reliable reproduction.

## Phase 2: Isolate

Narrow the blast radius. Find the smallest unit of code where the wrong behavior occurs.

Strategies:
- **Binary search**: Does the bug occur at the midpoint of the call stack? Narrow from there.
- **Comment out**: Remove code until the bug disappears, then re-add until it returns.
- **Add logging**: Log intermediate values to find where expected diverges from actual.
- **Unit test the suspect**: Write a minimal test targeting the suspected function in isolation.

Output of this phase: "The bug is in `<function/module>`, specifically when `<condition>`."

## Phase 3: Hypothesize

Generate a list of specific, falsifiable hypotheses. At least two before testing any.

Format each hypothesis:
```
IF <condition>, THEN <behavior> BECAUSE <mechanism>
```

Example:
```
IF the config value is empty string, THEN JSON.parse throws BECAUSE "" is not valid JSON
IF the config is nil, THEN the nil dereference panics BECAUSE we read .Timeout without a nil check
```

Do not start fixing until you have hypotheses that explain the root cause.

## Phase 4: Test Hypotheses

Test each hypothesis cheaply before writing a fix:

- **Add a log statement** at the suspected location
- **Write a failing unit test** that captures the hypothesis
- **Use the debugger** to inspect state at the suspect line
- **Read the code path** end-to-end following actual data flow

For each hypothesis: confirm or rule out. Update the list. Repeat until one hypothesis is confirmed.

## Phase 5: Fix

Only after confirming root cause:

1. **Write a failing test** that captures the exact failure mode (if not already written).
2. **Write the minimal fix** that makes the test pass.
3. **Run the full test suite** — confirm no regressions.
4. **Explain the fix** in the commit message: what the root cause was and why this fix addresses it.

## Anti-Patterns

| Anti-Pattern | Why It's Wrong |
|-------------|---------------|
| "Try this and see if it works" | No hypothesis. May mask the real bug. |
| Fix the symptom, not the cause | Bug returns under different conditions. |
| Multiple changes at once | Can't tell which change fixed it. |
| Skip reproduction | May be fixing a different scenario entirely. |
| "It's probably X" without checking | Confirmation bias. Wastes time if wrong. |

## When You're Stuck

- **Take a step back**: Re-read the error message literally. What does it actually say?
- **Check recent changes**: `git log --oneline -20`. What changed recently?
- **Read the docs**: Not the code — the documentation for the library/API you're calling.
- **Rubber duck**: Explain the problem out loud (or in a comment). The act often reveals the answer.
- **Ask for help**: State the bug, what you've tried, and what you expect. Don't just say "it's broken."

## Debugging Checklist

Before submitting a fix:

- [ ] Bug is reliably reproduced
- [ ] Root cause is identified (not just the symptom)
- [ ] Root cause explains all observed manifestations
- [ ] Fix targets root cause, not symptom
- [ ] Failing test added for the exact scenario
- [ ] All tests pass after fix
- [ ] Commit message explains root cause and fix rationale

*Source: github.com/obra/superpowers*
