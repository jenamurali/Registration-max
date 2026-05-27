# Domain Entities — Unit 2: Event & Category

## Event

Top-level organizing entity. All registrations, scans, and reports are scoped to an event.

**Fields**:
- `id: int` — PK
- `name: str(200)` — Event name, not null
- `start_date: date` — Event start
- `end_date: date` — Event end
- `venue: str(300)` — Venue/location, nullable
- `is_active: bool` — Default True
- `created_at: datetime`
- `updated_at: datetime`

**Relationships**: Has many Registrations, Categories (indirect)

## Category

Delegate type classification with printable flag and restriction rules.

**Fields**:
- `id: int` — PK
- `name: str(100)` — Category name (e.g., "Delegate", "VIP", "Crew"), unique, not null
- `is_printable: bool` — Default True. Non-printable = hide print options
- `description: str(500)` — Optional description
- `created_at: datetime`
- `updated_at: datetime`

**Relationships**: Many Registrations belong to one Category

**Inline Lists**:
- Default categories: Delegate, Organiser, Speaker, Guest, VIP, Sponsor, Exhibitor, Crew, Media

## Entity Diagram

```
┌──────────────────────┐       ┌──────────────────────┐
│        Event         │       │      Category        │
├──────────────────────┤       ├──────────────────────┤
│ id: int (PK)         │       │ id: int (PK)         │
│ name: str(200)       │       │ name: str(100) UNQ   │
│ start_date: date     │       │ is_printable: bool   │
│ end_date: date       │       │ description: str(500)│
│ venue: str(300)      │       │ created_at: datetime │
│ is_active: bool      │       │ updated_at: datetime │
│ created_at: datetime │       └──────────────────────┘
│ updated_at: datetime │
└──────────────────────┘
```
