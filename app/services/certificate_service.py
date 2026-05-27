from datetime import datetime, timezone
from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.certificate import CertificateTemplate
from app.repositories.certificate_repo import CertificateRepository
from app.repositories.registration_repo import RegistrationRepository
from app.schemas.certificate import CertificateData


class CertificateService:
    def __init__(self, session: AsyncSession):
        self._repo = CertificateRepository(session)
        self._reg_repo = RegistrationRepository(session)

    async def get_certificate_data(self, barcode: str) -> CertificateData:
        reg = await self._reg_repo.get_by_barcode(barcode)
        if not reg:
            from app.errors import NotFoundException
            raise NotFoundException("Registration not found")
        return CertificateData(
            registration_id=reg.id,
            name=reg.name,
            company_name=reg.company_name,
            reg_no=reg.reg_no,
            event_name=reg.event.name if reg.event else "",
            category_name=reg.category.name if reg.category else "",
            issued_at=datetime.now(timezone.utc),
        )

    async def search_certificate_data(self, query: str) -> List[CertificateData]:
        regs = await self._reg_repo.search(name=query)
        if not regs:
            regs = await self._reg_repo.search(company_name=query)
        return [
            CertificateData(
                registration_id=r.id, name=r.name, company_name=r.company_name,
                reg_no=r.reg_no,
                event_name=r.event.name if r.event else "",
                category_name=r.category.name if r.category else "",
                issued_at=datetime.now(timezone.utc),
            )
            for r in regs
        ]

    async def get_template(self, event_id: int) -> CertificateTemplate | None:
        return await self._repo.get_by_event(event_id)

    async def save_template(self, event_id: int, config: str) -> CertificateTemplate:
        existing = await self._repo.get_by_event(event_id)
        if existing:
            existing.template_config = config
            return await self._repo.update(existing)
        template = CertificateTemplate(event_id=event_id, template_config=config)
        return await self._repo.add(template)
