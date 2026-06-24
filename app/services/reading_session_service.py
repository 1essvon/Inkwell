from datetime import datetime

from app.database.session import SessionLocal

from app.models.reading_session import (
    ReadingSession
)


class ReadingSessionService:

    @staticmethod
    def create_session(
        book_id: int,
        start_page: int,
        end_page: int,
        duration_minutes: int
    ):

        session = SessionLocal()

        try:

            reading_session = (
                ReadingSession(
                    book_id=book_id,
                    start_page=start_page,
                    end_page=end_page,
                    duration_minutes=duration_minutes,
                    started_at=datetime.utcnow(),
                    ended_at=datetime.utcnow()
                )
            )

            session.add(
                reading_session
            )

            session.commit()

        finally:
            session.close()

    @staticmethod
    def get_all_sessions():

        session = SessionLocal()

        try:

            return session.query(
                ReadingSession
            ).all()

        finally:
            session.close()