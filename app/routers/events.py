from typing import List

from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.deps import get_db_session
from app.schemas.event import EventCreate, EventResponse, EventUpdate
from app.services.event_service import EventService

router = APIRouter(prefix="/events", tags=["events"])


@router.post("", response_model=EventResponse, status_code=201)
async def create_event(data: EventCreate, session: AsyncSession = Depends(get_db_session)):
    service = EventService(session)
    return await service.create_event(data)


@router.get("", response_model=List[EventResponse])
async def list_events(
    active_only: bool = Query(False),
    session: AsyncSession = Depends(get_db_session),
):
    service = EventService(session)
    return await service.list_events(active_only=active_only)


@router.get("/{event_id}", response_model=EventResponse)
async def get_event(event_id: int, session: AsyncSession = Depends(get_db_session)):
    service = EventService(session)
    return await service.get_event(event_id)


@router.put("/{event_id}", response_model=EventResponse)
async def update_event(
    event_id: int, data: EventUpdate, session: AsyncSession = Depends(get_db_session)
):
    service = EventService(session)
    return await service.update_event(event_id, data)


@router.delete("/{event_id}", response_model=EventResponse)
async def deactivate_event(event_id: int, session: AsyncSession = Depends(get_db_session)):
    service = EventService(session)
    return await service.deactivate_event(event_id)
