# Code Generation Plan — Unit 1: Foundation

## Unit Context
- **Stories**: Auth (JWT+RABC), database connectivity, security headers, logging, base patterns
- **Dependencies**: None (foundation unit)
- **Models**: User (with Base)
- **Repositories**: BaseRepository, UserRepository
- **Services**: AuthService
- **Routers**: Auth (login, refresh)

## Generation Steps

### Project Setup
- [ ] Step 1: Create `requirements.txt` with pinned dependencies
- [ ] Step 2: Create `app/__init__.py`
- [ ] Step 3: Create `app/config.py` — Settings from env vars

### Database Layer
- [ ] Step 4: Create `app/database.py` — Engine, async session factory
- [ ] Step 5: Create `app/models/__init__.py`
- [ ] Step 6: Create `app/models/base.py` — Base model with timestamps
- [ ] Step 7: Create `app/models/user.py` — User model

### Schemas
- [ ] Step 8: Create `app/schemas/__init__.py`
- [ ] Step 9: Create `app/schemas/auth.py` — LoginRequest, TokenResponse, RefreshRequest
- [ ] Step 10: Create `app/schemas/user.py` — UserCreate, UserResponse

### Repository Layer
- [ ] Step 11: Create `app/repositories/__init__.py`
- [ ] Step 12: Create `app/repositories/base.py` — Generic BaseRepository[T]
- [ ] Step 13: Create `app/repositories/user_repo.py` — UserRepository

### Unit of Work
- [ ] Step 14: Create `app/unit_of_work.py` — UnitOfWork with lazy repos

### Error Handling
- [ ] Step 15: Create `app/errors.py` — Exception classes and handlers

### Services
- [ ] Step 16: Create `app/services/__init__.py`
- [ ] Step 17: Create `app/services/auth_service.py` — AuthService

### Middleware
- [ ] Step 18: Create `app/middleware/__init__.py`
- [ ] Step 19: Create `app/middleware/correlation_id.py`
- [ ] Step 20: Create `app/middleware/security_headers.py`
- [ ] Step 21: Create `app/middleware/auth.py`
- [ ] Step 22: Create `app/middleware/rate_limit.py`

### Dependency Injection
- [ ] Step 23: Create `app/deps.py` — All DI functions

### Routers
- [ ] Step 24: Create `app/routers/__init__.py`
- [ ] Step 25: Create `app/routers/auth.py` — /auth/login, /auth/refresh

### App Entry Point
- [ ] Step 26: Create `app/main.py` — FastAPI app factory

### Tests
- [ ] Step 27: Create `tests/__init__.py`
- [ ] Step 28: Create `tests/conftest.py` — Test fixtures
- [ ] Step 29: Create `tests/test_auth.py` — Auth endpoint tests
- [ ] Step 30: Create `tests/test_uow.py` — Unit of Work tests
