from datetime import datetime, timezone

from sqlalchemy.ext.asyncio import AsyncSession

from app.errors import ConflictException, NotFoundException, ValidationException
from app.models.kit_issue import KITIssue
from app.repositories.kit_issue_repo import KITIssueRepository
from app.repositories.registration_repo import RegistrationRepository
from app.schemas.scanning import ScanResult


class KITService:
    def __init__(self, session: AsyncSession):
        self._kit_repo = KITIssueRepository(session)
        self._reg_repo = RegistrationRepository(session)

    async def issue_kit(self, barcode: str) -> ScanResult:
        reg = await self._reg_repo.get_by_barcode(barcode)
        if not reg:
            return ScanResult(success=False, message="Invalid barcode")
        existing = await self._kit_repo.get_by_registration(reg.id)
        if existing:
            return ScanResult(
                success=False,
                message="KIT already issued",
                registration_id=reg.id,
                already_issued=True,
                original_issued_at=existing.issued_at,
            )
        kit = KITIssue(registration_id=reg.id, event_id=reg.event_id)
        kit = await self._kit_repo.add(kit)
        return ScanResult(
            success=True,
            message="KIT issued successfully",
            registration_id=reg.id,
            issued_at=kit.issued_at,
        )

    async def check_status(self, barcode: str) -> ScanResult:
        reg = await self._reg_repo.get_by_barcode(barcode)
        if not reg:
            return ScanResult(success=False, message="Invalid barcode")
        existing = await self._kit_repo.get_by_registration(reg.id)
        if existing:
            return ScanResult(
                success=True,
                message="KIT already issued",
                registration_id=reg.id,
                already_issued=True,
                original_issued_at=existing.issued_at,
            )
        return ScanResult(success=True, message="KIT not yet issued", registration_id=reg.id)

    async def reissue_kit(self, barcode: str, remark: str) -> ScanResult:
        reg = await self._reg_repo.get_by_barcode(barcode)
        if not reg:
            return ScanResult(success=False, message="Invalid barcode")
        existing = await self._kit_repo.get_by_registration(reg.id)
        if not existing:
            return ScanResult(success=False, message="KIT not yet issued — cannot reissue")
        existing.reissued = True
        existing.reissue_remark = remark
        await self._kit_repo.update(existing)
        return ScanResult(
            success=True,
            message="KIT reissued successfully",
            registration_id=reg.id,
            issued_at=datetime.now(timezone.utc),
        )
