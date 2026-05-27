# NFR Requirements — Unit 1: Foundation

## Performance Requirements

| Requirement | Target | Measurement |
|-------------|--------|-------------|
| Login endpoint latency | < 300ms p95 | Response time excluding network |
| Token validation | < 10ms | Middleware processing overhead |
| DB connection acquire | < 5ms | Pool checkout time |
| API response (authenticated) | < 200ms p95 | Full request lifecycle |

## Scalability Requirements

| Requirement | Target |
|-------------|--------|
| Concurrent requests | 50+ simultaneous |
| Connection pool | 5 base + 10 overflow (15 max) |
| Connection pool timeout | 30s wait max |
| Session cleanup | Auto-close on request teardown |

## Availability

- Stateless API design — any instance can handle any request
- No session affinity required
- Graceful degradation: auth failures return 401, not 500

## Security Requirements

| Requirement | Implementation |
|-------------|---------------|
| Password hashing | bcrypt, 12 rounds via passlib |
| JWT signing | HS256, secret from env var |
| Token expiry | Access 30min, Refresh 7 days |
| Rate limiting | 5 failed logins / 15 min per username |
| Input validation | Pydantic models on all inputs |
| Security headers | CSP, HSTS, X-Content-Type-Options, X-Frame-Options, Referrer-Policy |
| CORS | Restricted to configured origins, no wildcard on authenticated endpoints |
| Request size limit | 1 MB default |

## Reliability Requirements

| Requirement | Implementation |
|-------------|---------------|
| Error handling | Global exception handler, no stack traces to client |
| DB transaction safety | UOW commit/rollback, no partial commits |
| Resource cleanup | Session always closed (finally/yield teardown) |
| Connection resilience | Auto-reconnect, pool timeout |

## Observability

| Requirement | Implementation |
|-------------|---------------|
| Structured logging | JSON-formatted logs with correlation ID |
| Request logging | Every request: method, path, status, duration |
| Auth logging | Login success/failure, token refresh |
| Log levels | INFO (normal), WARNING (auth failures), ERROR (exceptions) |
| PII protection | No passwords, tokens, or full emails in logs |

## Maintainability

- All config via environment variables (12-factor app)
- Dependency injection for testability
- Async/await throughout for consistency
- Type hints on all public interfaces
