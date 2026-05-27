# Components

## Core Domain Components

### 1. Event Component
**Purpose**: Manage events as the top-level organizing entity. All other data is scoped to an event.
**Responsibilities**:
- CRUD operations for events
- Event configuration and settings
- Event-based data filtering

### 2. Registration Component
**Purpose**: Core delegate registration with all personal and professional details.
**Responsibilities**:
- Delegate registration CRUD (Name, Company, Country/City, Mobile, Email, Photo, Logo)
- Category assignment
- Custom field handling
- Card layout configuration
- Payment tracking (Paid/Unpaid with payment methods)
- Print actions (Save & Print, Save/Edit, Save/Edit & Print)
- Bulk print by company search with checkbox selection
- Duplicate prevention by category rules
- Registration counts (pre-registered, on-spot, print count)

### 3. Category Component
**Purpose**: Define delegate categories with printable/non-printable flags and restrictions.
**Responsibilities**:
- Category CRUD (Delegate, Organiser, Speaker, Guest, VIP, Sponsor, Exhibitor, Crew, Media, etc.)
- Printable vs non-printable flag
- Category-based restrictions for KIT, Lunch, Dinner, Hall access

### 4. Payment Component
**Purpose**: Track payment details linked to registrations.
**Responsibilities**:
- Payment method tracking (Cash, Credit Card, DD, Cheque, Net Banking)
- Receipt number capture
- Paid/Unpaid status management

### 5. Search Component
**Purpose**: Multi-field search across registrations.
**Responsibilities**:
- Search by: Name, Company Name, Email, Registration No./Barcode, Mobile, City, Country
- Wildcard/partial matching support

### 6. Barcode Component
**Purpose**: Generate and validate barcode/QR codes.
**Responsibilities**:
- Barcode/QR code generation by registration ID or unique number
- Return both image (base64) and raw value
- Barcode/QR scanning validation

### 7. KIT Issue Component
**Purpose**: Manage KIT distribution tracking.
**Responsibilities**:
- First scan: Issue KIT with timestamp
- Duplicate scan detection: "Already Issued" with original time/date
- Reissue with remark/approval text
- KIT status check by scan

### 8. Lunch Scanning Component
**Purpose**: Track lunch plate issuance.
**Responsibilities**:
- Plate issue after barcode scan (time window: 12 PM - 6 PM)
- One plate per barcode enforcement
- Duplicate scan detection
- Reissue with remark
- Category restriction check (e.g., Crew not allowed)

### 9. Dinner Scanning Component
**Purpose**: Track dinner plate issuance.
**Responsibilities**:
- Plate issue after barcode scan (time window: 6 PM - midnight)
- One plate per barcode enforcement
- Duplicate scan detection
- Reissue with remark

### 10. Hall Management Component
**Purpose**: Track delegate entry/exit across multiple halls and sessions.
**Responsibilities**:
- Hall definitions (multiple halls)
- Session definitions per hall
- Entry/exit tracking by barcode scan
- In/out time logging
- Session-wise delegate tracking reports

### 11. Certificate Component
**Purpose**: Provide certificate data for printing.
**Responsibilities**:
- Certificate template configuration (text placement metadata)
- Certificate data retrieval by barcode scan or text search
- Date and time stamp on certificate data

### 12. Reports Component
**Purpose**: Aggregate reporting data across all modules.
**Responsibilities**:
- Registration counts (pre-registration, on-spot, total print)
- KIT issue report
- Lunch report
- Dinner report
- Hall scanning report
- Session scanning report
- Filterable by event, date range, category

### 13. Notification Component
**Purpose**: Queue email/SMS notifications for async processing.
**Responsibilities**:
- Pre/post registration notification queue
- Email and SMS job storage
- Processing status tracking

### 14. Display Component
**Purpose**: Provide delegate display data after registration.
**Responsibilities**:
- Retrieve name/photo by barcode scan or UHF card
- Return display-ready data

### 15. Card Layout Component
**Purpose**: Manage customizable card/badge design settings.
**Responsibilities**:
- Card layout configuration (field placement, sizing)
- Font selection and sizing
- Company logo and background settings
- Field order management (move left/right, up/down)

### 16. Custom Field Component
**Purpose**: Dynamic field management for registration forms.
**Responsibilities**:
- Add, remove, reorder custom fields
- Field type configuration
- Field visibility settings

## Cross-Cutting Components

### 17. Auth Component
**Purpose**: Authentication and authorization.
**Responsibilities**:
- JWT token generation and validation
- Role-based access control
- User management (Admin, Operator roles)
- Token refresh

### 18. File Storage Component
**Purpose**: Handle photo and logo file uploads.
**Responsibilities**:
- File upload to local filesystem
- File retrieval by path
- Accepted file type validation

## Technical Infrastructure Components

### 19. Unit of Work Component
**Purpose**: Coordinate transactional consistency across repositories.
**Responsibilities**:
- Manage database transaction lifecycle
- Commit/rollback coordination
- Per-request scoping

### 20. Repository Components
**Purpose**: Data access abstraction for each aggregate root.
**Responsibilities**:
- CRUD operations per aggregate root
- Query methods for search and filtering
- Transaction participation via UOW
