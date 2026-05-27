from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.card_layout import CardLayout
from app.repositories.base import BaseRepository


class CardLayoutRepository(BaseRepository[CardLayout]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, CardLayout)

    async def get_by_event(self, event_id: int) -> Optional[CardLayout]:
        result = await self._session.execute(
            select(CardLayout).where(CardLayout.event_id == event_id)
        )
        return result.scalar_one_or_none()
