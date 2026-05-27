# Unit Test Execution

## Run All Tests
```bash
pytest tests/ -v
```

## Run Specific Test Files
```bash
pytest tests/test_auth.py -v
pytest tests/test_uow.py -v
pytest tests/test_events.py -v
pytest tests/test_categories.py -v
pytest tests/test_registrations.py -v
```

## Test Configuration
- Tests use SQLite file-based (aiosqlite) — no external DB required
- Test database is created and dropped per test function
- Auth tokens are generated per test via signup endpoint or AuthService
- All tests are async (pytest-asyncio)

## Expected Results
- **test_auth.py**: 14 tests — signup (5), login success/fail (3), inactive user, refresh (2), validation (2), end-to-end
- **test_uow.py**: 6 tests — commit, rollback, lazy repo, user queries, pagination
- **test_events.py**: 4 tests — create, list, validation, deactivate
- **test_categories.py**: 4 tests — create, list, printable filter, delete
- **test_registrations.py**: 5 tests — create, barcode lookup, search, counts, print
- **Total**: 33 tests
