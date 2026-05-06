---
name: api-design-rules
description: REST API design rules — consistent error envelope, pagination via cursor, idempotency keys, and HTTP status discipline.
kind: rules
---

# API Design Rules

Rules for designing and reviewing REST APIs. Apply these when creating new endpoints, reviewing existing ones, or generating OpenAPI specs.

## URL Structure

- Resources are plural nouns: `/users`, `/organizations`, `/mcp-servers`.
- Sub-resources express ownership: `/organizations/{id}/members`.
- Actions that don't map to CRUD go on a sub-resource: `POST /jobs/{id}/cancel` not `PUT /jobs/{id}?action=cancel`.
- No verbs in path segments: `/users/{id}/deactivate` not `/deactivateUser/{id}`.
- Use kebab-case for multi-word segments: `/mcp-servers`, `/audit-events`.
- Path params use `{id}` format (OpenAPI standard), not `:id` (Express-style).

## HTTP Method Semantics

| Method | Semantics | Idempotent | Body |
|--------|-----------|------------|------|
| GET | Read, no side effects | Yes | No |
| POST | Create or trigger action | No | Yes |
| PUT | Replace entire resource | Yes | Yes |
| PATCH | Partial update | No | Yes |
| DELETE | Remove | Yes | No |

Never use GET for state-changing operations (cache poisoning, link prefetch attacks).

## Status Codes

| Code | Use when |
|------|---------|
| 200 | Successful GET, PUT, PATCH, DELETE with response body |
| 201 | Successful POST that creates a resource — include `Location` header |
| 204 | Successful DELETE or action with no response body |
| 400 | Client error: malformed JSON, missing required field, failed validation |
| 401 | Not authenticated |
| 403 | Authenticated but not authorized |
| 404 | Resource not found |
| 409 | Conflict: duplicate create, version mismatch |
| 422 | Semantically invalid input (valid JSON but business rule violation) |
| 429 | Rate limited — include `Retry-After` header |
| 500 | Server error — generic message, no internal details in body |
| 502 | Upstream dependency failed |

Never return 200 with an error payload. Use 4xx/5xx.

## Error Envelope

All error responses use this shape:

```json
{
  "error": {
    "code": "VALIDATION_FAILED",
    "message": "name is required",
    "field": "name"
  }
}
```

- `code`: machine-readable string constant (SCREAMING_SNAKE_CASE).
- `message`: human-readable, safe to display in UI.
- `field`: optional, for validation errors on a specific field.
- Never include stack traces, SQL errors, or internal details.

## Pagination

Use cursor-based pagination for all list endpoints:

```json
{
  "items": [...],
  "next_cursor": "eyJpZCI6IjEyMyJ9",
  "has_more": true
}
```

Request: `GET /resources?limit=50&cursor=<opaque_string>`

- Default limit: 50. Maximum limit: 200.
- Cursors are opaque base64-encoded strings. Never expose raw DB IDs or offsets.
- No offset/page pagination — it's inconsistent under concurrent writes.

## Idempotency

- PUT and DELETE must be idempotent.
- For non-idempotent POST operations (payments, emails, job triggers), support `Idempotency-Key` header.
- Store idempotency keys for at least 24 hours. Return the same response for duplicate keys.

## Request/Response Design

- Request bodies: always JSON. `Content-Type: application/json` required.
- Response bodies: always JSON. Set `Content-Type: application/json; charset=utf-8`.
- Timestamps: ISO 8601 / RFC 3339 in UTC: `"2026-05-06T08:00:00Z"`.
- IDs: opaque strings, not sequential integers. Prefix by type: `usr_`, `org_`, `skl_`.
- Optional fields: omit from response rather than returning `null`.
- Boolean fields: `is_active`, not `active` or `activated`.

## Versioning

- Version in URL path: `/api/v1/`, `/api/v2/`.
- Never break existing clients within a major version.
- Deprecate fields with `X-Deprecated-Field` response header before removal.
- Breaking changes (field rename, type change, removal) require a new major version.

## Security

- All authenticated endpoints: verify token before doing any DB work.
- Never expose internal IDs in error messages.
- Validate `Content-Type` on POST/PUT/PATCH to prevent content sniffing attacks.
- Set `X-Content-Type-Options: nosniff` and `X-Frame-Options: DENY` on all responses.
