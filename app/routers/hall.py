from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_db_session
from app.schemas.hall import (
    HallCreate, HallEntryResult, HallResponse, HallUpdate,
    SessionCreate, SessionResponse, SessionUpdate,
)
from app.services.hall_service import HallService

router = APIRouter(prefix="/hall", tags=["hall"])


@router.post("/halls", response_model=HallResponse, status_code=201)
async def create_hall(data: HallCreate, session: AsyncSession = Depends(get_db_session)):
    service = HallService(session)
    return await service.create_hall(data)


@router.get("/halls", response_model=List[HallResponse])
async def list_halls(event_id: int = Query(...), session: AsyncSession = Depends(get_db_session)):
    service = HallService(session)
    return await service.list_halls(event_id)


@router.put("/halls/{hall_id}", response_model=HallResponse)
async def update_hall(hall_id: int, data: HallUpdate, session: AsyncSession = Depends(get_db_session)):
    service = HallService(session)
    return await service.update_hall(hall_id, data)


@router.post("/sessions", response_model=SessionResponse, status_code=201)
async def create_session(data: SessionCreate, session: AsyncSession = Depends(get_db_session)):
    service = HallService(session)
    return await service.create_session(data)


@router.get("/sessions", response_model=List[SessionResponse])
async def list_sessions(hall_id: int = Query(...), session: AsyncSession = Depends(get_db_session)):
    service = HallService(session)
    return await service.list_sessions(hall_id)


@router.put("/sessions/{session_id}", response_model=SessionResponse)
async def update_session(session_id: int, data: SessionUpdate, session: AsyncSession = Depends(get_db_session)):
    service = HallService(session)
    return await service.update_session(session_id, data)


@router.post("/entry", response_model=HallEntryResult)
async def record_entry(
    barcode: str, hall_id: int, session_id: int,
    session: AsyncSession = Depends(get_db_session),
):
    service = HallService(session)
    return await service.record_entry(barcode, hall_id, session_id)


@router.post("/exit", response_model=HallEntryResult)
async def record_exit(barcode: str, session: AsyncSession = Depends(get_db_session)):
    service = HallService(session)
    return await service.record_exit(barcode)
