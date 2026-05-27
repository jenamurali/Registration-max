from datetime import datetime, time, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.lunch_scan import LunchScan
from app.repositories.category_repo import CategoryRepository
from app.repositories.lunch_scan_repo import LunchScanRepository
from app.repositories.registration_repo import RegistrationRepository
from app.schemas.scanning import ScanResult

LUNCH_START = time(12, 0)
LUNCH_END = time(18, 0)


class LunchService:
    def __init__(self, session: AsyncSession):
        self._scan_repo = LunchScanRepository(session)
        self._reg_repo = RegistrationRepository(session)
        self._cat_repo = CategoryRepository(session)

    async def issue_plate(self, barcode: str) -> ScanResult:
        now = datetime.now(timezone.utc).time()
        if not (LUNCH_START <= now <= LUNCH_END):
            return ScanResult(success=False, message="Lunch time is 12:00 PM to 6:00 PM")

        reg = await self._reg_repo.get_by_barcode(barcode)
        if not reg:
            return ScanResult(success=False, message="Invalid barcode")

        category = await self._cat_repo.get_by_id(reg.category_id)
        if category and not category.allowed_lunch:
            return ScanResult(success=False, message=f"Category '{category.name}' not allowed for lunch")

        existing = await self._scan_repo.get_by_registration(reg.id)
        if existing:
            return ScanResult(
                success=False, message="Plate already issued",
                registration_id=reg.id, already_issued=True,
                original_issued_at=existing.issued_at,
            )

        scan = LunchScan(registration_id=reg.id, event_id=reg.event_id)
        scan = await self._scan_repo.add(scan)
        return ScanResult(
            success=True, message="Plate issued successfully",
            registration_id=reg.id, issued_at=scan.issued_at,
        )

    async def reissue_plate(self, barcode: str, remark: str) -> ScanResult:
        reg = await self._reg_repo.get_by_barcode(barcode)
        if not reg:
            return ScanResult(success=False, message="Invalid barcode")
        existing = await self._scan_repo.get_by_registration(reg.id)
        if not existing:
            return ScanResult(success=False, message="Plate not yet issued")
        existing.reissued = True
        existing.reissue_remark = remark
        await self._scan_repo.update(existing)
        return ScanResult(
            success=True, message="Plate reissued successfully",
            registration_id=reg.id, issued_at=datetime.now(timezone.utc),
        )
