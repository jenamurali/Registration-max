from datetime import datetime

from sqlalchemy import DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class HallEntry(Base):
    __tablename__ = "hall_entries"

    registration_id: Mapped[int] = mapped_column(ForeignKey("registrations.id"), nullable=False, index=True)
    hall_id: Mapped[int] = mapped_column(ForeignKey("halls.id"), nullable=False)
    session_id: Mapped[int] = mapped_column(ForeignKey("sessions.id"), nullable=False)
    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), nullable=False, index=True)
    entry_time: Mapped[datetime] = mapped_column(DateTime, server_default=func.now(), nullable=False)
    exit_time: Mapped[datetime] = mapped_column(DateTime, nullable=True)
