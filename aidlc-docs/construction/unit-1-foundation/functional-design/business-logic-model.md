# Business Logic Model — Unit 1: Foundation

## 1. Base Repository Pattern

### Generic Base Repository
```
class BaseRepository[T]:
    model: type[T]                     # SQLAlchemy model class

    get_by_id(id: int) -> T | None     # Single entity by PK
    get_all() -> List[T]               # All entities
    add(entity: T) -> T                # Insert and return
    update(entity: T) -> T             # Update and return
    delete(entity: T) -> None          # Hard delete
    get_paginated(skip, limit) -> Tuple[List[T], int]  # Paginated list + total count
```

### User Repository
Extends BaseRepository[User]:
- `get_by_username(username: str) -> User | None`
- `get_by_email(email: str) -> User | None`

## 2. Unit of Work Pattern

### UOW Lifecycle
```
Request Start
  │
  ├── FastAPI dependency yields UOW
  │     └── UOW.__init__()
  │           └── Creates SQLAlchemy async session
  │
  ├── Service uses UOW
  │     ├── Access repositories via UOW.repo_name
  │     ├── Multiple repo operations within one session
  │     └── Service calls uow.commit() on success
  │
  ├── FastAPI dependency teardown
  │     ├── If uncommitted: uow.rollback()
  │     └── Session closed
  │
  Request End
```

### UOW Interface
```
class UnitOfWork:
    session: AsyncSession              # SQLAlchemy async session

    __aenter__() -> UnitOfWork         # Async context manager enter
    __aexit__(exc_type, exc, tb)       # Rollback on exception, close session
    async commit() -> None             # Commit current transaction
    async rollback() -> None           # Rollback current transaction
    async close() -> None              # Close session

    # Repository properties (lazy-loaded)
    users: UserRepository
```

## 3. Authentication Flow

### Login Flow
```
POST /api/v1/auth/login {username, password}
  │
  ├── AuthService.authenticate(username, password)
  │     ├── UserRepo.get_by_username(username)
  │     ├── If not found: raise 401
  │     ├── Verify password_hash with passlib
  │     ├── If mismatch: raise 401
  │     ├── If not is_active: raise 403
  │     └── Generate token pair
  │
  ├── Generate access_token (JWT, 30 min)
  │     └── Payload: {sub: user.id, role: user.role, exp, iat, type: "access"}
  │
  ├── Generate refresh_token (JWT, 7 days)
  │     └── Payload: {sub: user.id, exp, iat, type: "refresh"}
  │
  └── Return {access_token, refresh_token, token_type: "bearer"}
```

### Token Refresh Flow
```
POST /api/v1/auth/refresh {refresh_token}
  │
  ├── Validate refresh_token (signature, expiry)
  ├── Verify token type == "refresh"
  ├── UserRepo.get_by_id(payload.sub)
  ├── If not found or inactive: raise 401
  ├── Generate new access_token (30 min)
  └── Return {access_token, token_type: "bearer"}
```

### Token Validation (Middleware)
```
Every protected request:
  │
  ├── Extract Authorization: Bearer <token>
  ├── Validate JWT (signature, expiry, audience, issuer)
  ├── Verify token type == "access"
  ├── Extract payload: {sub, role}
  ├── Set request.state.user_id, request.state.role
  └── If invalid: return 401

Role check (for admin routes):
  ├── If request.state.role != "admin": return 403
```

## 4. Database Configuration

### Connection Setup
- Connection string from environment variable `DATABASE_URL`
- SQLAlchemy async engine with connection pooling (pool_size=10, max_overflow=20)
- Async session factory (`async_sessionmaker`)
- Echo SQL in debug mode only (configurable)

### Transaction Management
- One session per HTTP request (via FastAPI dependency yield)
- UOW.commit() flushes and commits
- Rollback on unhandled exceptions
- Nested transactions not supported (flat transaction per request)
