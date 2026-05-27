# Application Design

## Architecture Overview

**Pattern**: Feature-based layered architecture with Repository + Unit of Work
**Stack**: Python 3.12+ / FastAPI / SQLAlchemy (async) / SQL Server

## Component Summary

### Core Domain (16 components)
1. **Event** — Top-level organizing entity; all data scoped to an event
2. **Registration** — Delegate registration with custom fields, card layout, payment
3. **Category** — Delegate types with printable/non-printable flags and restrictions
4. **Payment** — Payment method tracking linked to registrations
5. **Search** — Multi-field search (name, company, email, reg no, mobile, city, country)
6. **Barcode** — QR/barcode generation and validation
7. **KIT Issue** — KIT distribution with duplicate prevention and reissue
8. **Lunch Scanning** — Plate issuance with time window (12 PM - 6 PM) and restrictions
9. **Dinner Scanning** — Plate issuance with time window (6 PM - midnight)
10. **Hall Management** — Multi-hall, multi-session entry/exit tracking
11. **Certificate** — Certificate data retrieval and template configuration
12. **Reports** — Cross-module report aggregation
13. **Notification** — Email/SMS queue for async processing
14. **Display** — Delegate name/photo display data
15. **Card Layout** — Badge design configuration
16. **Custom Field** — Dynamic field management

### Cross-Cutting (2 components)
17. **Auth** — JWT authentication, RBAC authorization
18. **File Storage** — Local filesystem photo/logo management

### Technical Infrastructure (2 components)
19. **Unit of Work** — Per-request transaction coordinator
20. **Repositories** — Data access per aggregate root (14 repositories)

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Component Organization | Feature-based (module folders) | Clear separation, each module self-contained |
| Service Granularity | One service per module | Balanced complexity, clear ownership |
| Repository Pattern | Per aggregate root | UOW coordinates across roots, prevents anemic data layer |
| UOW Scope | Per HTTP request | Natural FastAPI DI scoping, consistent transaction boundary |
| Barcode Generation | Server-side (both image + raw) | Library-based, returns base64 image and raw value |
| File Storage | Local filesystem + DB path | Simple, no cloud dependency |
| API Versioning | URL-based (/api/v1/) | Explicit, easy to evolve |
| Async Processing | FastAPI BackgroundTasks | Simple, no extra infrastructure |

## Project Structure

```
registration-backend/
├── app/
│   ├── main.py                  # FastAPI app, middleware, router registration
│   ├── config.py                # Settings, DB connection string
│   ├── deps.py                  # Dependency injection
│   ├── database.py              # SQLAlchemy engine, session factory
│   ├── models/                  # SQLAlchemy ORM models
│   │   ├── base.py
│   │   ├── event.py
│   │   ├── registration.py
│   │   ├── category.py
│   │   ├── payment.py
│   │   ├── kit_issue.py
│   │   ├── lunch_scan.py
│   │   ├── dinner_scan.py
│   │   ├── hall.py
│   │   ├── session.py
│   │   ├── hall_entry.py
│   │   ├── certificate.py
│   │   ├── notification.py
│   │   ├── card_layout.py
│   │   ├── custom_field.py
│   │   └── user.py
│   ├── schemas/                 # Pydantic request/response schemas
│   ├── repositories/            # Repository implementations
│   │   ├── base.py
│   │   ├── event_repo.py
│   │   ├── registration_repo.py
│   │   ├── category_repo.py
│   │   ├── payment_repo.py
│   │   ├── kit_issue_repo.py
│   │   ├── lunch_scan_repo.py
│   │   ├── dinner_scan_repo.py
│   │   ├── hall_repo.py
│   │   ├── session_repo.py
│   │   ├── hall_entry_repo.py
│   │   ├── certificate_repo.py
│   │   ├── notification_repo.py
│   │   ├── card_layout_repo.py
│   │   └── custom_field_repo.py
│   ├── unit_of_work.py          # UOW implementation
│   ├── services/                # Business logic
│   │   ├── event_service.py
│   │   ├── registration_service.py
│   │   ├── category_service.py
│   │   ├── payment_service.py
│   │   ├── barcode_service.py
│   │   ├── search_service.py
│   │   ├── kit_service.py
│   │   ├── lunch_service.py
│   │   ├── dinner_service.py
│   │   ├── hall_service.py
│   │   ├── certificate_service.py
│   │   ├── report_service.py
│   │   ├── notification_service.py
│   │   ├── display_service.py
│   │   ├── card_layout_service.py
│   │   ├── custom_field_service.py
│   │   ├── auth_service.py
│   │   └── file_storage_service.py
│   ├── routers/                 # FastAPI route handlers
│   │   ├── events.py
│   │   ├── registrations.py
│   │   ├── categories.py
│   │   ├── search.py
│   │   ├── kit.py
│   │   ├── lunch.py
│   │   ├── dinner.py
│   │   ├── hall.py
│   │   ├── certificates.py
│   │   ├── reports.py
│   │   ├── display.py
│   │   ├── card_layouts.py
│   │   ├── custom_fields.py
│   │   ├── auth.py
│   │   └── files.py
│   └── middleware/
│       ├── auth.py              # JWT validation middleware
│       ├── logging.py           # Request logging
│       └── security.py          # Security headers
├── tests/
├── uploads/                     # Photo/logo file storage
├── requirements.txt
└── README.md
```
