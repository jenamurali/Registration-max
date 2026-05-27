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


async def test_create_category(client: AsyncClient, test_session: AsyncSession):
    token = await _get_token(client, test_session)
    response = await client.post("/api/v1/categories", json={
        "name": "VIP",
        "is_printable": True,
        "description": "VIP Delegates",
    }, headers={"Authorization": f"Bearer {token}"})

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "VIP"
    assert data["allowed_kit"] is True


async def test_list_categories(client: AsyncClient, test_session: AsyncSession):
    token = await _get_token(client, test_session)
    await client.post("/api/v1/categories", json={"name": "Delegate"}, headers={"Authorization": f"Bearer {token}"})
    await client.post("/api/v1/categories", json={"name": "Speaker"}, headers={"Authorization": f"Bearer {token}"})

    response = await client.get("/api/v1/categories", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert len(response.json()) == 2


async def test_list_printable_only(client: AsyncClient, test_session: AsyncSession):
    token = await _get_token(client, test_session)
    await client.post("/api/v1/categories", json={
        "name": "Printable Cat", "is_printable": True,
    }, headers={"Authorization": f"Bearer {token}"})
    await client.post("/api/v1/categories", json={
        "name": "NonPrintable Cat", "is_printable": False,
    }, headers={"Authorization": f"Bearer {token}"})

    response = await client.get("/api/v1/categories?printable_only=true", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Printable Cat"


async def test_delete_category(client: AsyncClient, test_session: AsyncSession):
    token = await _get_token(client, test_session)
    create_resp = await client.post("/api/v1/categories", json={
        "name": "To Delete",
    }, headers={"Authorization": f"Bearer {token}"})
    cat_id = create_resp.json()["id"]

    response = await client.delete(f"/api/v1/categories/{cat_id}", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 204
