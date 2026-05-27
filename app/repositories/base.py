from typing import Generic, List, Optional, Tuple, Type, TypeVar

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, session: AsyncSession, model: Type[T]):
        self._session = session
        self.model = model

    async def get_by_id(self, entity_id: int) -> Optional[T]:
        result = await self._session.execute(
            select(self.model).where(self.model.id == entity_id)
        )
        return result.scalar_one_or_none()

    async def get_all(self) -> List[T]:
        result = await self._session.execute(select(self.model))
        return list(result.scalars().all())

    async def add(self, entity: T) -> T:
        self._session.add(entity)
        await self._session.flush()
        return entity

    async def update(self, entity: T) -> T:
        await self._session.flush()
        await self._session.refresh(entity)
        return entity

    async def delete(self, entity: T) -> None:
        await self._session.delete(entity)
        await self._session.flush()

    async def get_paginated(self, skip: int = 0, limit: int = 100) -> Tuple[List[T], int]:
        total = await self._session.scalar(
            select(func.count()).select_from(self.model)
        )
        result = await self._session.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return list(result.scalars().all()), total
