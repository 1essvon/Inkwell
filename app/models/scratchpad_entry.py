from datetime import datetime

from sqlalchemy import (
    DateTime,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
)

from app.database.base import Base


class ScratchpadEntry(Base):

    __tablename__ = "scratchpad_entries"

    # ======================
    # Primary Key
    # ======================

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    # ======================
    # Content
    # ======================

    title: Mapped[str] = mapped_column(
        String(255),
        default="Untitled",
    )

    content: Mapped[str] = mapped_column(
        Text,
        default="",
    )

    # ======================
    # Timestamps
    # ======================

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )