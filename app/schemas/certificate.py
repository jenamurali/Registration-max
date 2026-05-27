from datetime import datetime

from pydantic import BaseModel, Field


class CertificateData(BaseModel):
    registration_id: int
    name: str
    company_name: str | None
    reg_no: str
    event_name: str
    category_name: str
    issued_at: datetime


class TemplateConfig(BaseModel):
    template_config: str


class CertificateTemplateResponse(BaseModel):
    id: int
    event_id: int
    template_config: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
