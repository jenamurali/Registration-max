from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_db_session
from app.services.display_service import DisplayService

router = APIRouter(prefix="/display", tags=["display"])


@router.get("/barcode")
async def get_display_by_barcode(barcode: str, session: AsyncSession = Depends(get_db_session)):
    service = DisplayService(session)
    return await service.get_display_data(barcode)
