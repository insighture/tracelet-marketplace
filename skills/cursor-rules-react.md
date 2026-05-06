---
name: cursor-rules-react
description: Cursor rules for React + TanStack Router — semantic tokens, no inline styles, Combobox over select, accessible forms.
kind: cursor_rules
---

# Cursor Rules — React / TanStack

Cursor rules for React applications using TanStack Router, Tailwind CSS, and a semantic design system.

## Components

- Function components with hooks only. No class components.
- One component per file. Filename matches component name (PascalCase).
- Export components as named exports, not default exports.
- Extract sub-components when JSX nesting exceeds 4 levels or 60 lines.
- Colocate component-specific hooks in the same file until they're reused.

## Design System — Mandatory Components

| Need | Use |
|------|-----|
| Dropdown / select | `<Combobox>` — never `<select>` |
| Badge / status | `<Badge>` |
| Empty list state | `<EmptyState>` |
| Page title | `<SectionHeader>` |
| Text input | `<Input>` |
| Toggle | `<Switch>` |
| Compact selector | `<SegmentedControl>` |
| Loading placeholder | `<Skeleton>` |

No bare `<h1>/<h2>` on top-level routes. No inline icon+title+description empty states.

## Styling

- Semantic tokens only. No hardcoded palette colors (`bg-zinc-100`, `text-rose-700`).
- No inline `style={{ color: "#..." }}`. Use CSS variables.
- Use `cn()` for conditional class merging. No string concatenation for classNames.
- Tailwind utility classes: alphabetical order within each variant group.
- Responsive: mobile-first. `sm:` / `md:` / `lg:` prefixes, never `max-*`.

## State & Data Fetching

- Server state via TanStack Query (`useQuery`, `useMutation`). No hand-rolled fetch in components.
- URL search params for filter/sort/drawer state. Round-trip links must preserve state.
- Local UI state (`useState`) only for ephemeral UI state (hover, open/closed).
- No context for data that could live in the URL or a query cache.

## Routing (TanStack Router)

- Route files named by path segment: `governance.findings.tsx` → `/governance/findings`.
- `createFileRoute` with the correct path string — checked by router at build time.
- No cross-product `<Link>` or `navigate()` inside product pages.
- `loader` for data that's required before render. `useQuery` for data that can defer.

## Accessibility

- All interactive elements are keyboard reachable and have accessible labels.
- Icon-only buttons: `aria-label` required.
- Form fields: `<label>` associated via `htmlFor` or wrapping.
- No `onClick` on `<div>` or `<span>`. Use `<button type="button">` or `<a>`.
- Color is never the sole indicator of state. Pair with text or icon.

## Performance

- `key` props on list items: stable IDs, never array index.
- `useMemo` / `useCallback` only when profiling shows a real problem.
- Lazy load routes and heavy components with `React.lazy` + `Suspense`.
- No side effects in render. All side effects in `useEffect` or event handlers.
