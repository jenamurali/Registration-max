# Domain Entities — Unit 1: Foundation

## Base Model

### Base
Common fields inherited by all entities:
- `id: int` — Primary key, auto-increment
- `created_at: datetime` — Auto-set on insert
- `updated_at: datetime` — Auto-updated on change

## User

### User
Stores authentication credentials for system operators.

**Fields**:
- `id: int` — PK
- `username: str(50)` — Unique, not null
- `email: str(255)` — Unique, not null
- `password_hash: str(255)` — Hashed password, not null
- `role: str(20)` — Enum: "admin", "operator", not null
- `is_active: bool` — Default True
- `created_at: datetime`
- `updated_at: datetime`

**Relationships**: None (standalone entity)

**Validation Rules**:
- Username: 3-50 chars, alphanumeric + underscore
- Email: Valid email format, unique
- Password: Minimum 8 chars before hashing
- Role: Must be "admin" or "operator"

## Entity Diagram

```
┌──────────────────────┐
│        Base          │
├──────────────────────┤
│ id: int (PK)         │
│ created_at: datetime │
│ updated_at: datetime │
└──────────────────────┘
           ▲
           │ inherits
┌──────────────────────┐
│        User          │
├──────────────────────┤
│ username: str(50)    │
│ email: str(255)      │
│ password_hash: str   │
│ role: str(20)        │
│ is_active: bool      │
└──────────────────────┘
```

## SQLAlchemy Model Notes

- Base uses `declarative_base()` with `__abstract__ = True`
- User table name: `users`
- All models use async SQLAlchemy 2.0 style with `Mapped` type annotations
- `created_at` uses `server_default=func.now()`
- `updated_at` uses `onupdate=func.now()`
