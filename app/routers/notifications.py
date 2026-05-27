from typing import List

from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_db_session
from app.schemas.notification import NotificationCreate, NotificationResponse
from app.services.notification_service import NotificationService

router = APIRouter(prefix="/notifications", tags=["notifications"])


@router.post("", response_model=NotificationResponse, status_code=201)
async def queue_notification(
    data: NotificationCreate,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_db_session),
):
    service = NotificationService(session)
    notif = await service.queue_notification(data)
    background_tasks.add_task(_process_notification, notif.id)
    return notif


@router.get("/pending", response_model=List[NotificationResponse])
async def get_pending(session: AsyncSession = Depends(get_db_session)):
    service = NotificationService(session)
    return await service.get_pending()


async def _process_notification(notif_id: int) -> None:
    pass
