from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
)

from app.database.base import Base


if TYPE_CHECKING:
    from app.models.book import Book


class Quote(Base):

    __tablename__ = "quotes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id")
    )

    content: Mapped[str] = mapped_column(
        Text
    )

    page: Mapped[int] = mapped_column(
        Integer
    )

    # ======================
    # Reflection
    # ======================

    note: Mapped[str] = mapped_column(
        Text,
        default="",
    )

    tags: Mapped[str] = mapped_column(
        String(255),
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

    # ======================
    # Relationship
    # ======================

    book: Mapped["Book"] = relationship(
        back_populates="quotes"
    )