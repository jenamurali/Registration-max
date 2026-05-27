from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Registration(Base):
    __tablename__ = "registrations"

    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False, index=True)
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)

    reg_no: Mapped[str] = mapped_column(String(50), unique=True, nullable=False, index=True)
    barcode: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    qr_code: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    name: Mapped[str] = mapped_column(String(200), nullable=False)
    name_line_adjust: Mapped[str] = mapped_column(String(20), default="single", nullable=False)
    company_name: Mapped[str] = mapped_column(String(300), nullable=True)
    country: Mapped[str] = mapped_column(String(100), nullable=True)
    city: Mapped[str] = mapped_column(String(100), nullable=True)
    mobile: Mapped[str] = mapped_column(String(20), nullable=True)
    email: Mapped[str] = mapped_column(String(255), nullable=True)

    photo_path: Mapped[str] = mapped_column(String(500), nullable=True)
    logo_path: Mapped[str] = mapped_column(String(500), nullable=True)

    is_paid: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    payment_method: Mapped[str] = mapped_column(String(50), nullable=True)
    receipt_no: Mapped[str] = mapped_column(String(100), nullable=True)

    is_pre_registered: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    print_count: Mapped[int] = mapped_column(Integer, default=0, nullable=False)

    registration_date: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)

    event = relationship("Event", lazy="selectin")
    category = relationship("Category", lazy="selectin")
