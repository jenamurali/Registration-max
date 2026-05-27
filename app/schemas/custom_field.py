from datetime import datetime

from pydantic import BaseModel, Field


class CustomFieldCreate(BaseModel):
    event_id: int
    field_name: str = Field(min_length=1, max_length=100)
    field_label: str = Field(min_length=1, max_length=200)
    field_type: str = Field(default="text", pattern=r"^(text|number|dropdown|date|textarea)$")
    is_required: bool = False
    is_printable: bool = True
    display_order: int = 0
    options: str | None = Field(default=None, max_length=1000)


class CustomFieldUpdate(BaseModel):
    field_name: str | None = Field(default=None, min_length=1, max_length=100)
    field_label: str | None = Field(default=None, min_length=1, max_length=200)
    field_type: str | None = Field(default=None, pattern=r"^(text|number|dropdown|date|textarea)$")
    is_required: bool | None = None
    is_printable: bool | None = None
    display_order: int | None = None
    options: str | None = Field(default=None, max_length=1000)


class CustomFieldResponse(BaseModel):
    id: int
    event_id: int
    field_name: str
    field_label: str
    field_type: str
    is_required: bool
    is_printable: bool
    display_order: int
    options: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class FieldOrderUpdate(BaseModel):
    field_id: int
    display_order: int
