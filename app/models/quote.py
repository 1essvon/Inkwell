from datetime import datetime

from sqlalchemy import Integer
from sqlalchemy import Text
from sqlalchemy import String
from sqlalchemy import DateTime

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database.base import Base


class Quote(Base):
    __tablename__ = "quotes"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True
    )

    quote_text: Mapped[str] = mapped_column(
        Text
    )

    source: Mapped[str | None] = mapped_column(
        String(255),
        nullable=True
    )

    page_number: Mapped[int | None] = mapped_column(
        Integer,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )