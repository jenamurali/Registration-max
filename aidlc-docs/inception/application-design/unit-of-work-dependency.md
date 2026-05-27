# Unit of Work Dependencies

## Dependency Matrix

| Unit | 1-Foundation | 2-EventCat | 3-Reg | 4-PayBarcode | 5-SearchDisp | 6-Scanning | 7-Hall | 8-CertRpt | 9-NotifFile |
|------|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| **1-Foundation** | - | | | | | | | | |
| **2-EventCat** | x | - | | | | | | | |
| **3-Registration** | x | x | - | | | | | | |
| **4-PayBarcode** | x | | x | - | | | | | |
| **5-SearchDisp** | x | | x | | - | | | | |
| **6-Scanning** | x | | x | x | | - | | | |
| **7-Hall** | x | | x | x | | | - | | |
| **8-CertRpt** | x | | x | | | x | x | - | |
| **9-NotifFile** | x | | x | | | | | | - |

## Dependency Graph

```
Unit 1: Foundation
    │
    ├── Unit 2: Event & Category
    │       │
    │       └── Unit 3: Registration Core
    │               │
    │               ├── Unit 4: Payment & Barcode
    │               │       │
    │               │       ├── Unit 6: Scanning (KIT, Lunch, Dinner)
    │               │       │       │
    │               │       │       └── Unit 8: Certificate & Reports
    │               │       │
    │               │       └── Unit 7: Hall Management
    │               │               │
    │               │               └── Unit 8: Certificate & Reports
    │               │
    │               ├── Unit 5: Search & Display
    │               │
    │               └── Unit 9: Notifications & File Storage
```

## Sequential Execution Order

| Order | Unit | Rationale |
|-------|------|-----------|
| 1 | Foundation | Everything depends on it |
| 2 | Event & Category | Required by Registration |
| 3 | Registration Core | Required by all downstream units |
| 4 | Payment & Barcode | Required by Scanning, Hall |
| 5 | Search & Display | Independent of 4, depends on 3 |
| 6 | Scanning (KIT/Lunch/Dinner) | Depends on Registration + Barcode |
| 7 | Hall Management | Depends on Registration + Barcode |
| 8 | Certificate & Reports | Depends on Registration + Scanning + Hall |
| 9 | Notifications & File Storage | Independent of 6-8, depends on 3 |

## Within Each Unit

Each unit delivers:
- SQLAlchemy model(s) in `app/models/`
- Pydantic schemas in `app/schemas/`
- Repository in `app/repositories/`
- Service in `app/services/`
- Router in `app/routers/`
- Unit tests in `tests/`
