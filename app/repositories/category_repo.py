from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.category import Category
from app.repositories.base import BaseRepository


class CategoryRepository(BaseRepository[Category]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Category)

    async def get_by_name(self, name: str) -> Optional[Category]:
        result = await self._session.execute(
            select(Category).where(Category.name == name)
        )
        return result.scalar_one_or_none()

    async def get_printable(self) -> List[Category]:
        result = await self._session.execute(
            select(Category).where(Category.is_printable == True)
        )
        return list(result.scalars().all())

    async def get_non_printable(self) -> List[Category]:
        result = await self._session.execute(
            select(Category).where(Category.is_printable == False)
        )
        return list(result.scalars().all())
