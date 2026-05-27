from datetime import datetime

from pydantic import BaseModel, Field


class ScanResult(BaseModel):
    success: bool
    message: str
    registration_id: int | None = None
    issued_at: datetime | None = None
    already_issued: bool = False
    original_issued_at: datetime | None = None


class ReissueRequest(BaseModel):
    barcode: str
    remark: str = Field(min_length=1, max_length=500)


class KITIssueResponse(BaseModel):
    id: int
    registration_id: int
    event_id: int
    issued_at: datetime
    reissued: bool
    reissue_remark: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
