from sqlalchemy import ForeignKey, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class CardLayout(Base):
    __tablename__ = "card_layouts"

    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), unique=True, nullable=False)
    font_family: Mapped[str] = mapped_column(String(100), default="Arial", nullable=False)
    font_size: Mapped[int] = mapped_column(default=12, nullable=False)
    logo_position: Mapped[str] = mapped_column(String(50), default="top-left", nullable=False)
    show_logo: Mapped[bool] = mapped_column(default=True, nullable=False)
    show_company_logo: Mapped[bool] = mapped_column(default=True, nullable=False)
    background_color: Mapped[str] = mapped_column(String(20), default="#FFFFFF", nullable=False)
    field_positions: Mapped[str] = mapped_column(Text, nullable=True)
