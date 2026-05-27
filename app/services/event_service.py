from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import NotFoundException, ValidationException
from app.models.event import Event
from app.repositories.event_repo import EventRepository
from app.schemas.event import EventCreate, EventUpdate


class EventService:
    def __init__(self, session: AsyncSession):
        self._repo = EventRepository(session)

    async def create_event(self, data: EventCreate) -> Event:
        if data.end_date < data.start_date:
            raise ValidationException("end_date must be on or after start_date")
        event = Event(
            name=data.name,
            start_date=data.start_date,
            end_date=data.end_date,
            venue=data.venue,
        )
        return await self._repo.add(event)

    async def update_event(self, event_id: int, data: EventUpdate) -> Event:
        event = await self._repo.get_by_id(event_id)
        if not event:
            raise NotFoundException("Event not found")
        if data.name is not None:
            event.name = data.name
        if data.start_date is not None:
            event.start_date = data.start_date
        if data.end_date is not None:
            event.end_date = data.end_date
        if data.venue is not None:
            event.venue = data.venue
        if data.is_active is not None:
            event.is_active = data.is_active
        if event.end_date < event.start_date:
            raise ValidationException("end_date must be on or after start_date")
        return await self._repo.update(event)

    async def get_event(self, event_id: int) -> Event:
        event = await self._repo.get_by_id(event_id)
        if not event:
            raise NotFoundException("Event not found")
        return event

    async def list_events(self, active_only: bool = False) -> List[Event]:
        if active_only:
            return await self._repo.get_active()
        return await self._repo.get_all()

    async def deactivate_event(self, event_id: int) -> Event:
        event = await self._repo.get_by_id(event_id)
        if not event:
            raise NotFoundException("Event not found")
        event.is_active = False
        return await self._repo.update(event)
