from datetime import datetime

from pydantic import BaseModel, Field


class RegistrationCreate(BaseModel):
    event_id: int
    category_id: int
    name: str = Field(min_length=1, max_length=200)
    name_line_adjust: str = Field(default="single", pattern=r"^(single|paragraph)$")
    company_name: str | None = Field(default=None, max_length=300)
    country: str | None = Field(default=None, max_length=100)
    city: str | None = Field(default=None, max_length=100)
    mobile: str | None = Field(default=None, max_length=20)
    email: str | None = Field(default=None, max_length=255)
    is_pre_registered: bool = False


class RegistrationUpdate(BaseModel):
    category_id: int | None = None
    name: str | None = Field(default=None, min_length=1, max_length=200)
    name_line_adjust: str | None = Field(default=None, pattern=r"^(single|paragraph)$")
    company_name: str | None = Field(default=None, max_length=300)
    country: str | None = Field(default=None, max_length=100)
    city: str | None = Field(default=None, max_length=100)
    mobile: str | None = Field(default=None, max_length=20)
    email: str | None = Field(default=None, max_length=255)
    photo_path: str | None = None
    logo_path: str | None = None


class RegistrationResponse(BaseModel):
    id: int
    event_id: int
    category_id: int
    reg_no: str
    barcode: str
    qr_code: str
    name: str
    name_line_adjust: str
    company_name: str | None
    country: str | None
    city: str | None
    mobile: str | None
    email: str | None
    photo_path: str | None
    logo_path: str | None
    is_paid: bool
    payment_method: str | None
    receipt_no: str | None
    is_pre_registered: bool
    print_count: int
    registration_date: datetime
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class RegistrationCounts(BaseModel):
    total: int
    pre_registered: int
    on_spot: int
    total_prints: int
