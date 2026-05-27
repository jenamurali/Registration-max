from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.kit_issue import KITIssue
from app.repositories.base import BaseRepository


class KITIssueRepository(BaseRepository[KITIssue]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, KITIssue)

    async def get_by_registration(self, registration_id: int) -> Optional[KITIssue]:
        result = await self._session.execute(
            select(KITIssue).where(KITIssue.registration_id == registration_id)
        )
        return result.scalar_one_or_none()

    async def get_by_event(self, event_id: int):
        result = await self._session.execute(
            select(KITIssue).where(KITIssue.event_id == event_id)
        )
        return list(result.scalars().all())
