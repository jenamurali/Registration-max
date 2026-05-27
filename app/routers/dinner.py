from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_db_session
from app.schemas.scanning import ReissueRequest, ScanResult
from app.services.dinner_service import DinnerService

router = APIRouter(prefix="/dinner", tags=["dinner"])


@router.post("/issue", response_model=ScanResult)
async def issue_dinner(barcode: str, session: AsyncSession = Depends(get_db_session)):
    service = DinnerService(session)
    return await service.issue_plate(barcode)


@router.post("/reissue", response_model=ScanResult)
async def reissue_dinner(request: ReissueRequest, session: AsyncSession = Depends(get_db_session)):
    service = DinnerService(session)
    return await service.reissue_plate(request.barcode, request.remark)
