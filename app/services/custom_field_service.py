from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import NotFoundException
from app.models.custom_field import CustomField
from app.repositories.custom_field_repo import CustomFieldRepository
from app.schemas.custom_field import CustomFieldCreate, CustomFieldUpdate, FieldOrderUpdate


class CustomFieldService:
    def __init__(self, session: AsyncSession):
        self._repo = CustomFieldRepository(session)

    async def add_field(self, data: CustomFieldCreate) -> CustomField:
        field = CustomField(**data.model_dump())
        return await self._repo.add(field)

    async def update_field(self, field_id: int, data: CustomFieldUpdate) -> CustomField:
        field = await self._repo.get_by_id(field_id)
        if not field:
            raise NotFoundException("Custom field not found")
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(field, key, value)
        return await self._repo.update(field)

    async def remove_field(self, field_id: int) -> None:
        field = await self._repo.get_by_id(field_id)
        if not field:
            raise NotFoundException("Custom field not found")
        await self._repo.delete(field)

    async def list_fields(self, event_id: int) -> List[CustomField]:
        return await self._repo.get_by_event(event_id)

    async def reorder_fields(self, orders: List[FieldOrderUpdate]) -> List[CustomField]:
        updates = [(o.field_id, o.display_order) for o in orders]
        await self._repo.reorder(updates)
        return await self._repo.get_all()
