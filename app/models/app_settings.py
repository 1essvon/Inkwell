from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    Integer,
    String
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column
)

from app.database.base import Base


class AppSettings(Base):

    __tablename__ = "app_settings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    theme: Mapped[str] = mapped_column(
        String(50),
        default="Dark"
    )

    autosave_scratchpad: Mapped[bool] = mapped_column(
        Boolean,
        default=False
    )

    confirm_before_clear: Mapped[bool] = mapped_column(
        Boolean,
        default=True
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )