from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.dinner_scan_repo import DinnerScanRepository
from app.repositories.hall_entry_repo import HallEntryRepository
from app.repositories.kit_issue_repo import KITIssueRepository
from app.repositories.lunch_scan_repo import LunchScanRepository
from app.repositories.registration_repo import RegistrationRepository
from app.schemas.report import HallReportRow, RegistrationReportRow, ScanReportRow


class ReportService:
    def __init__(self, session: AsyncSession):
        self._session = session
        self._reg_repo = RegistrationRepository(session)
        self._kit_repo = KITIssueRepository(session)
        self._lunch_repo = LunchScanRepository(session)
        self._dinner_repo = DinnerScanRepository(session)
        self._entry_repo = HallEntryRepository(session)

    async def get_registration_report(self, event_id: int) -> List[RegistrationReportRow]:
        regs = await self._reg_repo.get_by_event(event_id)
        return [
            RegistrationReportRow(
                reg_no=r.reg_no, name=r.name, company_name=r.company_name,
                category_name=r.category.name if r.category else "",
                city=r.city, country=r.country, mobile=r.mobile, email=r.email,
                is_paid=r.is_paid, is_pre_registered=r.is_pre_registered,
                print_count=r.print_count, registration_date=r.registration_date,
            )
            for r in regs
        ]

    async def get_kit_report(self, event_id: int) -> List[ScanReportRow]:
        issues = await self._kit_repo.get_by_event(event_id)
        result = []
        for i in issues:
            reg = await self._reg_repo.get_by_id(i.registration_id)
            if reg:
                result.append(ScanReportRow(
                    name=reg.name, company_name=reg.company_name, reg_no=reg.reg_no,
                    category_name=reg.category.name if reg.category else "",
                    issued_at=i.issued_at, reissued=i.reissued,
                ))
        return result

    async def get_lunch_report(self, event_id: int) -> List[ScanReportRow]:
        scans = await self._lunch_repo.get_by_event(event_id)
        result = []
        for s in scans:
            reg = await self._reg_repo.get_by_id(s.registration_id)
            if reg:
                result.append(ScanReportRow(
                    name=reg.name, company_name=reg.company_name, reg_no=reg.reg_no,
                    category_name=reg.category.name if reg.category else "",
                    issued_at=s.issued_at, reissued=s.reissued,
                ))
        return result

    async def get_dinner_report(self, event_id: int) -> List[ScanReportRow]:
        scans = await self._dinner_repo.get_by_event(event_id)
        result = []
        for s in scans:
            reg = await self._reg_repo.get_by_id(s.registration_id)
            if reg:
                result.append(ScanReportRow(
                    name=reg.name, company_name=reg.company_name, reg_no=reg.reg_no,
                    category_name=reg.category.name if reg.category else "",
                    issued_at=s.issued_at, reissued=s.reissued,
                ))
        return result

    async def get_hall_report(self, event_id: int, hall_id: int | None = None) -> List[HallReportRow]:
        if hall_id:
            entries = await self._entry_repo.get_by_hall(hall_id)
        else:
            entries = await self._entry_repo.get_by_event(event_id)
        result = []
        for e in entries:
            reg = await self._reg_repo.get_by_id(e.registration_id)
            if reg:
                result.append(HallReportRow(
                    name=reg.name, company_name=reg.company_name, reg_no=reg.reg_no,
                    hall_name="", session_name="",
                    entry_time=e.entry_time, exit_time=e.exit_time,
                ))
        return result
