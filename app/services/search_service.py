from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.registration import Registration
from app.repositories.registration_repo import RegistrationRepository


class SearchService:
    def __init__(self, session: AsyncSession):
        self._repo = RegistrationRepository(session)

    async def search(self, **kwargs) -> List[Registration]:
        return await self._repo.search(**kwargs)
