from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.custom_field import CustomField
from app.repositories.base import BaseRepository


class CustomFieldRepository(BaseRepository[CustomField]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, CustomField)

    async def get_by_event(self, event_id: int) -> List[CustomField]:
        result = await self._session.execute(
            select(CustomField)
            .where(CustomField.event_id == event_id)
            .order_by(CustomField.display_order)
        )
        return list(result.scalars().all())

    async def reorder(self, field_orders: list[tuple[int, int]]) -> None:
        for field_id, order in field_orders:
            field = await self.get_by_id(field_id)
            if field:
                field.display_order = order
        await self._session.flush()
