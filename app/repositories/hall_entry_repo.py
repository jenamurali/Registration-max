from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.hall_entry import HallEntry
from app.repositories.base import BaseRepository


class HallEntryRepository(BaseRepository[HallEntry]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, HallEntry)

    async def get_active_entry(self, registration_id: int) -> Optional[HallEntry]:
        result = await self._session.execute(
            select(HallEntry).where(
                HallEntry.registration_id == registration_id,
                HallEntry.exit_time.is_(None),
            )
        )
        return result.scalar_one_or_none()

    async def get_by_hall(self, hall_id: int) -> List[HallEntry]:
        result = await self._session.execute(
            select(HallEntry).where(HallEntry.hall_id == hall_id)
        )
        return list(result.scalars().all())

    async def get_by_session(self, session_id: int) -> List[HallEntry]:
        result = await self._session.execute(
            select(HallEntry).where(HallEntry.session_id == session_id)
        )
        return list(result.scalars().all())

    async def get_by_event(self, event_id: int) -> List[HallEntry]:
        result = await self._session.execute(
            select(HallEntry).where(HallEntry.event_id == event_id)
        )
        return list(result.scalars().all())
