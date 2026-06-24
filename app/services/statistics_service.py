from app.database.session import SessionLocal

from app.models.book import Book
from app.models.note import Note
from app.models.quote import Quote
from app.models.reading_session import (
    ReadingSession
)


class StatisticsService:

    @staticmethod
    def get_statistics():

        session = SessionLocal()

        try:

            reading_sessions = (
                session.query(
                    ReadingSession
                ).all()
            )

            total_pages = sum(
                s.end_page - s.start_page
                for s in reading_sessions
            )

            total_minutes = sum(
                s.duration_minutes
                for s in reading_sessions
            )

            return {

                "books":
                    session.query(Book).count(),

                "notes":
                    session.query(Note).count(),

                "quotes":
                    session.query(Quote).count(),

                "reading_sessions":
                    len(reading_sessions),

                "pages_read":
                    total_pages,

                "reading_minutes":
                    total_minutes
            }

        finally:
            session.close()