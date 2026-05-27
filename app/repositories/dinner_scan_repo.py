from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.dinner_scan import DinnerScan
from app.repositories.base import BaseRepository


class DinnerScanRepository(BaseRepository[DinnerScan]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, DinnerScan)

    async def get_by_registration(self, registration_id: int) -> Optional[DinnerScan]:
        result = await self._session.execute(
            select(DinnerScan).where(DinnerScan.registration_id == registration_id)
        )
        return result.scalar_one_or_none()

    async def get_by_event(self, event_id: int):
        result = await self._session.execute(
            select(DinnerScan).where(DinnerScan.event_id == event_id)
        )
        return list(result.scalars().all())
