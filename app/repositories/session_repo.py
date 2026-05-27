from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.session import Session
from app.repositories.base import BaseRepository


class SessionRepository(BaseRepository[Session]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Session)

    async def get_by_hall(self, hall_id: int) -> List[Session]:
        result = await self._session.execute(
            select(Session).where(Session.hall_id == hall_id)
        )
        return list(result.scalars().all())
