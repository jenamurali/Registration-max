# Business Logic Model — Unit 2: Event & Category

## EventService

```
EventService(event_repo: EventRepository)
  ├── create_event(data: EventCreate) -> Event
  │     ├── Validate end_date >= start_date
  │     └── event_repo.add(event)
  │
  ├── update_event(event_id: int, data: EventUpdate) -> Event
  │     ├── event_repo.get_by_id(event_id) -> raise 404 if missing
  │     ├── Validate date range if both provided
  │     └── event_repo.update(event)
  │
  ├── get_event(event_id: int) -> Event
  │     └── event_repo.get_by_id -> raise 404 if None
  │
  ├── list_events(active_only: bool = False) -> List[Event]
  │     └── event_repo.get_all or get_active
  │
  └── deactivate_event(event_id: int) -> Event
        └── Set is_active=False, save

## CategoryService

CategoryService(category_repo: CategoryRepository)
  ├── create_category(data: CategoryCreate) -> Category
  │     ├── Check name uniqueness
  │     └── category_repo.add(category)
  │
  ├── update_category(cat_id: int, data: CategoryUpdate) -> Category
  │     └── category_repo.update(category)
  │
  ├── get_category(cat_id: int) -> Category
  │     └── category_repo.get_by_id -> raise 404
  │
  ├── list_categories(printable_only: bool = False) -> List[Category]
  │     └── category_repo.get_all or get_printable
  │
  └── delete_category(cat_id: int) -> None
        └── category_repo.delete(category)
```

## Repositories

### EventRepository
Extends BaseRepository[Event]:
- `get_active() -> List[Event]`

### CategoryRepository
Extends BaseRepository[Category]:
- `get_by_name(name: str) -> Optional[Category]`
- `get_printable() -> List[Category]`
- `get_non_printable() -> List[Category]`
