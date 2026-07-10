from datetime import date
from datetime import timedelta

from sqlalchemy import func

from app.database.session import (
    SessionLocal,
)

from app.models.book import (
    Book,
)

from app.models.note import (
    Note,
)

from app.models.quote import (
    Quote,
)

from app.models.reading_session import (
    ReadingSession,
)

from app.constants.book_status import (
    BookStatus,
)


class StatisticsService:

    # ==========================
    # Library
    # ==========================

    @staticmethod
    def get_library_statistics():

        session = SessionLocal()

        try:

            books = session.query(
                Book
            ).all()

            return {

                "total_books": len(books),

                "reading": sum(
                    1
                    for b in books
                    if b.status == BookStatus.READING
                ),

                "completed": sum(
                    1
                    for b in books
                    if b.status == BookStatus.COMPLETED
                ),

                "want_to_read": sum(
                    1
                    for b in books
                    if b.status == BookStatus.WANT_TO_READ
                ),

                "paused": sum(
                    1
                    for b in books
                    if b.status == BookStatus.PAUSED
                ),

                "dropped": sum(
                    1
                    for b in books
                    if b.status == BookStatus.DROPPED
                ),

            }

        finally:

            session.close()

    # ==========================
    # Reading
    # ==========================

    @staticmethod
    def get_reading_statistics():

        session = SessionLocal()

        try:

            books = session.query(
                Book
            ).all()

            total_pages = sum(
                book.current_page or 0
                for book in books
            )

            active_books = sum(
                1
                for book in books
                if book.status == BookStatus.READING
            )

            progress = []

            for book in books:

                if book.page_count:

                    progress.append(

                        (
                            (book.current_page or 0)
                            / book.page_count
                        )
                        * 100

                    )

            average_progress = 0

            if progress:

                average_progress = round(

                    sum(progress)
                    / len(progress),

                    1,

                )

            valid_books = [

                b

                for b in books

                if b.page_count

            ]

            longest_book = "-"

            shortest_book = "-"

            if valid_books:

                longest_book = max(

                    valid_books,

                    key=lambda b: b.page_count,

                ).title

                shortest_book = min(

                    valid_books,

                    key=lambda b: b.page_count,

                ).title

            sessions = session.query(
                ReadingSession
            ).count()

            minutes = (

                session.query(

                    func.sum(
                        ReadingSession.duration_minutes
                    )

                ).scalar()

                or 0

            )

            return {

                "pages_read": total_pages,

                "active_books": active_books,

                "average_progress": average_progress,

                "longest_book": longest_book,

                "shortest_book": shortest_book,

                "reading_sessions": sessions,

                "reading_minutes": minutes,

            }

        finally:

            session.close()

    # ==========================
    # Journal
    # ==========================

    @staticmethod
    def get_journal_statistics():

        session = SessionLocal()

        try:

            return {

                "notes": session.query(
                    Note
                ).count(),

                "quotes": session.query(
                    Quote
                ).count(),

            }

        finally:

            session.close()

    # ==========================
    # Reading Streak
    # ==========================

    @staticmethod
    def get_reading_streak():

        session = SessionLocal()

        try:

            sessions = (

                session.query(
                    ReadingSession
                )

                .order_by(
                    ReadingSession.started_at
                )

                .all()

            )

            if not sessions:

                return {

                    "current": 0,

                    "best": 0,

                    "last_read": None,

                }

            days = sorted(

                {

                    s.started_at.date()

                    for s in sessions

                }

            )

            # ----------------------
            # Best streak
            # ----------------------

            best = 1

            streak = 1

            for previous, current in zip(

                days,

                days[1:],

            ):

                if current == previous + timedelta(days=1):

                    streak += 1

                    best = max(

                        best,

                        streak,

                    )

                else:

                    streak = 1

            # ----------------------
            # Current streak
            # ----------------------

            current = 0

            today = date.today()

            cursor = today

            day_set = set(days)

            while cursor in day_set:

                current += 1

                cursor -= timedelta(days=1)

            # Jika hari ini belum membaca,
            # tetapi kemarin membaca,
            # streak masih dihitung.

            if current == 0:

                cursor = today - timedelta(days=1)

                while cursor in day_set:

                    current += 1

                    cursor -= timedelta(days=1)

            return {

                "current": current,

                "best": best,

                "last_read": days[-1],

            }

        finally:

            session.close()

    # ==========================
    # Combined
    # ==========================

    @staticmethod
    def get_statistics():

        library = (
            StatisticsService.get_library_statistics()
        )

        reading = (
            StatisticsService.get_reading_statistics()
        )

        journal = (
            StatisticsService.get_journal_statistics()
        )

        streak = (
            StatisticsService.get_reading_streak()
        )

        return {

            # Dashboard

            "books": library["total_books"],

            "notes": journal["notes"],

            "quotes": journal["quotes"],

            "reading_sessions": reading["reading_sessions"],

            "pages_read": reading["pages_read"],

            "reading_minutes": reading["reading_minutes"],

            "reading_streak": streak["current"],

            "best_streak": streak["best"],

            # Statistics page

            **library,

            **reading,

            **journal,

            **streak,

        }