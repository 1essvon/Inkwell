from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database.base import Base
from app.constants.book_status import BookStatus


class Book(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    title: Mapped[str] = mapped_column(
        String(255)
    )

    author: Mapped[str] = mapped_column(
        String(255)
    )

    isbn: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True
    )

    publisher: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    published_year: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    genre: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    page_count: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    cover_path: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    current_page: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        default=BookStatus.WANT_TO_READ
    )

    rating: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    date_added: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )