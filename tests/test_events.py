import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.auth_service import AuthService

pytestmark = pytest.mark.asyncio


async def _get_token(client: AsyncClient, test_session: AsyncSession) -> str:
    auth_service = AuthService(test_session)
    await auth_service.create_user("admin", "admin@test.com", "password123", "admin")
    await test_session.commit()
    resp = await client.post("/api/v1/auth/login", json={
        "username": "admin", "password": "password123",
    })
    return resp.json()["access_token"]


async def test_create_event(client: AsyncClient, test_session: AsyncSession):
    token = await _get_token(client, test_session)
    response = await client.post("/api/v1/events", json={
        "name": "Test Conference",
        "start_date": "2026-06-01",
        "end_date": "2026-06-03",
        "venue": "Convention Center",
    }, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Conference"
    assert data["is_active"] is True


async def test_list_events(client: AsyncClient, test_session: AsyncSession):
    token = await _get_token(client, test_session)
    await client.post("/api/v1/events", json={
        "name": "Event A", "start_date": "2026-01-01", "end_date": "2026-01-02",
    }, headers={"Authorization": f"Bearer {token}"})

    response = await client.get("/api/v1/events", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()) == 1


async def test_invalid_date_range(client: AsyncClient, test_session: AsyncSession):
    token = await _get_token(client, test_session)
    response = await client.post("/api/v1/events", json={
        "name": "Bad Event",
        "start_date": "2026-06-03",
        "end_date": "2026-06-01",
    }, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 422


async def test_deactivate_event(client: AsyncClient, test_session: AsyncSession):
    token = await _get_token(client, test_session)
    create_resp = await client.post("/api/v1/events", json={
        "name": "To Deactivate", "start_date": "2026-01-01", "end_date": "2026-01-02",
    }, headers={"Authorization": f"Bearer {token}"})
    event_id = create_resp.json()["id"]

    response = await client.delete(f"/api/v1/events/{event_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.json()["is_active"] is False
