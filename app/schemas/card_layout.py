from datetime import datetime

from pydantic import BaseModel, Field


class CardLayoutUpdate(BaseModel):
    font_family: str | None = Field(default=None, max_length=100)
    font_size: int | None = None
    logo_position: str | None = Field(default=None, max_length=50)
    show_logo: bool | None = None
    show_company_logo: bool | None = None
    background_color: str | None = Field(default=None, max_length=20)
    field_positions: str | None = None


class CardLayoutResponse(BaseModel):
    id: int
    event_id: int
    font_family: str
    font_size: int
    logo_position: str
    show_logo: bool
    show_company_logo: bool
    background_color: str
    field_positions: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
