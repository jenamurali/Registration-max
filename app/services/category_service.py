from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import NotFoundException
from app.models.category import Category
from app.repositories.category_repo import CategoryRepository
from app.schemas.category import CategoryCreate, CategoryUpdate


class CategoryService:
    def __init__(self, session: AsyncSession):
        self._repo = CategoryRepository(session)

    async def create_category(self, data: CategoryCreate) -> Category:
        category = Category(
            name=data.name,
            is_printable=data.is_printable,
            description=data.description,
            allowed_kit=data.allowed_kit,
            allowed_lunch=data.allowed_lunch,
            allowed_dinner=data.allowed_dinner,
        )
        return await self._repo.add(category)

    async def update_category(self, cat_id: int, data: CategoryUpdate) -> Category:
        category = await self._repo.get_by_id(cat_id)
        if not category:
            raise NotFoundException("Category not found")
        if data.name is not None:
            category.name = data.name
        if data.is_printable is not None:
            category.is_printable = data.is_printable
        if data.description is not None:
            category.description = data.description
        if data.allowed_kit is not None:
            category.allowed_kit = data.allowed_kit
        if data.allowed_lunch is not None:
            category.allowed_lunch = data.allowed_lunch
        if data.allowed_dinner is not None:
            category.allowed_dinner = data.allowed_dinner
        return await self._repo.update(category)

    async def get_category(self, cat_id: int) -> Category:
        category = await self._repo.get_by_id(cat_id)
        if not category:
            raise NotFoundException("Category not found")
        return category

    async def list_categories(self, printable_only: bool = False) -> List[Category]:
        if printable_only:
            return await self._repo.get_printable()
        return await self._repo.get_all()

    async def delete_category(self, cat_id: int) -> None:
        category = await self._repo.get_by_id(cat_id)
        if not category:
            raise NotFoundException("Category not found")
        await self._repo.delete(category)
