from datetime import datetime

from pydantic import BaseModel, Field


class HallCreate(BaseModel):
    event_id: int
    name: str = Field(min_length=1, max_length=200)


class HallUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    is_active: bool | None = None


class HallResponse(BaseModel):
    id: int
    event_id: int
    name: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SessionCreate(BaseModel):
    hall_id: int
    name: str = Field(min_length=1, max_length=200)
    start_time: datetime
    end_time: datetime


class SessionUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    start_time: datetime | None = None
    end_time: datetime | None = None


class SessionResponse(BaseModel):
    id: int
    hall_id: int
    name: str
    start_time: datetime
    end_time: datetime
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class HallEntryResponse(BaseModel):
    id: int
    registration_id: int
    hall_id: int
    session_id: int
    event_id: int
    entry_time: datetime
    exit_time: datetime | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class HallEntryResult(BaseModel):
    success: bool
    message: str
    entry_id: int | None = None
    entry_time: datetime | None = None
    exit_time: datetime | None = None
