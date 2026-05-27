from datetime import datetime, timezone
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import ConflictException, NotFoundException, ValidationException
from app.models.hall import Hall
from app.models.hall_entry import HallEntry
from app.models.session import Session
from app.repositories.hall_entry_repo import HallEntryRepository
from app.repositories.hall_repo import HallRepository
from app.repositories.registration_repo import RegistrationRepository
from app.repositories.session_repo import SessionRepository
from app.schemas.hall import HallCreate, HallEntryResult, HallUpdate, SessionCreate, SessionUpdate


class HallService:
    def __init__(self, session: AsyncSession):
        self._hall_repo = HallRepository(session)
        self._session_repo = SessionRepository(session)
        self._entry_repo = HallEntryRepository(session)
        self._reg_repo = RegistrationRepository(session)

    async def create_hall(self, data: HallCreate) -> Hall:
        hall = Hall(event_id=data.event_id, name=data.name)
        return await self._hall_repo.add(hall)

    async def update_hall(self, hall_id: int, data: HallUpdate) -> Hall:
        hall = await self._hall_repo.get_by_id(hall_id)
        if not hall:
            raise NotFoundException("Hall not found")
        if data.name is not None:
            hall.name = data.name
        if data.is_active is not None:
            hall.is_active = data.is_active
        return await self._hall_repo.update(hall)

    async def list_halls(self, event_id: int) -> List[Hall]:
        return await self._hall_repo.get_by_event(event_id)

    async def create_session(self, data: SessionCreate) -> Session:
        session = Session(**data.model_dump())
        return await self._session_repo.add(session)

    async def update_session(self, session_id: int, data: SessionUpdate) -> Session:
        s = await self._session_repo.get_by_id(session_id)
        if not s:
            raise NotFoundException("Session not found")
        for key, value in data.model_dump(exclude_unset=True).items():
            setattr(s, key, value)
        return await self._session_repo.update(s)

    async def list_sessions(self, hall_id: int) -> List[Session]:
        return await self._session_repo.get_by_hall(hall_id)

    async def record_entry(self, barcode: str, hall_id: int, session_id: int) -> HallEntryResult:
        reg = await self._reg_repo.get_by_barcode(barcode)
        if not reg:
            return HallEntryResult(success=False, message="Invalid barcode")
        active = await self._entry_repo.get_active_entry(reg.id)
        if active:
            return HallEntryResult(success=False, message="Already inside a hall — exit first")
        entry = HallEntry(
            registration_id=reg.id, hall_id=hall_id,
            session_id=session_id, event_id=reg.event_id,
        )
        entry = await self._entry_repo.add(entry)
        return HallEntryResult(
            success=True, message="Entry recorded",
            entry_id=entry.id, entry_time=entry.entry_time,
        )

    async def record_exit(self, barcode: str) -> HallEntryResult:
        reg = await self._reg_repo.get_by_barcode(barcode)
        if not reg:
            return HallEntryResult(success=False, message="Invalid barcode")
        active = await self._entry_repo.get_active_entry(reg.id)
        if not active:
            return HallEntryResult(success=False, message="No active entry found")
        active.exit_time = datetime.now(timezone.utc)
        await self._entry_repo.update(active)
        return HallEntryResult(
            success=True, message="Exit recorded",
            entry_id=active.id, exit_time=active.exit_time,
        )
