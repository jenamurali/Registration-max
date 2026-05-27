# Logical Components — Unit 1: Foundation

## Middleware Stack Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    FastAPI Application                   │
│                                                         │
│  ┌───────────────────────────────────────────────────┐  │
│  │              Middleware Layer                      │  │
│  │  ┌─────────────────┐  ┌────────────────────────┐  │  │
│  │  │ CorrelationID   │  │ RequestIDMiddleware     │  │  │
│  │  │ Middleware       │  │ → Generate UUID        │  │  │
│  │  │                 │  │ → Set response header   │  │  │
│  │  └────────┬────────┘  └───────────┬────────────┘  │  │
│  │           │                       │                │  │
│  │           ▼                       ▼                │  │
│  │  ┌─────────────────┐  ┌────────────────────────┐  │  │
│  │  │ SecurityHeaders │  │ SecurityMiddleware     │  │  │
│  │  │ Middleware       │  │ → CSP, HSTS, X-CTO,    │  │  │
│  │  │                 │  │   XFO, Referrer-Policy │  │  │
│  │  └────────┬────────┘  └───────────┬────────────┘  │  │
│  │           │                       │                │  │
│  │           ▼                       ▼                │  │
│  │  ┌─────────────────┐  ┌────────────────────────┐  │  │
│  │  │ Auth            │  │ AuthMiddleware         │  │  │
│  │  │ Middleware       │  │ → Validate JWT         │  │  │
│  │  │                 │  │ → Set user context      │  │  │
│  │  └────────┬────────┘  └───────────┬────────────┘  │  │
│  │           │                       │                │  │
│  │           ▼                       ▼                │  │
│  │  ┌─────────────────┐  ┌────────────────────────┐  │  │
│  │  │ Rate Limit      │  │ RateLimitMiddleware     │  │  │
│  │  │ Middleware       │  │ → Check login attempts │  │  │
│  │  │                 │  │ → In-memory state       │  │  │
│  │  └────────┬────────┘  └───────────┬────────────┘  │  │
│  │           │                       │                │  │
│  └───────────┼───────────────────────┼────────────────┘  │
│              │                       │                    │
│              ▼                       ▼                    │
│  ┌───────────────────────────────────────────────────┐  │
│  │                 Route Handlers                    │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────────┐   │  │
│  │  │ Auth     │  │ Event    │  │ Registration │   │  │
│  │  │ Router   │  │ Router   │  │ Router       │   │  │
│  │  └──────────┘  └──────────┘  └──────────────┘   │  │
│  └───────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────┘
```

## Dependency Injection Chain

```
app/deps.py
│
├── get_db_session() → AsyncSession
│     └── yields session per request
│
├── get_uow(session) → UnitOfWork
│     └── Wraps session, provides repositories
│
├── get_auth_service(uow) → AuthService
│     └── Login, token generation, validation
│
├── get_current_user(token=Depends(oauth2_scheme), auth_service)
│     └── Validates token, returns User
│
├── require_admin(current_user)
│     └── Checks user.role == "admin"
│
└── require_role(role: str)
      └── Factory for role-based dependency
```

## Component Wiring

### main.py — App Factory
```
create_app() -> FastAPI:
  1. Load config from env vars
  2. Create FastAPI instance (title, version, docs_url)
  3. Add middleware stack (correlation_id, security_headers, auth, rate_limit)
  4. Add exception handlers (app_exception, validation_error, generic)
  5. Register routers with /api/v1 prefix
  6. Register startup/shutdown events (DB engine init/dispose)
  7. Return app
```

### Startup/Shutdown Lifecycle
```
Startup:
  1. Create async SQLAlchemy engine
  2. Verify DB connectivity (optional, configurable)
  3. Log "Application started"

Shutdown:
  1. Dispose SQLAlchemy engine (close all connections)
  2. Log "Application stopped"
```

## Exception Handler Wiring

```
app/errors.py
│
├── AppException(BaseException)
│     ├── status_code: int
│     └── detail: str
│
├── app_exception_handler(request, exc: AppException)
│     └── Returns JSONResponse(status_code, content={"detail": exc.detail})
│
├── validation_exception_handler(request, exc: RequestValidationError)
│     └── Returns 422 with field-level errors
│
├── integrity_error_handler(request, exc: IntegrityError)
│     └── Returns 409 with generic conflict message
│
└── generic_exception_handler(request, exc: Exception)
      └── Logs full traceback, returns 500 generic message
```

## File Structure (Unit 1 Deliverables)

```
app/
├── main.py              # FastAPI app factory
├── config.py            # Settings from env vars
├── database.py          # Engine, session factory
├── deps.py              # Dependency injection
├── errors.py            # Exception classes + handlers
├── models/
│   ├── __init__.py
│   ├── base.py          # Base model class
│   └── user.py          # User model
├── schemas/
│   ├── __init__.py
│   ├── auth.py          # LoginRequest, TokenResponse
│   └── user.py          # UserCreate, UserResponse
├── repositories/
│   ├── __init__.py
│   ├── base.py          # BaseRepository[T]
│   └── user_repo.py     # UserRepository
├── unit_of_work.py      # UnitOfWork
├── services/
│   ├── __init__.py
│   └── auth_service.py  # AuthService
├── routers/
│   ├── __init__.py
│   └── auth.py          # /auth/login, /auth/refresh
└── middleware/
    ├── __init__.py
    ├── correlation_id.py
    ├── security_headers.py
    ├── auth.py
    └── rate_limit.py
```
