from typing import List, Optional

from sqlalchemy import func, or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.registration import Registration
from app.repositories.base import BaseRepository


class RegistrationRepository(BaseRepository[Registration]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Registration)

    async def get_by_reg_no(self, reg_no: str) -> Optional[Registration]:
        result = await self._session.execute(
            select(Registration).where(Registration.reg_no == reg_no)
        )
        return result.scalar_one_or_none()

    async def get_by_barcode(self, barcode: str) -> Optional[Registration]:
        result = await self._session.execute(
            select(Registration).where(Registration.barcode == barcode)
        )
        return result.scalar_one_or_none()

    async def get_by_event(self, event_id: int) -> List[Registration]:
        result = await self._session.execute(
            select(Registration).where(Registration.event_id == event_id)
        )
        return list(result.scalars().all())

    async def search(
        self,
        name: str | None = None,
        company_name: str | None = None,
        email: str | None = None,
        mobile: str | None = None,
        city: str | None = None,
        country: str | None = None,
        event_id: int | None = None,
    ) -> List[Registration]:
        query = select(Registration)
        conditions = []
        if name:
            conditions.append(Registration.name.ilike(f"%{name}%"))
        if company_name:
            conditions.append(Registration.company_name.ilike(f"%{company_name}%"))
        if email:
            conditions.append(Registration.email.ilike(f"%{email}%"))
        if mobile:
            conditions.append(Registration.mobile.ilike(f"%{mobile}%"))
        if city:
            conditions.append(Registration.city.ilike(f"%{city}%"))
        if country:
            conditions.append(Registration.country.ilike(f"%{country}%"))
        if event_id:
            conditions.append(Registration.event_id == event_id)
        if conditions:
            query = query.where(or_(*conditions))
        result = await self._session.execute(query)
        return list(result.scalars().all())

    async def get_counts(self, event_id: int):
        total = await self._session.scalar(
            select(func.count()).select_from(Registration).where(Registration.event_id == event_id)
        )
        pre_reg = await self._session.scalar(
            select(func.count())
            .select_from(Registration)
            .where(Registration.event_id == event_id, Registration.is_pre_registered == True)
        )
        total_prints = await self._session.scalar(
            select(func.sum(Registration.print_count))
            .select_from(Registration)
            .where(Registration.event_id == event_id)
        )
        return {
            "total": total or 0,
            "pre_registered": pre_reg or 0,
            "on_spot": (total or 0) - (pre_reg or 0),
            "total_prints": total_prints or 0,
        }
