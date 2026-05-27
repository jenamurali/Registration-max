from datetime import datetime

from pydantic import BaseModel, Field


class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    is_printable: bool = True
    description: str | None = Field(default=None, max_length=500)
    allowed_kit: bool = True
    allowed_lunch: bool = True
    allowed_dinner: bool = True


class CategoryUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    is_printable: bool | None = None
    description: str | None = Field(default=None, max_length=500)
    allowed_kit: bool | None = None
    allowed_lunch: bool | None = None
    allowed_dinner: bool | None = None


class CategoryResponse(BaseModel):
    id: int
    name: str
    is_printable: bool
    description: str | None
    allowed_kit: bool
    allowed_lunch: bool
    allowed_dinner: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
