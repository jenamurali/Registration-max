from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lunch_scan import LunchScan
from app.repositories.base import BaseRepository


class LunchScanRepository(BaseRepository[LunchScan]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, LunchScan)

    async def get_by_registration(self, registration_id: int) -> Optional[LunchScan]:
        result = await self._session.execute(
            select(LunchScan).where(LunchScan.registration_id == registration_id)
        )
        return result.scalar_one_or_none()

    async def get_by_event(self, event_id: int):
        result = await self._session.execute(
            select(LunchScan).where(LunchScan.event_id == event_id)
        )
        return list(result.scalars().all())
