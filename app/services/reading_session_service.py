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

    @staticmethod
    def get_recent_sessions(
        limit=20
    ):

        session = SessionLocal()

        try:

            return (

                session.query(
                    ReadingSession
                )

                .order_by(
                    ReadingSession.ended_at.desc()
                )

                .limit(limit)

                .all()

            )

        finally:

            session.close()

    @staticmethod
    def get_sessions_by_book(
        book_id: int
    ):

        session = SessionLocal()

        try:

            return (

                session.query(
                    ReadingSession
                )

                .filter(
                    ReadingSession.book_id == book_id
                )

                .order_by(
                    ReadingSession.started_at.desc()
                )

                .all()

            )

        finally:

            session.close()

    @staticmethod
    def get_total_pages_read():

        sessions = (
            ReadingSessionService
            .get_all_sessions()
        )

        return sum(

            session.end_page
            - session.start_page

            for session in sessions

        )
    
    @staticmethod
    def get_total_reading_minutes():

        sessions = (
            ReadingSessionService
            .get_all_sessions()
        )

        return sum(

            session.duration_minutes

            for session in sessions

        )
    
    