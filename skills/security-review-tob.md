---
name: security-review-tob
description: Trail of Bits security review methodology — threat modelling, vulnerability classes, and remediation patterns.
kind: skill
---

# Security Review (Trail of Bits)

Structured security review methodology inspired by Trail of Bits' engineering practices. Apply when reviewing code, designing systems, or before shipping security-sensitive features.

## Threat Modelling

Before reviewing code, build the threat model:

1. **Assets**: What are we protecting? (user data, credentials, session tokens, admin actions)
2. **Attackers**: Who might attack? (external internet, authenticated users, insider threat, compromised dependency)
3. **Entry points**: Where does untrusted data enter? (HTTP body, query params, headers, files, env vars, DB values)
4. **Trust boundaries**: Where does data cross from untrusted to trusted? Each boundary must validate.

## Vulnerability Classes to Check

### Injection
- SQL injection via string interpolation (`fmt.Sprintf`, template strings in queries)
- Command injection via `exec.Command` with unsanitized input
- Path traversal via `..` in file paths from user input
- Template injection via user-controlled template strings

**Fix pattern:** Parameterize everything. Never concatenate user input into commands, queries, or paths.

### Authentication & Session
- Missing authentication checks on non-public endpoints
- Session tokens in URLs (visible in logs, Referer headers)
- Predictable session token generation (Math.random, sequential IDs)
- Missing expiry on tokens/sessions
- Password hashing with weak algorithms (MD5, SHA1, unsalted SHA256)

**Fix pattern:** Use `crypto/rand` for tokens (≥128 bits). bcrypt/argon2id for passwords. HttpOnly+Secure cookies.

### Authorization
- Missing authorization after authentication (authn ≠ authz)
- Horizontal privilege escalation (user A accesses user B's resources)
- Vertical privilege escalation (normal user accesses admin endpoints)
- IDOR (Insecure Direct Object Reference) — using user-supplied IDs without ownership check

**Fix pattern:** Check ownership: `WHERE id = $1 AND owner_id = $2`. Never trust client-supplied resource IDs alone.

### Cryptography
- Rolling custom crypto
- Hardcoded keys or IVs
- ECB mode block cipher
- Weak PRNG for security-sensitive values
- Key material logged or stored in plain text

**Fix pattern:** Use standard library crypto primitives. Never log key material.

### Input Validation
- Missing length checks (DoS via large payloads)
- Missing type validation (integer overflow, type confusion)
- Accepting arbitrary file extensions for upload
- Trusting client-supplied content types

**Fix pattern:** Validate at every trust boundary. Reject early. Allowlist over denylist.

### Information Disclosure
- Stack traces or SQL errors in HTTP responses
- Internal hostnames, IPs, or file paths in error messages
- Verbose 404s that reveal valid resource IDs
- Debug endpoints left enabled in production

**Fix pattern:** Log details server-side. Return generic messages to clients.

### Dependency Risk
- Known CVEs in pinned dependencies
- Unpinned dependencies (supply chain attack surface)
- Dependencies with excessive filesystem/network access
- Transitive dependencies from untrusted maintainers

**Fix pattern:** Pin all dependencies. Run `govulncheck`/`npm audit` in CI. Review new transitive deps.

## Code Review Protocol

For each file changed, ask:

1. **Entry points**: Does this file receive untrusted input? Is it validated?
2. **Auth boundary**: Is this endpoint authenticated? Authorized?
3. **Data flow**: Does user input reach a DB query, shell command, file path, or template?
4. **Error handling**: Do error responses leak internal details?
5. **Crypto**: Are any keys, tokens, or hashes generated here? Are they using correct primitives?
6. **Audit trail**: Does a state-changing action write an audit row?

## Severity Classification

| Severity | Criteria | Response |
|----------|----------|----------|
| Critical | Remote code execution, auth bypass, mass data exfil | Block merge, immediate escalation |
| High | Privilege escalation, targeted data exfil, SSRF | Block merge |
| Medium | Information disclosure, CSRF, rate-limit bypass | Track, fix before next release |
| Low | Missing headers, verbose errors, minor info leak | Advisory |
| Informational | Best practice, defense-in-depth | Document |

## Remediation Checklist

After identifying vulnerabilities:

- [ ] Each finding has: file+line, severity, description, reproduction steps, fix recommendation
- [ ] Root cause addressed (not just the symptom)
- [ ] Fix reviewed separately — patches introduce new bugs
- [ ] Regression test added for each Critical/High finding
- [ ] Audit log updated if the vuln involved unauthorized access

*Methodology inspired by Trail of Bits security review practices.*
