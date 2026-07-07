from app.database.base import Base
from app.database.engine import engine

# Import all models
from app.models.book import Book
from app.models.note import Note
from app.models.quote import Quote
from app.models.reading_session import ReadingSession
from app.models.scratchpad_entry import ScratchpadEntry
from app.models.app_settings import AppSettings


def init_database():

    Base.metadata.create_all(
        bind=engine
    )