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


class Note(Base):

    __tablename__ = "notes"

    # ======================================
    # Primary Key
    # ======================================

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
    )

    # ======================================
    # Relationships
    # ======================================

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id"),
        nullable=False,
    )

    # ======================================
    # Reading Context
    # ======================================

    page: Mapped[int] = mapped_column(
        Integer,
        default=1,
    )

    # ======================================
    # Note Content
    # ======================================

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False,
    )

    content: Mapped[str] = mapped_column(
        Text,
        default="",
    )

    # ======================================
    # Timestamps
    # ======================================

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )

    # ======================================
    # ORM Relationships
    # ======================================

    book: Mapped["Book"] = relationship(
        back_populates="notes",
    )