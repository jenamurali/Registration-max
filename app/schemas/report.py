from datetime import date, datetime

from pydantic import BaseModel


class ReportFilters(BaseModel):
    event_id: int
    start_date: date | None = None
    end_date: date | None = None
    category_id: int | None = None


class RegistrationReportRow(BaseModel):
    reg_no: str
    name: str
    company_name: str | None
    category_name: str
    city: str | None
    country: str | None
    mobile: str | None
    email: str | None
    is_paid: bool
    is_pre_registered: bool
    print_count: int
    registration_date: datetime

    model_config = {"from_attributes": True}


class ScanReportRow(BaseModel):
    name: str
    company_name: str | None
    reg_no: str
    category_name: str
    issued_at: datetime
    reissued: bool


class HallReportRow(BaseModel):
    name: str
    company_name: str | None
    reg_no: str
    hall_name: str
    session_name: str
    entry_time: datetime
    exit_time: datetime | None
