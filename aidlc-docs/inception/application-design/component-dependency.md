# Component Dependencies

## Dependency Matrix

| Component | Event | Reg | Cat | Pay | Search | Barcode | KIT | Lunch | Dinner | Hall | Cert | Report | Notif | Display | CardLayout | CustomField | Auth | File |
|-----------|---|---|---|---|---|---|-----|---------|-----|-------|--------|------|------|--------|-------|---------|------------|-------------|------|-----|
| **Event** | - | | | | | | | | | | | | | | | | | |
| **Registration** | x | - | x | x | | x | | | | | | | x | | | | | x |
| **Category** | | | - | | | | | | | | | | | | | | | |
| **Payment** | | x | | - | | | | | | | | | | | | | | |
| **Search** | | x | | | - | | | | | | | | | | | | | |
| **Barcode** | | x | | | | - | | | | | | | | | | | | |
| **KIT** | | x | x | | | x | - | | | | | | | | | | | |
| **Lunch** | | x | x | | | x | | - | | | | | | | | | | |
| **Dinner** | | x | | | | x | | | - | | | | | | | | | |
| **Hall** | | x | | | | x | | | | - | | | | | | | | |
| **Certificate** | | x | | | | x | | | | | - | | | | | | | |
| **Reports** | x | x | x | x | | | x | x | x | x | | - | | | | | | |
| **Notifications** | | x | | | | | | | | | | | - | | | | | |
| **Display** | | x | | | | x | | | | | | | | - | | | | x |
| **CardLayout** | x | | | | | | | | | | | | | | - | | | |
| **CustomField** | x | | | | | | | | | | | | | | | - | | |
| **Auth** | | | | | | | | | | | | | | | | | - | |
| **File** | | | | | | | | | | | | | | | | | | - |

## Communication Patterns

### Synchronous (Direct Method Calls)
- **Service-to-Service**: All service interactions are synchronous method calls within the same process
- **Service-to-Repository**: Via Unit of Work, synchronous data access
- **Controller-to-Service**: FastAPI routers call services directly

### Data Flow
```
HTTP Request → Router → Service(s) → UOW → Repository(ies) → SQLAlchemy → SQL Server
                              ↓
                        HTTP Response (JSON)
```

### Transaction Boundary
```
┌─────────────────── Request Scope ──────────────────┐
│  Router Layer (FastAPI)                             │
│  ┌─────────────────────────────────────────────┐   │
│  │  Service Layer                               │   │
│  │  ┌─────────────────────────────────────┐    │   │
│  │  │  Unit of Work                       │    │   │
│  │  │  ┌──────────┐ ┌──────────┐         │    │   │
│  │  │  │ Repo A   │ │ Repo B   │  ...    │    │   │
│  │  │  └──────────┘ └──────────┘         │    │   │
│  │  └─────────────────────────────────────┘    │   │
│  └─────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────┘
```

## Dependency Injection Flow

```
app (FastAPI)
 └── deps.py
      ├── get_uow() → UnitOfWork (scoped to request)
      ├── get_event_service(uow) → EventService
      ├── get_registration_service(uow) → RegistrationService
      ├── get_category_service(uow) → CategoryService
      ├── get_barcode_service(uow) → BarcodeService
      ├── get_kit_service(uow, barcode_svc) → KITService
      ├── get_lunch_service(uow, barcode_svc) → LunchService
      ├── get_dinner_service(uow, barcode_svc) → DinnerService
      ├── get_hall_service(uow, barcode_svc) → HallService
      ├── get_certificate_service(uow, barcode_svc) → CertificateService
      ├── get_report_service(uow) → ReportService
      ├── get_notification_service(uow) → NotificationService
      ├── get_display_service(uow, barcode_svc, file_svc) → DisplayService
      ├── get_card_layout_service(uow) → CardLayoutService
      ├── get_custom_field_service(uow) → CustomFieldService
      ├── get_auth_service(uow) → AuthService
      ├── get_search_service(uow) → SearchService
      ├── get_payment_service(uow) → PaymentService
      └── get_file_storage_service() → FileStorageService
```
