# Business Rules — Unit 2: Event & Category

## Event Rules

### BR-EVT-01: Event Name Uniqueness
- Event name must be unique per event
- Attempting to create duplicate returns 409

### BR-EVT-02: Date Validation
- end_date must be >= start_date
- Invalid date range returns 422

### BR-EVT-03: Active Events
- Only active events appear in dropdown lists
- Deactivating an event does not delete its data

## Category Rules

### BR-CAT-01: Category Name Uniqueness
- Category name must be unique
- Duplicate returns 409

### BR-CAT-02: Printable Flag
- Non-printable categories: print options hidden in UI (backend returns flag)
- Default all new categories to printable=True

### BR-CAT-03: Category Restriction Metadata
- Categories carry restriction metadata for scanning modules:
  - allowed_kit: bool (default True)
  - allowed_lunch: bool (default True)
  - allowed_dinner: bool (default True)
- These are stored on the Category for scanning module checks in later units

### BR-CAT-04: Default Categories
- System seeds default categories on first run if none exist
- Default categories can be modified or deleted

## API Rules

### BR-API-01: Standard CRUD
- Both Event and Category follow RESTful CRUD pattern
- GET (list + single), POST (create), PUT (update), DELETE (soft delete via deactivation)
