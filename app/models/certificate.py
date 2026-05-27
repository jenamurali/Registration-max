from sqlalchemy import ForeignKey, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class CertificateTemplate(Base):
    __tablename__ = "certificate_templates"

    event_id: Mapped[int] = mapped_column(ForeignKey("events.id"), unique=True, nullable=False)
    template_config: Mapped[str] = mapped_column(Text, nullable=True)
