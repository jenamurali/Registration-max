import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.services.auth_service import AuthService

pytestmark = pytest.mark.asyncio


async def test_signup_success(client: AsyncClient):
    response = await client.post("/api/v1/auth/signup", json={
        "username": "newuser",
        "email": "new@example.com",
        "password": "password123",
        "role": "admin",
    })

    assert response.status_code == 201
    data = response.json()
    assert data["username"] == "newuser"
    assert data["email"] == "new@example.com"
    assert data["role"] == "admin"
    assert data["is_active"] is True
    assert "id" in data


async def test_signup_duplicate_username(client: AsyncClient):
    await client.post("/api/v1/auth/signup", json={
        "username": "dupe", "email": "a@example.com", "password": "password123", "role": "operator",
    })
    response = await client.post("/api/v1/auth/signup", json={
        "username": "dupe", "email": "b@example.com", "password": "password123", "role": "operator",
    })

    assert response.status_code == 409


async def test_signup_duplicate_email(client: AsyncClient):
    await client.post("/api/v1/auth/signup", json={
        "username": "user1", "email": "same@example.com", "password": "password123", "role": "operator",
    })
    response = await client.post("/api/v1/auth/signup", json={
        "username": "user2", "email": "same@example.com", "password": "password123", "role": "operator",
    })

    assert response.status_code == 409


async def test_signup_validation_short_password(client: AsyncClient):
    response = await client.post("/api/v1/auth/signup", json={
        "username": "user3", "email": "u3@example.com", "password": "1234567", "role": "operator",
    })

    assert response.status_code == 422


async def test_signup_validation_invalid_role(client: AsyncClient):
    response = await client.post("/api/v1/auth/signup", json={
        "username": "user4", "email": "u4@example.com", "password": "password123", "role": "superadmin",
    })

    assert response.status_code == 422


async def test_login_success(client: AsyncClient, test_session: AsyncSession):
    auth_service = AuthService(test_session)
    await auth_service.create_user("testuser", "test@example.com", "password123", "admin")
    await test_session.commit()

    response = await client.post("/api/v1/auth/login", json={
        "username": "testuser",
        "password": "password123",
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert "refresh_token" in data
    assert data["token_type"] == "bearer"


async def test_login_invalid_password(client: AsyncClient, test_session: AsyncSession):
    auth_service = AuthService(test_session)
    await auth_service.create_user("testuser", "test@example.com", "password123", "admin")
    await test_session.commit()

    response = await client.post("/api/v1/auth/login", json={
        "username": "testuser",
        "password": "wrongpassword",
    })

    assert response.status_code == 401


async def test_login_nonexistent_user(client: AsyncClient):
    response = await client.post("/api/v1/auth/login", json={
        "username": "nobody",
        "password": "password123",
    })

    assert response.status_code == 401


async def test_login_inactive_user(client: AsyncClient, test_session: AsyncSession):
    auth_service = AuthService(test_session)
    user = await auth_service.create_user("testuser", "test@example.com", "password123", "operator")
    user.is_active = False
    test_session.add(user)
    await test_session.commit()

    response = await client.post("/api/v1/auth/login", json={
        "username": "testuser",
        "password": "password123",
    })

    assert response.status_code == 403


async def test_refresh_token(client: AsyncClient, test_session: AsyncSession):
    auth_service = AuthService(test_session)
    await auth_service.create_user("testuser", "test@example.com", "password123", "admin")
    await test_session.commit()

    login_resp = await client.post("/api/v1/auth/login", json={
        "username": "testuser",
        "password": "password123",
    })
    refresh_token = login_resp.json()["refresh_token"]

    response = await client.post("/api/v1/auth/refresh", json={
        "refresh_token": refresh_token,
    })

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data


async def test_refresh_with_access_token_fails(client: AsyncClient, test_session: AsyncSession):
    auth_service = AuthService(test_session)
    await auth_service.create_user("testuser", "test@example.com", "password123", "admin")
    await test_session.commit()

    login_resp = await client.post("/api/v1/auth/login", json={
        "username": "testuser",
        "password": "password123",
    })
    access_token = login_resp.json()["access_token"]

    response = await client.post("/api/v1/auth/refresh", json={
        "refresh_token": access_token,
    })

    assert response.status_code == 401


async def test_login_validation_short_username(client: AsyncClient):
    response = await client.post("/api/v1/auth/login", json={
        "username": "ab",
        "password": "password123",
    })

    assert response.status_code == 422


async def test_signup_and_login(client: AsyncClient):
    signup_resp = await client.post("/api/v1/auth/signup", json={
        "username": "fullflow", "email": "full@example.com",
        "password": "password123", "role": "operator",
    })
    assert signup_resp.status_code == 201

    login_resp = await client.post("/api/v1/auth/login", json={
        "username": "fullflow", "password": "password123",
    })
    assert login_resp.status_code == 200
    assert "access_token" in login_resp.json()


async def test_login_validation_empty_password(client: AsyncClient):
    response = await client.post("/api/v1/auth/login", json={
        "username": "testuser",
        "password": "",
    })

    assert response.status_code == 422
