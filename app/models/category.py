from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Category(Base):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    is_printable: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=True)
    allowed_kit: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    allowed_lunch: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
    allowed_dinner: Mapped[bool] = mapped_column(Boolean, default=True, nullable=False)
