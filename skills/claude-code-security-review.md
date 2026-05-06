---
name: claude-code-security-review
description: Security review skill for Claude Code — OWASP checks, secret detection, auth review, and remediation guidance.
kind: skill
---

# Claude Code Security Review

Automated security review skill for code written or modified by Claude Code. Run this skill before submitting any PR that touches auth, data handling, or external interfaces.

## When to Activate

Activate this skill when:
- Adding or modifying HTTP endpoints
- Changing authentication or authorization logic
- Adding new dependencies
- Handling file uploads, user input, or external API responses
- Modifying database queries or schema
- Touching cryptography, token generation, or session management

## OWASP Top 10 Checks

### A01 — Broken Access Control
- [ ] Every endpoint verifies authentication before doing work
- [ ] Authorization (role/permission) checked after authentication
- [ ] Resource ownership verified: `WHERE id = $1 AND user_id = $currentUser`
- [ ] Admin endpoints not reachable by lower-privilege users
- [ ] CORS origin allowlist is explicit, never `*` for authenticated paths

### A02 — Cryptographic Failures
- [ ] No sensitive data transmitted in plain HTTP
- [ ] Passwords hashed with bcrypt/argon2id (cost ≥ 12), never MD5/SHA1
- [ ] Tokens generated with `crypto/rand` (≥ 128 bits)
- [ ] No sensitive data in URL query params (logged by servers/proxies)
- [ ] Cookies: `HttpOnly`, `Secure`, `SameSite=Strict`

### A03 — Injection
- [ ] All SQL uses parameterized queries. No string concatenation into SQL.
- [ ] Shell commands use argument arrays, not interpolated strings
- [ ] File paths sanitized against path traversal (`../`)
- [ ] Template rendering with user input uses auto-escaping

### A04 — Insecure Design
- [ ] Sensitive operations rate-limited
- [ ] Bulk operations have pagination/limits (no "fetch all 1M rows")
- [ ] New features have threat model in PR description

### A05 — Security Misconfiguration
- [ ] Debug endpoints/flags disabled in production builds
- [ ] Error responses return generic messages, not stack traces
- [ ] Security headers set: `X-Content-Type-Options`, `X-Frame-Options`
- [ ] No hardcoded credentials in config files or defaults

### A06 — Vulnerable Components
- [ ] New dependencies scanned for known CVEs before merging
- [ ] Dependency versions pinned (no `latest` or `^` in lockfiles)
- [ ] `govulncheck` / `pnpm audit` passing in CI

### A07 — Identification and Authentication Failures
- [ ] Session tokens invalidated on logout
- [ ] Account lockout after repeated auth failures
- [ ] Password reset tokens are single-use and short-lived (≤ 1 hour)
- [ ] No weak default credentials

### A08 — Software and Data Integrity
- [ ] Dependencies fetched from official registries with integrity hashes
- [ ] User-uploaded files validated (type, size, content — not just extension)
- [ ] Deserialization of untrusted data avoided; if unavoidable, validated before use

### A09 — Security Logging and Monitoring
- [ ] Auth failures logged with actor, timestamp, IP
- [ ] State-changing admin actions produce audit rows
- [ ] Logs do NOT contain: passwords, tokens, session IDs, PII, full request bodies
- [ ] Alerts configured for repeated auth failures, mass data access

### A10 — Server-Side Request Forgery (SSRF)
- [ ] URLs fetched from user input validated against allowlist
- [ ] Internal network addresses (`127.0.0.1`, `169.254.*`, `10.*`) blocked for user-supplied URLs
- [ ] Response bodies from user-supplied URLs not reflected directly to other users

## Secret Detection

Scan for accidental secrets before committing:

Patterns to search:
```
api_key\s*=\s*["'][^"']{10,}["']
password\s*=\s*["'][^"']{4,}["']
secret\s*=\s*["'][^"']{8,}["']
-----BEGIN.*PRIVATE KEY-----
ghp_[A-Za-z0-9]{36}
sk-[A-Za-z0-9]{48}
```

If found: rotate the secret immediately, then remove from code. Do not just remove from code — the secret is already in git history.

## PR Security Section Template

For every PR touching security-sensitive code, include in the PR body:

```
## Security

- **Who can call this?** [public / any authenticated user / role X only]
- **Auth boundary:** [which middleware gates this?]
- **Input validation:** [what's validated, where]
- **Audit row:** [yes — table X / no — not state-changing]
- **Rate limit:** [yes — N req/min / no — low abuse surface]
- **Sensitive data in response:** [no / yes — what, and why necessary]
```

## Automated Checks

Run before merging:

```bash
# Go
govulncheck ./...
go vet ./...
staticcheck ./...

# JavaScript/TypeScript
pnpm audit
pnpm exec eslint --rule 'no-eval: error' .

# Secret scanning
git diff HEAD~1 | grep -E '(api_key|password|secret|token)\s*=\s*["\x27][^"\x27]{8,}'
```
