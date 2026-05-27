import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.user_repo import UserRepository
from app.unit_of_work import UnitOfWork

pytestmark = pytest.mark.asyncio


async def test_uow_add_and_commit(test_session: AsyncSession):
    async with UnitOfWork(test_session) as uow:
        user = User(username="uow_test", email="uow@example.com", password_hash="hashed", role="operator")
        await uow.users.add(user)
        await uow.commit()

    repo = UserRepository(test_session)
    found = await repo.get_by_username("uow_test")
    assert found is not None
    assert found.email == "uow@example.com"


async def test_uow_rollback_on_exception(test_session: AsyncSession):
    try:
        async with UnitOfWork(test_session) as uow:
            user = User(username="rollback_test", email="rb@example.com", password_hash="hashed", role="operator")
            await uow.users.add(user)
            raise ValueError("simulated error")
    except ValueError:
        pass

    repo = UserRepository(test_session)
    found = await repo.get_by_username("rollback_test")
    assert found is None


async def test_uow_lazy_repository(test_session: AsyncSession):
    async with UnitOfWork(test_session) as uow:
        assert uow._users is None
        _ = uow.users
        assert uow._users is not None


async def test_user_repository_get_by_username(test_session: AsyncSession):
    repo = UserRepository(test_session)
    user = User(username="repotest", email="repo@example.com", password_hash="hashed", role="operator")
    test_session.add(user)
    await test_session.commit()

    found = await repo.get_by_username("repotest")
    assert found is not None
    assert found.email == "repo@example.com"

    not_found = await repo.get_by_username("nonexistent")
    assert not_found is None


async def test_user_repository_get_by_email(test_session: AsyncSession):
    repo = UserRepository(test_session)
    user = User(username="emailtest", email="email@example.com", password_hash="hashed", role="operator")
    test_session.add(user)
    await test_session.commit()

    found = await repo.get_by_email("email@example.com")
    assert found is not None
    assert found.username == "emailtest"


async def test_user_repository_paginated(test_session: AsyncSession):
    repo = UserRepository(test_session)
    for i in range(15):
        user = User(username=f"pageuser{i}", email=f"page{i}@example.com", password_hash="hashed", role="operator")
        test_session.add(user)
    await test_session.commit()

    results, total = await repo.get_paginated(skip=0, limit=10)
    assert len(results) == 10
    assert total == 15

    results, total = await repo.get_paginated(skip=10, limit=10)
    assert len(results) == 5
