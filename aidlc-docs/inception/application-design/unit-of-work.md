# Units of Work

## Decomposition Strategy
**Approach**: Grouped by dependency, sequential execution
**Rationale**: Each unit builds on the foundation of previous units. Dependencies are explicit and ordered.

## Unit Definitions

### Unit 1: Foundation
**Priority**: 1 (Build first)
**Description**: Core infrastructure that all other units depend on.
**Scope**:
- SQLAlchemy database configuration, engine, session factory
- Base model class with common fields (id, created_at, updated_at)
- Base repository class with generic CRUD operations
- Unit of Work implementation
- Configuration management (settings, env vars)
- FastAPI app setup, CORS, middleware registration
- Auth middleware (JWT validation)
- Security headers middleware
- Structured logging setup
- Dependency injection wiring (deps.py)
- User model and auth service (login, token generation)

### Unit 2: Event & Category Management
**Priority**: 2
**Dependencies**: Unit 1 (Foundation)
**Description**: Top-level organizing entities.
**Scope**:
- Event model, repository, service, router
- Category model, repository, service, router
- Category restrictions (printable/non-printable)

### Unit 3: Registration Core
**Priority**: 3
**Dependencies**: Unit 1, Unit 2
**Description**: Core delegate registration with supporting features.
**Scope**:
- Registration model, repository, service, router
- Custom Field model, repository, service, router
- Card Layout model, repository, service, router
- Registration CRUD (all fields, photo, logo)
- Category assignment to registrations
- Dropdown data sources (company name, city, country lists)

### Unit 4: Payment & Barcode
**Priority**: 4
**Dependencies**: Unit 1, Unit 3
**Description**: Payment tracking and barcode generation.
**Scope**:
- Payment model, repository, service, router
- Barcode/QR generation service (python-barcode, qrcode libraries)
- Payment methods (Cash, Credit Card, DD, Cheque, Net Banking)
- Receipt number tracking
- Paid/Unpaid status

### Unit 5: Search & Display
**Priority**: 5
**Dependencies**: Unit 1, Unit 3
**Description**: Multi-field search and display data retrieval.
**Scope**:
- Search service (name, company, email, reg no, mobile, city, country)
- Display service (name/photo by barcode or UHF card)
- Registration counts (pre-registered, on-spot, print count)

### Unit 6: Scanning Modules (KIT, Lunch, Dinner)
**Priority**: 6
**Dependencies**: Unit 1, Unit 3, Unit 4
**Description**: KIT distribution, lunch and dinner plate issuance.
**Scope**:
- KIT Issue model, repository, service, router
- Lunch Scan model, repository, service, router
- Dinner Scan model, repository, service, router
- Duplicate scan prevention ("Already Issued" with timestamp)
- Time window enforcement (Lunch 12PM-6PM, Dinner 6PM-Midnight)
- Category restriction checks (e.g., Crew not allowed in Lunch)
- Reissue with remark workflow
- KIT status check by scan

### Unit 7: Hall Management
**Priority**: 7
**Dependencies**: Unit 1, Unit 3, Unit 4
**Description**: Hall entry/exit tracking with session management.
**Scope**:
- Hall model, repository, service, router
- Session model, repository, service, router
- Hall Entry model, repository, service, router
- Entry/exit recording by barcode scan
- In/out time logging
- Active entry detection (exit requires prior entry)
- Session-wise tracking per hall

### Unit 8: Certificate & Reports
**Priority**: 8
**Dependencies**: Unit 1, Unit 3, Unit 6, Unit 7
**Description**: Certificate data and cross-module reporting.
**Scope**:
- Certificate template model, repository, service, router
- Certificate data retrieval (by scan or search)
- Report service (all report types)
- Registration report (pre-reg, on-spot, total)
- KIT issue report
- Lunch report
- Dinner report
- Hall scanning report
- Session scanning report
- Print count report
- Filtering by event, date range, category

### Unit 9: Notifications & File Storage
**Priority**: 9
**Dependencies**: Unit 1, Unit 3
**Description**: Async notifications and file upload handling.
**Scope**:
- Notification model, repository, service, router
- Email/SMS queue management
- FastAPI BackgroundTasks for async processing
- File storage service (photo/logo upload)
- Local filesystem storage with path in DB
- Accepted file type validation
