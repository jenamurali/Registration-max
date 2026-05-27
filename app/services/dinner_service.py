from datetime import datetime, time, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.models.dinner_scan import DinnerScan
from app.repositories.dinner_scan_repo import DinnerScanRepository
from app.repositories.registration_repo import RegistrationRepository
from app.schemas.scanning import ScanResult

DINNER_START = time(18, 0)
DINNER_END = time(23, 59, 59)


class DinnerService:
    def __init__(self, session: AsyncSession):
        self._scan_repo = DinnerScanRepository(session)
        self._reg_repo = RegistrationRepository(session)

    async def issue_plate(self, barcode: str) -> ScanResult:
        now = datetime.now(timezone.utc).time()
        if not (DINNER_START <= now <= DINNER_END):
            return ScanResult(success=False, message="Dinner time is 6:00 PM to midnight")

        reg = await self._reg_repo.get_by_barcode(barcode)
        if not reg:
            return ScanResult(success=False, message="Invalid barcode")

        existing = await self._scan_repo.get_by_registration(reg.id)
        if existing:
            return ScanResult(
                success=False, message="Plate already issued",
                registration_id=reg.id, already_issued=True,
                original_issued_at=existing.issued_at,
            )

        scan = DinnerScan(registration_id=reg.id, event_id=reg.event_id)
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
