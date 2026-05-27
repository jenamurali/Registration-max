from datetime import date, datetime

from pydantic import BaseModel, Field, model_validator


class EventCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    start_date: date
    end_date: date
    venue: str | None = Field(default=None, max_length=300)

    @model_validator(mode="after")
    def validate_dates(self):
        if self.end_date < self.start_date:
            raise ValueError("end_date must be on or after start_date")
        return self


class EventUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    start_date: date | None = None
    end_date: date | None = None
    venue: str | None = Field(default=None, max_length=300)
    is_active: bool | None = None


class EventResponse(BaseModel):
    id: int
    name: str
    start_date: date
    end_date: date
    venue: str | None
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
