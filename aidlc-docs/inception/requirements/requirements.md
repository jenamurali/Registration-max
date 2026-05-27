# Requirements Document

## Intent Analysis

- **User Request**: Build only the backend with Repository and Unit of Work (UOW) pattern
- **Request Type**: New Project (Greenfield)
- **Scope Estimate**: Multiple Components — Registration, KIT, Lunch, Dinner, Hall Management, Certificate, Reports modules
- **Complexity Estimate**: Moderate — well-defined domain with clear entities and business rules

## Technology Decisions

| Decision | Choice |
|----------|--------|
| Backend Stack | Python 3.12+ with FastAPI + SQLAlchemy (async) |
| Database | SQL Server |
| API Style | RESTful API |
| Authentication | JWT-based with Role-Based Access Control |
| Multi-Event | Single DB with event_id filtering |
| Barcode/QR | Server generates image + returns raw ID |
| File Upload | Basic upload (store photos/logos) |
| Notifications | Queue-based (store in table for async processing) |
| Reporting | JSON data endpoints |
| Certificates | Data-only, client handles PDF generation |
| Security Extension | Enforced |
| PBT Extension | Skipped |

## Architecture Pattern

- **Repository Pattern**: Each aggregate root gets a repository interface and implementation
- **Unit of Work (UOW)**: Coordinates transactions across multiple repositories
- **Layered Architecture**: Routers → Services → Repositories/UOW → SQLAlchemy → SQL Server

## Functional Requirements

### Module 1: Event Management
- CRUD for events (master entity that all other data filters by)
- Event configuration settings

### Module 2: Registration
- **Delegate Registration**: Capture Name, Company, Country/City, Mobile, Email, Photo (optional), Logo (optional)
- **Category Assignment**: Delegate, Organiser, Speaker, Guest, VIP, Sponsor, Exhibitor, Crew, Media, etc.
- **Custom Fields**: Dynamic fields — add, remove, reorder (left/right, up/down)
- **Card Layout Configuration**: Adjustable card design, font selection, font sizing
- **Barcode/QR Generation**: Per registration ID or unique number, both image and raw value
- **Dropdown/List Box Data**: Company name, City, Country list sources
- **Payment Tracking**: Paid (Cash, Credit Card, DD, Cheque, Net Banking + Receipt No.) or Unpaid
- **Registration Counts**: Live chart data for pre-registered, on-spot, print counts
- **Duplicate Prevention**: Category-based restriction and allow rules
- **Print Actions**: Save & Print, Save/Edit, Save/Edit & Print
- **Bulk Print**: Search by company, select via checkbox, print multiple

### Module 3: Search
- Search by: Name, Company Name, Email, Registration No./Barcode, Mobile, City, Country
- Support wildcard/partial matching

### Module 4: KIT Issue
- First scan: Issue KIT with timestamp
- Duplicate scan: Show "Already Issued" with original time & date
- Reissue: Allow with remark/approval text
- Check status: Scan to display KIT issued or not

### Module 5: Lunch Scanning
- Plate issue after barcode scan
- Time window: 12:00 PM to 6:00 PM
- One plate per barcode
- Duplicate scan: Show "Already Issued"
- Reissue: Allow with remark

### Module 6: Dinner Scanning
- Plate issue after barcode scan
- Time window: After 6:00 PM to midnight
- One plate per barcode
- Duplicate scan: Show "Already Issued"
- Reissue: Allow with remark

### Module 7: Hall Management (Delegate Tracking)
- Hall entry/exit tracking by barcode scan
- Multiple halls support
- Session-wise tracking within each hall
- In/Out time logging

### Module 8: Certificate Printing
- Scan barcode → return certificate data (name, subject, company, date/time)
- Text-based search to find and retrieve certificate data
- Configurable text placement metadata

### Module 9: Category Restrictions
- Restrict categories from certain actions (e.g., Crew not allowed in Lunch)
- Scan validation returns allow/deny with message

### Module 10: Display Module
- After registration: display delegate name/photo on screen via barcode scan or UHF card

### Module 11: Reports
- Total registration counts (pre-registration, on-spot)
- Print counts (single/multiple)
- KIT issue report
- Lunch report
- Dinner report
- Hall scanning report
- Session scanning report
- All filterable by event, date range, category

### Module 12: Notifications
- Pre/post registration email/SMS queue
- Notification jobs stored in database for async processing

## Non-Functional Requirements

- **Performance**: API responses under 500ms for typical queries
- **Security**: JWT authentication, role-based authorization, input validation, SQL injection prevention via EF Core parameterization
- **Scalability**: Stateless API design, connection pooling via EF Core
- **Data Integrity**: Unit of Work pattern ensures transactional consistency across repositories
- **Maintainability**: Clear separation of concerns (Controllers → Services → Repositories → EF Core)

## Entity Overview

- **Event** — Master event entity
- **Registration** — Core delegate registration with all fields
- **Category** — Delegate types (printable/non-printable flag)
- **Payment** — Payment details linked to registration
- **KITIssue** — KIT issuance log
- **LunchScan** — Lunch plate issuance log
- **DinnerScan** — Dinner plate issuance log
- **HallEntry** — Hall entry/exit tracking
- **Hall** — Hall definitions
- **Session** — Session definitions within halls
- **Certificate** — Certificate template config
- **Notification** — Email/SMS queue
- **CardLayout** — Card design configuration
- **CustomField** — Dynamic field definitions
