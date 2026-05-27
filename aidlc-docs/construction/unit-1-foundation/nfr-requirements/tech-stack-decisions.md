# Tech Stack Decisions — Unit 1: Foundation

## Core Stack (Decided in Requirements Analysis)

| Layer | Choice | Version |
|-------|--------|---------|
| Runtime | Python | 3.12+ |
| Web Framework | FastAPI | 0.115.x |
| ORM | SQLAlchemy (async) | 2.0.x |
| Database Driver | pyodbc + aioodbc | latest |
| Database | SQL Server | 2022 |

## Unit 1 Specific Libraries

| Library | Version | Purpose | Rationale |
|---------|---------|---------|-----------|
| fastapi | 0.115.x | Web framework | Async-native, auto docs, Pydantic integration |
| uvicorn | 0.34.x | ASGI server | Fast, production-ready |
| sqlalchemy | 2.0.x | ORM (async) | Mature, async support, UOW-friendly |
| pyodbc | 5.x | SQL Server driver | Required for SQL Server connectivity |
| pydantic | 2.x | Validation/schemas | Built into FastAPI |
| python-jose | 3.3.x | JWT handling | Well-maintained, supports HS256 |
| passlib[bcrypt] | 1.7.x | Password hashing | Standard Python library, bcrypt support |
| python-multipart | 0.0.x | Form/file parsing | Required by FastAPI for OAuth2 forms |
| uuid (stdlib) | - | Correlation IDs | No extra dependency needed |
| logging (stdlib) | - | Structured logging | Configured as JSON formatter |

## Configuration

All configuration via environment variables:

| Variable | Purpose | Default |
|----------|---------|---------|
| DATABASE_URL | SQL Server connection string | Required |
| JWT_SECRET_KEY | JWT signing secret | Required |
| JWT_ALGORITHM | JWT algorithm | HS256 |
| ACCESS_TOKEN_EXPIRE_MINUTES | Access token lifetime | 30 |
| REFRESH_TOKEN_EXPIRE_DAYS | Refresh token lifetime | 7 |
| CORS_ORIGINS | Allowed origins (comma-separated) | http://localhost:3000 |
| LOG_LEVEL | Logging level | INFO |
| MAX_REQUEST_SIZE_MB | Max request body size | 1 |

## Dependency File

```
# requirements.txt
fastapi==0.115.*
uvicorn[standard]==0.34.*
sqlalchemy[asyncio]==2.0.*
pyodbc==5.*
pydantic==2.*
python-jose[cryptography]==3.3.*
passlib[bcrypt]==1.7.*
python-multipart==0.0.*
```
