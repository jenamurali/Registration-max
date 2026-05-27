from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notification import Notification
from app.repositories.base import BaseRepository


class NotificationRepository(BaseRepository[Notification]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Notification)

    async def get_pending(self) -> List[Notification]:
        result = await self._session.execute(
            select(Notification).where(Notification.is_sent == False)
        )
        return list(result.scalars().all())

    async def mark_sent(self, notif_id: int) -> None:
        notif = await self.get_by_id(notif_id)
        if notif:
            from datetime import datetime
            notif.is_sent = True
            notif.sent_at = datetime.utcnow()
            await self._session.flush()

    async def mark_failed(self, notif_id: int, error: str) -> None:
        notif = await self.get_by_id(notif_id)
        if notif:
            notif.error_message = error
            await self._session.flush()
