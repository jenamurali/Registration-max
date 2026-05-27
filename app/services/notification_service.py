from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notification import Notification
from app.repositories.notification_repo import NotificationRepository
from app.schemas.notification import NotificationCreate


class NotificationService:
    def __init__(self, session: AsyncSession):
        self._repo = NotificationRepository(session)

    async def queue_notification(self, data: NotificationCreate) -> Notification:
        notif = Notification(**data.model_dump())
        return await self._repo.add(notif)

    async def get_pending(self) -> List[Notification]:
        return await self._repo.get_pending()

    async def mark_sent(self, notif_id: int) -> None:
        await self._repo.mark_sent(notif_id)

    async def mark_failed(self, notif_id: int, error: str) -> None:
        await self._repo.mark_failed(notif_id, error)
