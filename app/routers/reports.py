from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_db_session
from app.schemas.report import HallReportRow, RegistrationReportRow, ScanReportRow
from app.services.report_service import ReportService

router = APIRouter(prefix="/reports", tags=["reports"])


@router.get("/registrations/{event_id}", response_model=List[RegistrationReportRow])
async def registration_report(event_id: int, session: AsyncSession = Depends(get_db_session)):
    service = ReportService(session)
    return await service.get_registration_report(event_id)


@router.get("/kit/{event_id}", response_model=List[ScanReportRow])
async def kit_report(event_id: int, session: AsyncSession = Depends(get_db_session)):
    service = ReportService(session)
    return await service.get_kit_report(event_id)


@router.get("/lunch/{event_id}", response_model=List[ScanReportRow])
async def lunch_report(event_id: int, session: AsyncSession = Depends(get_db_session)):
    service = ReportService(session)
    return await service.get_lunch_report(event_id)


@router.get("/dinner/{event_id}", response_model=List[ScanReportRow])
async def dinner_report(event_id: int, session: AsyncSession = Depends(get_db_session)):
    service = ReportService(session)
    return await service.get_dinner_report(event_id)


@router.get("/hall/{event_id}", response_model=List[HallReportRow])
async def hall_report(
    event_id: int, hall_id: int | None = Query(None),
    session: AsyncSession = Depends(get_db_session),
):
    service = ReportService(session)
    return await service.get_hall_report(event_id, hall_id)
