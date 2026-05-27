# Services

## Service Layer Architecture

All business logic resides in service classes. Controllers (FastAPI routers) handle HTTP concerns and delegate to services. Services use Unit of Work for transaction management and repositories for data access.

## Service Definitions

### EventService
- **Responsibility**: Event lifecycle management
- **Dependencies**: UnitOfWork (events)
- **Orchestration**: Standalone — no cross-service calls

### RegistrationService
- **Responsibility**: Delegate registration workflow including payment, barcode generation, and notifications
- **Dependencies**: UnitOfWork (registrations, payments), BarcodeService, NotificationService
- **Orchestration**: Coordinates barcode generation and notification queuing during registration

### CategoryService
- **Responsibility**: Category definitions and restriction rules
- **Dependencies**: UnitOfWork (categories)
- **Orchestration**: Standalone — consumed by scanning services for restriction checks

### PaymentService
- **Responsibility**: Payment recording and status management
- **Dependencies**: UnitOfWork (payments)
- **Orchestration**: Called by RegistrationService during registration workflow

### SearchService
- **Responsibility**: Multi-field search aggregation
- **Dependencies**: UnitOfWork (registrations)
- **Orchestration**: Delegates directly to RegistrationRepository query methods

### BarcodeService
- **Responsibility**: Barcode/QR generation and validation
- **Dependencies**: UnitOfWork (registrations), qrcode/python-barcode libraries
- **Orchestration**: Called by RegistrationService and all scanning services

### KITService
- **Responsibility**: KIT issuance with duplicate prevention and reissue workflow
- **Dependencies**: UnitOfWork (kit_issues, registrations), BarcodeService
- **Orchestration**: Validates barcode, checks category restrictions, records issue

### LunchService
- **Responsibility**: Lunch plate issuance with time window and duplicate prevention
- **Dependencies**: UnitOfWork (lunch_scans, registrations, categories), BarcodeService
- **Orchestration**: Validates time window, barcode, category restrictions, records issue

### DinnerService
- **Responsibility**: Dinner plate issuance with time window and duplicate prevention
- **Dependencies**: UnitOfWork (dinner_scans, registrations), BarcodeService
- **Orchestration**: Validates time window, barcode, records issue

### HallService
- **Responsibility**: Hall entry/exit tracking with session awareness
- **Dependencies**: UnitOfWork (hall_entries, halls, sessions, registrations), BarcodeService
- **Orchestration**: Validates barcode, checks active entry for exit, records entry/exit events

### CertificateService
- **Responsibility**: Certificate data retrieval and template configuration
- **Dependencies**: UnitOfWork (registrations, certificates), BarcodeService
- **Orchestration**: Resolves barcode to registration, returns certificate data

### ReportService
- **Responsibility**: Aggregate report data across all modules
- **Dependencies**: UnitOfWork (all repositories)
- **Orchestration**: Cross-module data aggregation, no business logic

### NotificationService
- **Responsibility**: Queue notifications and process pending jobs
- **Dependencies**: UnitOfWork (notifications), FastAPI BackgroundTasks
- **Orchestration**: Called by RegistrationService, runs async processing

### DisplayService
- **Responsibility**: Provide display data for screens
- **Dependencies**: UnitOfWork (registrations), BarcodeService, FileStorageService
- **Orchestration**: Resolves barcode/UHF to registration with photo

### CardLayoutService
- **Responsibility**: Card design configuration
- **Dependencies**: UnitOfWork (card_layouts)
- **Orchestration**: Standalone

### CustomFieldService
- **Responsibility**: Dynamic field management
- **Dependencies**: UnitOfWork (custom_fields)
- **Orchestration**: Standalone

### AuthService
- **Responsibility**: Authentication and token management
- **Dependencies**: UnitOfWork (users), JWT library, passlib
- **Orchestration**: Called by auth middleware on protected routes

### FileStorageService
- **Responsibility**: File upload and retrieval
- **Dependencies**: Filesystem (local storage)
- **Orchestration**: Called by RegistrationService for photo/logo uploads

## Service Interaction Patterns

```
Registration Flow:
  Router → RegistrationService
              ├── PaymentService (payment recording)
              ├── BarcodeService (code generation)
              ├── FileStorageService (photo/logo upload)
              └── NotificationService (queue email/SMS)

Scanning Flow (KIT/Lunch/Dinner/Hall):
  Router → ScanningService
              ├── BarcodeService (barcode validation)
              ├── CategoryService (restriction check)
              └── [Module]Repository (record issue/scan)

Report Flow:
  Router → ReportService
              └── Multiple Repositories (data aggregation)
```
