from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_db_session
from app.schemas.scanning import ReissueRequest, ScanResult
from app.services.lunch_service import LunchService

router = APIRouter(prefix="/lunch", tags=["lunch"])


@router.post("/issue", response_model=ScanResult)
async def issue_lunch(barcode: str, session: AsyncSession = Depends(get_db_session)):
    service = LunchService(session)
    return await service.issue_plate(barcode)


@router.post("/reissue", response_model=ScanResult)
async def reissue_lunch(request: ReissueRequest, session: AsyncSession = Depends(get_db_session)):
    service = LunchService(session)
    return await service.reissue_plate(request.barcode, request.remark)
