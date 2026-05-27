from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_db_session
from app.schemas.card_layout import CardLayoutResponse, CardLayoutUpdate
from app.services.card_layout_service import CardLayoutService

router = APIRouter(prefix="/card-layouts", tags=["card_layouts"])


@router.get("/event/{event_id}", response_model=CardLayoutResponse)
async def get_layout(event_id: int, session: AsyncSession = Depends(get_db_session)):
    service = CardLayoutService(session)
    return await service.get_layout(event_id)


@router.put("/event/{event_id}", response_model=CardLayoutResponse)
async def save_layout(
    event_id: int, data: CardLayoutUpdate, session: AsyncSession = Depends(get_db_session)
):
    service = CardLayoutService(session)
    return await service.save_layout(event_id, data)
