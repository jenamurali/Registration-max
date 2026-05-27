from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.certificate import CertificateTemplate
from app.repositories.base import BaseRepository


class CertificateRepository(BaseRepository[CertificateTemplate]):
    def __init__(self, session: AsyncSession):
        super().__init__(session, CertificateTemplate)

    async def get_by_event(self, event_id: int) -> Optional[CertificateTemplate]:
        result = await self._session.execute(
            select(CertificateTemplate).where(CertificateTemplate.event_id == event_id)
        )
        return result.scalar_one_or_none()
