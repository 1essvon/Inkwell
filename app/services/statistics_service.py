from app.database.session import SessionLocal

from app.models.book import Book
from app.models.note import Note
from app.models.quote import Quote


class StatisticsService:

    @staticmethod
    def get_statistics():

        session = SessionLocal()

        try:

            return {
                "books": session.query(Book).count(),
                "notes": session.query(Note).count(),
                "quotes": session.query(Quote).count()
            }

        finally:
            session.close()