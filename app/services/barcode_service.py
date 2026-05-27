from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import NotFoundException
from app.repositories.registration_repo import RegistrationRepository


class BarcodeService:
    def __init__(self, session: AsyncSession):
        self._reg_repo = RegistrationRepository(session)

    async def validate_barcode(self, barcode: str):
        reg = await self._reg_repo.get_by_barcode(barcode)
        if not reg:
            raise NotFoundException("Invalid barcode — registration not found")
        return reg

    def generate_barcode_value(self, registration_id: int) -> str:
        import hashlib
        digest = hashlib.sha256(str(registration_id).encode()).hexdigest()[:12].upper()
        return f"BC-{digest}"

    def generate_qr_value(self, registration_id: int) -> str:
        import hashlib
        digest = hashlib.sha256(f"QR-{registration_id}".encode()).hexdigest()[:12].upper()
        return f"QR-{digest}"
