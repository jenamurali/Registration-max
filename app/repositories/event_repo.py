from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.event import Event
from app.repositories.base import BaseRepository


class EventRepository(BaseRepository[Event]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Event)

    async def get_active(self) -> List[Event]:
        result = await self._session.execute(
            select(Event).where(Event.is_active == True)
        )
        return list(result.scalars().all())
