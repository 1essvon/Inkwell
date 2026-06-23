from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.database.base import Base


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
