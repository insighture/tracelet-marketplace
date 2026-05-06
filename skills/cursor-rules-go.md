---
name: cursor-rules-go
description: Cursor rules for idiomatic Go — error wrapping, context threading, table-driven tests, and no global state.
kind: cursor_rules
---

# Cursor Rules — Go

Cursor rules for idiomatic Go codebases. Enforces error handling discipline, context threading, test patterns, and zero global state.

## Error Handling

- Always handle errors. Never `_` an error from a function that can fail.
- Wrap errors with context: `fmt.Errorf("doing X: %w", err)`.
- Use `errors.Is` / `errors.As` for error comparison. Never string-match errors.
- Define sentinel errors with `var ErrFoo = errors.New("foo")` at package level.
- Return errors up the call stack; log at the top boundary only, once.

## Context

- Every function that does IO or can block takes `ctx context.Context` as its first argument.
- Never store context in a struct. Pass it through function arguments.
- Respect `ctx.Done()` in long-running loops: `select { case <-ctx.Done(): return ctx.Err() }`.
- Use `context.WithTimeout` at the outermost call site (HTTP handler, job runner).

## Package Design

- No `utils`, `helpers`, or `common` packages. Name packages by what they provide.
- No global variables except `var _ Interface = (*Impl)(nil)` compile-time assertions.
- Pass dependencies explicitly: `*pgxpool.Pool`, `*store.Store`, etc.
- Unexport types and functions that don't need to cross package boundaries.

## Naming

- Acronyms in names are all-caps: `MCPID`, `HTTPURL`, `RBACPolicy`.
- Interface names: noun or verb-er (`Reader`, `Storer`, `PolicyEvaluator`).
- Test files: `foo_test.go`. Test functions: `TestFooBar` / `TestFooBar_edgeCase`.
- Receiver name: one or two letters, consistent across all methods.

## Testing

- Table-driven tests for any function with more than two input combinations.
- Subtests with `t.Run("case name", ...)` for clear failure messages.
- Use `testcontainers` for Postgres tests. Never mock the database.
- `t.Parallel()` at the top of each test function and subtest where safe.
- No `time.Sleep` in tests. Use `require.Eventually` with a timeout.

## Concurrency

- No bare `go func()` without a wait group or errgroup.
- Use `sync.Mutex` for protecting shared state. Document invariants in comments.
- Channels for signalling; mutexes for shared state. Don't mix the two roles.
- Close channels from the sender, never the receiver.

## Formatting

- `gofmt` and `goimports` on every save — non-negotiable.
- Line length: soft 100, hard 120. Split long function signatures vertically.
- Group imports: stdlib → external → internal. Blank line between groups.
