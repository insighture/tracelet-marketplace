---
name: cursor-rules-typescript
description: Cursor rules tuned for TypeScript monorepos — strict imports, no any, prefer unknown, consistent error patterns.
kind: cursor_rules
---

# Cursor Rules — TypeScript

Cursor rules for TypeScript monorepos. Enforces strict type discipline, consistent error handling, and import hygiene.

## Type Safety

- Never use `any`. Use `unknown` for values of unknown type and narrow before use.
- Prefer `interface` over `type` for object shapes. Use `type` for unions and intersections.
- Always annotate function return types explicitly for exported functions.
- No non-null assertions (`!`) without a comment explaining why null is impossible here.
- Enable strict mode: `"strict": true` in `tsconfig.json`.

## Imports

- No default exports for modules with multiple exports. Use named exports.
- Barrel files (`index.ts`) only at package boundaries, not within a package.
- Sort imports: external → internal → relative. No mixing.
- Use path aliases (`~/`) for cross-package imports; never `../../..`.
- No circular imports. Run `madge --circular` in CI.

## Error Handling

- Never swallow errors silently (`catch (_) {}`).
- Wrap external calls: `Result<T, E>` pattern or typed error classes.
- Never `throw` a string. Throw an `Error` instance with a descriptive message.
- At API boundaries, convert internal errors to user-facing messages before returning.

## Async / Promises

- Always `await` or chain `.catch()` — no floating promises.
- Use `Promise.allSettled` when you need partial results; `Promise.all` when all must succeed.
- No `async` functions that never `await` anything.

## Naming

- `PascalCase` for types, interfaces, classes, and React components.
- `camelCase` for variables, functions, and methods.
- `SCREAMING_SNAKE_CASE` for module-level constants.
- Boolean variables: `is`, `has`, `can`, `should` prefix.

## React (when applicable)

- No class components. Function components with hooks only.
- No inline `style` props. Use CSS modules or the design system's semantic tokens.
- Key props on list items: use stable IDs, never array index.
- No direct DOM manipulation. Use refs only when required by third-party libraries.

## Testing

- Colocate tests: `foo.test.ts` next to `foo.ts`.
- Test names: `it("should <action> when <condition>")`.
- No `any` in test code.
- Mock at the boundary (HTTP, DB), not at function level.
