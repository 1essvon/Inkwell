from datetime import datetime

from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database.base import Base


class ReadingSession(Base):
    __tablename__ = "reading_sessions"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    book_id: Mapped[int] = mapped_column(
        ForeignKey("books.id")
    )

    start_page: Mapped[int] = mapped_column(
        Integer
    )

    end_page: Mapped[int] = mapped_column(
        Integer
    )

    duration_minutes: Mapped[int] = mapped_column(
        Integer
    )

    started_at: Mapped[datetime] = mapped_column(
        DateTime
    )

    ended_at: Mapped[datetime] = mapped_column(
        DateTime
    )