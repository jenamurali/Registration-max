# Registration System Backend

Backend API for event registration management built with Python/FastAPI, SQLAlchemy 2.0 async, and Repository + Unit of Work pattern.

## Quick Start

```bash
# 1. Create virtual environment
python -m venv venv

# 2. Activate (Windows)
venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment (edit .env with your settings)
# Default uses SQLite for local dev — no setup needed

# 5. Start server
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Open http://localhost:8000/docs for interactive API documentation.

## Create Admin User

```bash
curl -X POST http://localhost:8000/api/v1/auth/signup \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","email":"admin@example.com","password":"password123","role":"admin"}'
```

Then login at `POST /api/v1/auth/login` to get a JWT token.

## Run Tests

```bash
pytest tests/ -v
```

## Environment Variables (.env)

| Variable | Default | Description |
|----------|---------|-------------|
| DATABASE_URL | sqlite+aiosqlite:///./app.db | Database connection |
| JWT_SECRET_KEY | (required in production) | JWT signing secret |
| JWT_ALGORITHM | HS256 | JWT algorithm |
| ACCESS_TOKEN_EXPIRE_MINUTES | 30 | Access token lifetime |
| REFRESH_TOKEN_EXPIRE_DAYS | 7 | Refresh token lifetime |
| CORS_ORIGINS | http://localhost:3000 | Allowed CORS origins |
| LOG_LEVEL | INFO | Logging level |
| LOG_FORMAT | text | text or json |

## Architecture

```
Router → Service → UOW → Repository → SQLAlchemy → DB
```

## API Modules

| Module | Prefix | Description |
|--------|--------|-------------|
| Auth | /api/v1/auth | Signup, login, token refresh |
| Events | /api/v1/events | Event CRUD |
| Categories | /api/v1/categories | Delegate category management |
| Registrations | /api/v1/registrations | Core registration + search + barcode |
| Custom Fields | /api/v1/custom-fields | Dynamic field management |
| Card Layouts | /api/v1/card-layouts | Badge design configuration |
| Search | /api/v1/search | Multi-field registration search |
| KIT | /api/v1/kit | KIT issue/status/reissue |
| Lunch | /api/v1/lunch | Lunch plate scanning |
| Dinner | /api/v1/dinner | Dinner plate scanning |
| Hall | /api/v1/hall | Halls, sessions, entry/exit tracking |
| Certificates | /api/v1/certificates | Certificate data + templates |
| Reports | /api/v1/reports | All report types |
| Notifications | /api/v1/notifications | Email/SMS queue |
| Display | /api/v1/display | Screen display data |
| Files | /api/v1/files | Photo/logo upload |
