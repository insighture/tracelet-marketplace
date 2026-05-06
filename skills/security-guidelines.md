---
name: security-guidelines
description: Shared CLAUDE.md section covering OWASP Top 10 prevention — no SQL interpolation, no secrets in logs, input validation at boundaries.
kind: claude_md
---

# Security Guidelines

Security rules for AI coding agents. Every PR is a security PR. These rules apply to all code written or reviewed.

## Input Validation

- Validate all input at system boundaries: HTTP handlers, CLI args, config files, external API responses.
- Never trust data that crosses a trust boundary. Sanitize before use.
- Use allowlists, not denylists. Reject anything not explicitly permitted.
- Maximum lengths on all string inputs. Reject oversized payloads early.

## SQL Injection Prevention

- Never use `fmt.Sprintf` or string concatenation to build SQL queries.
- Use parameterized queries exclusively: `$1`, `$2`, etc. for Postgres; `?` for SQLite.
- If dynamic SQL is unavoidable (dynamic column names, ORDER BY), use an allowlist of permitted identifiers.
- Log the query template, never the rendered query with parameter values.

## Authentication & Authorization

- Every non-public endpoint must verify authentication before doing any work.
- Authorization check (RBAC permission) runs after authentication.
- Never expose internal IDs or error details in 401/403 responses — generic message only.
- Session tokens: `HttpOnly`, `Secure`, `SameSite=Strict`. Never in URL params or logs.
- Rate-limit authentication endpoints. Lock out after repeated failures.

## Secrets Management

- Never hardcode secrets, API keys, or passwords in source code.
- Never log secrets, tokens, auth headers, prompts, or PII — log IDs and counts instead.
- Secrets come from environment variables or a secrets manager only.
- Rotate secrets that may have been exposed immediately. Treat exposure as a breach.

## CORS

- Never set `Access-Control-Allow-Origin: *` for authenticated endpoints.
- Allowlist origins explicitly. Log rejected origins at warn level.
- `Access-Control-Allow-Credentials: true` requires a specific origin, never `*`.

## Dependency Security

- Pin dependency versions. Use lock files (`go.sum`, `pnpm-lock.yaml`).
- Run vulnerability scans in CI (`govulncheck`, `pnpm audit`).
- No new dependencies without review of license and maintenance status.
- Prefer stdlib over third-party for security-sensitive operations (crypto, hashing).

## Cryptography

- Never roll your own crypto. Use `crypto/rand`, `crypto/sha256`, `golang.org/x/crypto`.
- Passwords: bcrypt or argon2id with cost factor ≥ 12. Never MD5/SHA1 for passwords.
- Token generation: `crypto/rand` with ≥ 128 bits of entropy.
- Encrypt at rest for PII and sensitive configuration. Key rotation must be planned.

## Audit Logging

- All state-changing operations on sensitive resources write an audit row.
- Audit rows include: actor ID, action, resource type, resource ID, timestamp, IP.
- Audit rows are append-only. No UPDATE or DELETE on audit tables.
- Logs ≠ audit rows. Structured logs go to stdout; audit rows go to the database.

## Code Review Checklist (Security)

Before merging, verify:
- [ ] No new SQL string interpolation
- [ ] No new secrets in code or config files
- [ ] New endpoints have auth + permission check
- [ ] Error responses don't leak internal details
- [ ] Input validation at every new entry point
- [ ] Audit row written for state-changing actions
