# Application Design Plan

## Design Questions

## Question 1: Component Organization
How should the backend components be organized?

A) Flat — all services in one layer, simple imports

B) Feature-based — group by module (registration/, kit/, lunch/, etc.), each with its own router/service/repository

C) Technical layer-based — separate top-level directories for routers/, services/, repositories/, models/

D) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 2: Service Granularity
How granular should the service layer be?

A) One service per module (e.g., RegistrationService handles all registration operations)

B) Multiple focused services per module (e.g., RegistrationWriteService, RegistrationReadService)

C) One service per entity

D) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 3: Repository Pattern Granularity
How should repositories be structured?

A) One repository per aggregate root (e.g., RegistrationRepository for Registration + Payment)

B) One repository per database table/entity

C) Generic repository with specific query methods per module

D) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 4: Unit of Work Scope
What should be the scope of the Unit of Work?

A) Per-request — one UOW instance per HTTP request, shared across services

B) Per-transaction — new UOW for each logical operation

C) Service-managed — each service manages its own UOW lifecycle

D) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 5: Barcode/QR Generation
How should barcode/QR code generation be handled?

A) Dedicated BarcodeService using a library (e.g., python-barcode, qrcode) returning base64 images

B) Simple unique ID generation — client creates barcode from the ID

C) Both — service generates code image and returns both image and raw value

D) Other (please describe after [Answer]: tag below)

[Answer]: C

## Question 6: File Upload Storage
Where should uploaded photos and logos be stored?

A) Database as binary/BLOB

B) Local filesystem with path stored in DB

C) Cloud storage (S3/Azure Blob)

D) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 7: API Versioning
Should the API include versioning from the start?

A) Yes — URL-based versioning (/api/v1/...)

B) Yes — header-based versioning

C) No — add versioning later when needed

D) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 8: Async Processing
How should async operations (email/SMS, report generation) be handled?

A) Background tasks via FastAPI's BackgroundTasks

B) Celery task queue

C) Database queue table with a separate worker process

D) Synchronous only — no async processing needed

E) Other (please describe after [Answer]: tag below)

[Answer]: A

---

## Design Artifacts Checklist

- [ ] Generate components.md — Component definitions and responsibilities
- [ ] Generate component-methods.md — Method signatures for each component
- [ ] Generate services.md — Service definitions and orchestration
- [ ] Generate component-dependency.md — Dependency relationships
- [ ] Validate design completeness and consistency
