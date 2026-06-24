from app.database.base import Base
from app.database.engine import engine

from app.models.book import Book
from app.models.note import Note
from app.models.quote import Quote


def init_database():
    Base.metadata.create_all(bind=engine)
