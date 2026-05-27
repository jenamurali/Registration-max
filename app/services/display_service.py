from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import NotFoundException
from app.repositories.registration_repo import RegistrationRepository


class DisplayService:
    def __init__(self, session: AsyncSession):
        self._reg_repo = RegistrationRepository(session)

    async def get_display_data(self, barcode: str) -> dict:
        reg = await self._reg_repo.get_by_barcode(barcode)
        if not reg:
            raise NotFoundException("Registration not found")
        return {
            "name": reg.name,
            "company_name": reg.company_name,
            "category": reg.category.name if reg.category else None,
            "photo_path": reg.photo_path,
            "city": reg.city,
            "country": reg.country,
        }
