from datetime import datetime

from pydantic import BaseModel, Field


class NotificationCreate(BaseModel):
    registration_id: int
    event_id: int
    notif_type: str = Field(pattern=r"^(email|sms)$")
    recipient: str = Field(max_length=255)
    subject: str | None = Field(default=None, max_length=500)
    body: str | None = None


class NotificationResponse(BaseModel):
    id: int
    registration_id: int
    event_id: int
    notif_type: str
    recipient: str
    subject: str | None
    is_sent: bool
    sent_at: datetime | None
    error_message: str | None
    created_at: datetime

    model_config = {"from_attributes": True}
