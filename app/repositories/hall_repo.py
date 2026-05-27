from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.hall import Hall
from app.repositories.base import BaseRepository


class HallRepository(BaseRepository[Hall]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Hall)

    async def get_by_event(self, event_id: int) -> List[Hall]:
        result = await self._session.execute(
            select(Hall).where(Hall.event_id == event_id)
        )
        return list(result.scalars().all())
