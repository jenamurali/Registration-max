# Business Rules — Unit 1: Foundation

## Authentication Rules

### BR-AUTH-01: Password Policy
- Minimum 8 characters required
- Must be hashed using bcrypt via passlib (adaptive algorithm)
- Never stored or logged in plaintext
- Never returned in API responses

### BR-AUTH-02: Login Rate Limiting
- Maximum 5 failed login attempts per username in 15 minutes
- After 5 failures, account locked for 15 minutes
- Successful login resets the counter

### BR-AUTH-03: Token Security
- Access tokens expire after 30 minutes
- Refresh tokens expire after 7 days
- Refresh token rotation: old refresh token invalidated on use
- JWT signing algorithm: HS256 (or RS256 if key pair available)
- Tokens include: sub (user id), role, exp, iat, type (access/refresh)

### BR-AUTH-04: Session Invalidation
- Server-side logout invalidates refresh token
- Password change invalidates all existing tokens for that user
- Account deactivation immediately invalidates all tokens

## Authorization Rules

### BR-AUTH-05: Role-Based Access
- **Admin**: Full access to all endpoints
- **Operator**: Access to all non-user-management endpoints
- Public routes (no auth required): `/api/v1/auth/login`, `/api/v1/auth/refresh`, `/docs`, `/openapi.json`

### BR-AUTH-06: Deny by Default
- All routes require authentication unless explicitly marked as public
- Missing or invalid token returns 401
- Insufficient role returns 403

## Data Integrity Rules

### BR-DATA-01: Base Entity Timestamps
- `created_at` auto-set on insert, never modified after
- `updated_at` auto-updated on every change
- Both use server time (UTC)

### BR-DATA-02: Unit of Work Transactions
- All operations within a request share one database transaction
- Commit happens once at the end of successful processing
- Any exception triggers full rollback
- No partial commits allowed

## Error Handling Rules

### BR-ERR-01: API Error Responses
- 400: Validation errors (return field-level details)
- 401: Authentication required or token expired
- 403: Insufficient permissions
- 404: Resource not found
- 409: Conflict (duplicate username, email, etc.)
- 422: Unprocessable entity (business rule violation)
- 500: Internal server error (generic message only, no stack trace)

### BR-ERR-02: Global Error Handler
- Catch all unhandled exceptions at FastAPI level
- Log full error with traceback to application logs
- Return generic "Internal server error" to client
- Never expose database details, file paths, or framework internals

## Security Header Rules

### BR-SEC-01: HTTP Security Headers
Applied via middleware to all responses:
- `Content-Security-Policy: default-src 'self'`
- `Strict-Transport-Security: max-age=31536000; includeSubDomains`
- `X-Content-Type-Options: nosniff`
- `X-Frame-Options: DENY`
- `Referrer-Policy: strict-origin-when-cross-origin`

## Logging Rules

### BR-LOG-01: Structured Logging
- Every request logged with: timestamp, request_id (correlation ID), method, path, status_code, duration_ms
- Auth events logged: login success, login failure, token refresh, logout
- Log level: INFO for normal operations, WARNING for auth failures, ERROR for exceptions
- Never log: passwords, tokens, PII (emails truncated: `us***@domain.com`)

### BR-LOG-02: Correlation ID
- Generate UUID per request (middleware)
- Pass through all service calls
- Include in all log entries for tracing
- Return in response header `X-Request-ID`

## Input Validation Rules

### BR-VAL-01: All Endpoints
- Validate all path parameters, query parameters, and request bodies
- Use Pydantic models for all request/response schemas
- String fields: enforce max_length on all inputs
- Request body: enforce size limit (configurable, default 1MB)
