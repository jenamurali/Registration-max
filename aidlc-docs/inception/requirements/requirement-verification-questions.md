# Requirements Clarification Questions

Please answer the following questions to help clarify the backend implementation requirements.

## Question 1
What backend technology stack should be used?

A) .NET 8 (C#) with Entity Framework Core

B) Node.js with Express/TypeScript

C) Python with FastAPI/Django

D) Java with Spring Boot

E) Other (please describe after [Answer]: tag below)

[Answer]: C

## Question 2
What database should be used?

A) SQL Server

B) PostgreSQL

C) MySQL

D) SQLite (for development/prototype)

E) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 3
What API style should the backend expose?

A) RESTful API

B) GraphQL

C) Both REST and GraphQL

D) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 4
Should authentication and authorization be included in this backend build?

A) Yes — full JWT-based auth with role-based access control (Admin, Operator, etc.)

B) Yes — basic API key authentication only

C) No — authentication will be added later

D) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 5
The feature list mentions "eventwise" database connectivity. Should the system support multiple events with isolated data?

A) Yes — multi-tenant by event (each event has its own segregated data)

B) Yes — single database with event_id filtering on all records

C) No — single event only (no event segmentation needed)

D) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 6
For the barcode/QR code generation, what approach should be taken?

A) Generate barcode/QR code images server-side and return as part of the API response

B) Return a unique registration ID only — client handles barcode/QR generation

C) Both — server generates the code image and also returns the raw ID

D) Other (please describe after [Answer]: tag below)

[Answer]: C

## Question 7
Should file upload handling (photos, logos) be included in this backend build?

A) Yes — full file upload/storage with image cropping support

B) Yes — basic file upload only (store images, no server-side processing)

C) No — file upload will be handled later

D) Other (please describe after [Answer]: tag below)

[Answer]: B

## Question 8
For email/SMS notifications, what should be included?

A) Full integration — email service (SMTP/SendGrid) + SMS gateway integration

B) Email only — integrate email service, SMS deferred

C) Queue-based — store notifications in a queue/table for a separate service to process

D) No — notifications will be handled later

E) Other (please describe after [Answer]: tag below)

[Answer]: C

## Question 9
What reporting approach should the backend support?

A) API endpoints returning report data (JSON) — frontend handles rendering

B) Server-side report generation (PDF/Excel) via API endpoints

C) Both — data endpoints + downloadable report files

D) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 10
Should the certificate printing module include server-side PDF generation?

A) Yes — server generates certificate PDF with configurable text placement

B) No — backend returns certificate data only, client handles PDF/image generation

C) Other (please describe after [Answer]: tag below)

[Answer]: B

---

## Extension Opt-In Questions

## Question 11: Security Extensions
Should security extension rules be enforced for this project?

A) Yes — enforce all SECURITY rules as blocking constraints (recommended for production-grade applications)

B) No — skip all SECURITY rules (suitable for PoCs, prototypes, and experimental projects)

C) Other (please describe after [Answer]: tag below)

[Answer]: A

## Question 12: Property-Based Testing Extension
Should property-based testing (PBT) rules be enforced for this project?

A) Yes — enforce all PBT rules as blocking constraints (recommended for projects with business logic, data transformations, serialization, or stateful components)

B) Partial — enforce PBT rules only for pure functions and serialization round-trips (suitable for projects with limited algorithmic complexity)

C) No — skip all PBT rules (suitable for simple CRUD applications, UI-only projects, or thin integration layers with no significant business logic)

D) Other (please describe after [Answer]: tag below)

[Answer]: C
