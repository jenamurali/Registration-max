import uuid
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import NotFoundException
from app.models.registration import Registration
from app.repositories.registration_repo import RegistrationRepository
from app.schemas.registration import RegistrationCounts, RegistrationCreate, RegistrationUpdate


class RegistrationService:
    def __init__(self, session: AsyncSession):
        self._repo = RegistrationRepository(session)

    async def register(self, data: RegistrationCreate) -> Registration:
        unique_id = uuid.uuid4().hex[:12].upper()
        reg = Registration(
            event_id=data.event_id,
            category_id=data.category_id,
            reg_no=f"REG-{unique_id}",
            barcode=f"BC-{unique_id}",
            qr_code=f"QR-{unique_id}",
            name=data.name,
            name_line_adjust=data.name_line_adjust,
            company_name=data.company_name,
            country=data.country,
            city=data.city,
            mobile=data.mobile,
            email=data.email,
            is_pre_registered=data.is_pre_registered,
        )
        return await self._repo.add(reg)

    async def update_registration(self, reg_id: int, data: RegistrationUpdate) -> Registration:
        reg = await self._repo.get_by_id(reg_id)
        if not reg:
            raise NotFoundException("Registration not found")
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(reg, field, value)
        return await self._repo.update(reg)

    async def get_registration(self, reg_id: int) -> Registration:
        reg = await self._repo.get_by_id(reg_id)
        if not reg:
            raise NotFoundException("Registration not found")
        return reg

    async def get_by_barcode(self, barcode: str) -> Registration:
        reg = await self._repo.get_by_barcode(barcode)
        if not reg:
            raise NotFoundException("Registration not found")
        return reg

    async def get_counts(self, event_id: int) -> RegistrationCounts:
        counts = await self._repo.get_counts(event_id)
        return RegistrationCounts(**counts)

    async def increment_print_count(self, reg_id: int) -> Registration:
        reg = await self._repo.get_by_id(reg_id)
        if not reg:
            raise NotFoundException("Registration not found")
        reg.print_count += 1
        return await self._repo.update(reg)

    async def delete_registration(self, reg_id: int) -> None:
        reg = await self._repo.get_by_id(reg_id)
        if not reg:
            raise NotFoundException("Registration not found")
        await self._repo.delete(reg)
