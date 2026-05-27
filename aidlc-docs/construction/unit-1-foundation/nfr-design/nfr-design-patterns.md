# NFR Design Patterns — Unit 1: Foundation

## Security Patterns

### Pattern 1: JWT Middleware Chain
```
Request
  │
  ├── CorrelationIDMiddleware  → Generate X-Request-ID
  ├── SecurityHeadersMiddleware → Apply security headers
  ├── AuthMiddleware           → Validate JWT, set user context
  │     ├── Extract Bearer token
  │     ├── Verify signature (HS256)
  │     ├── Check expiry
  │     ├── Extract payload: {sub, role}
  │     └── Set request.state.user_id, request.state.role
  ├── RateLimitMiddleware      → Check login attempt limits
  └── Router                   → Handle request
```

### Pattern 2: Deny-by-Default Authorization
- All routes protected by default via `Depends(get_current_user)`
- Public routes explicitly decorated with `@public` marker
- Role check via `Depends(require_role("admin"))` for admin endpoints
- No authorization logic in route handlers — all in dependencies

### Pattern 3: Password Hashing Strategy
- bcrypt with 12 rounds via `passlib.context.CryptContext`
- Schemes: `["bcrypt"]`, deprecated: `"auto"`
- Hash on user creation and password change
- Verify on each login attempt
- Never log or return hashes in responses

### Pattern 4: CORS Restriction
- Whitelist of allowed origins from `CORS_ORIGINS` env var
- No wildcard on authenticated endpoints
- Methods: GET, POST, PUT, DELETE, PATCH
- Headers: Authorization, Content-Type
- Max age: 600 seconds

## Resilience Patterns

### Pattern 5: Graceful Error Handling
```
Exception Hierarchy:
  AppException (base)
    ├── AuthException (401)
    ├── ForbiddenException (403)
    ├── NotFoundException (404)
    ├── ConflictException (409)
    └── ValidationException (422)

Global Exception Handler:
  ├── AppException → Return structured error with status code
  ├── ValidationError (Pydantic) → Return 422 with field details
  ├── IntegrityError (SQLAlchemy) → Return 409 with generic message
  └── Exception → Log full traceback, return 500 generic
```

### Pattern 6: Connection Pool Resilience
- Pool timeout: 30 seconds max wait
- Pool pre-ping: True (validate connections before use)
- Dispose on app shutdown
- Auto-recycle after 1 hour

### Pattern 7: Fail-Closed Authorization
- If JWT validation fails → 401 (not 200 with empty user)
- If role check fails → 403 (not silently downgraded)
- If DB is unreachable during auth → 503 (not bypassed)
- Never default to authenticated state on error

## Performance Patterns

### Pattern 8: Async Throughout
- All database operations async (SQLAlchemy 2.0 async API)
- All route handlers async
- No blocking I/O in request path
- UOW session management uses async context manager

### Pattern 9: Connection Pool Tuning
- pool_size: 5 (base connections)
- max_overflow: 10 (surge capacity)
- pool_timeout: 30 (seconds to wait for connection)
- pool_recycle: 3600 (recycle connections after 1 hour)
- pool_pre_ping: True (validate before use)

### Pattern 10: Lazy-Loaded Repositories in UOW
- Repository instances created on first access (not at UOW init)
- Uses `@property` with internal cache per UOW instance
- Avoids unnecessary repository instantiation for simple requests

## Observability Patterns

### Pattern 11: Structured Logging
```
Log Entry Format:
{
  "timestamp": "2026-05-26T10:30:00.000Z",
  "level": "INFO",
  "request_id": "uuid",
  "user_id": "int|null",
  "method": "GET",
  "path": "/api/v1/events",
  "status_code": 200,
  "duration_ms": 45.2,
  "message": "Request completed"
}
```
- JSON format in production, text in development
- Controlled by `LOG_FORMAT` env var ("json" or "text")

### Pattern 12: Auth Audit Trail
- Login success: INFO with user_id
- Login failure: WARNING with username, reason
- Token refresh: INFO with user_id
- Rate limit hit: WARNING with username
- Account lockout: WARNING with username
