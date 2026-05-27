from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class LunchScan(Base):
    __tablename__ = "lunch_scans"

    registration_id: Mapped[int] = mapped_column(ForeignKey("registrations.id"), unique=True, nullable=False)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False, index=True)
    issued_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    reissued: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    reissue_remark: Mapped[str] = mapped_column(String(500), nullable=True)
