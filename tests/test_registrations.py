from datetime import date

import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.models.event import Event
from app.services.auth_service import AuthService

pytestmark = pytest.mark.asyncio


async def _setup(client: AsyncClient, test_session: AsyncSession) -> str:
    auth_service = AuthService(test_session)
    await auth_service.create_user("admin", "admin@test.com", "password123", "admin")
    await test_session.commit()
    resp = await client.post("/api/v1/auth/login", json={
        "username": "admin", "password": "password123",
    })
    token = resp.json()["access_token"]

    event = Event(name="Test Event", start_date=date(2026, 1, 1), end_date=date(2026, 1, 2))
    cat = Category(name="Delegate")
    test_session.add_all([event, cat])
    await test_session.commit()
    return token


async def test_create_registration(client: AsyncClient, test_session: AsyncSession):
    token = await _setup(client, test_session)
    response = await client.post("/api/v1/registrations", json={
        "event_id": 1,
        "category_id": 1,
        "name": "John Doe",
        "company_name": "Acme Corp",
        "country": "India",
        "city": "Mumbai",
        "mobile": "9876543210",
        "email": "john@acme.com",
    }, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "John Doe"
    assert data["reg_no"].startswith("REG-")
    assert data["barcode"].startswith("BC-")


async def test_get_by_barcode(client: AsyncClient, test_session: AsyncSession):
    token = await _setup(client, test_session)
    create_resp = await client.post("/api/v1/registrations", json={
        "event_id": 1, "category_id": 1, "name": "Jane Doe",
    }, headers={"Authorization": f"Bearer {token}"})
    barcode = create_resp.json()["barcode"]

    response = await client.get(f"/api/v1/registrations/barcode/{barcode}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["name"] == "Jane Doe"


async def test_search(client: AsyncClient, test_session: AsyncSession):
    token = await _setup(client, test_session)
    await client.post("/api/v1/registrations", json={
        "event_id": 1, "category_id": 1, "name": "Alice", "company_name": "TechCorp",
    }, headers={"Authorization": f"Bearer {token}"})

    response = await client.get("/api/v1/registrations?company_name=TechCorp", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_get_counts(client: AsyncClient, test_session: AsyncSession):
    token = await _setup(client, test_session)
    await client.post("/api/v1/registrations", json={
        "event_id": 1, "category_id": 1, "name": "User1", "is_pre_registered": True,
    }, headers={"Authorization": f"Bearer {token}"})
    await client.post("/api/v1/registrations", json={
        "event_id": 1, "category_id": 1, "name": "User2",
    }, headers={"Authorization": f"Bearer {token}"})

    response = await client.get("/api/v1/registrations/counts/1", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 2
    assert data["pre_registered"] == 1
    assert data["on_spot"] == 1


async def test_record_print(client: AsyncClient, test_session: AsyncSession):
    token = await _setup(client, test_session)
    create_resp = await client.post("/api/v1/registrations", json={
        "event_id": 1, "category_id": 1, "name": "Print Test",
    }, headers={"Authorization": f"Bearer {token}"})
    reg_id = create_resp.json()["id"]

    response = await client.post(f"/api/v1/registrations/{reg_id}/print", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["print_count"] == 1
