from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_db_session
from app.schemas.scanning import ReissueRequest, ScanResult
from app.services.kit_service import KITService

router = APIRouter(prefix="/kit", tags=["kit"])


@router.post("/issue", response_model=ScanResult)
async def issue_kit(barcode: str, session: AsyncSession = Depends(get_db_session)):
    service = KITService(session)
    return await service.issue_kit(barcode)


@router.get("/status", response_model=ScanResult)
async def check_status(barcode: str, session: AsyncSession = Depends(get_db_session)):
    service = KITService(session)
    return await service.check_status(barcode)


@router.post("/reissue", response_model=ScanResult)
async def reissue_kit(request: ReissueRequest, session: AsyncSession = Depends(get_db_session)):
    service = KITService(session)
    return await service.reissue_kit(request.barcode, request.remark)
