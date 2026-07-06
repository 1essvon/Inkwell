from sqlalchemy import func

from app.database.session import SessionLocal

from app.models.book import Book
from app.models.note import Note
from app.models.quote import Quote

from app.constants.book_status import (
    BookStatus
)

class StatisticsService:

    @staticmethod
    def get_library_statistics():

        session = SessionLocal()

        try:

            books = session.query(Book).all()

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
                )

            }

        finally:

            session.close()

    @staticmethod
    def get_reading_statistics():

        session = SessionLocal()

        try:

            books = session.query(Book).all()

            total_pages = sum(

                book.current_page or 0

                for book in books

            )

            active_books = sum(

                1

                for book in books

                if book.status == BookStatus.READING

            )

            average_progress = 0

            progress = []

            for book in books:

                if book.page_count:

                    progress.append(

                        (book.current_page or 0)

                        / book.page_count

                        * 100

                    )

            if progress:

                average_progress = round(

                    sum(progress)

                    / len(progress),

                    1

                )

            longest_book = None

            shortest_book = None

            completed_books = [

                book

                for book in books

                if book.page_count

            ]

            if completed_books:

                longest_book = max(

                    completed_books,

                    key=lambda b: b.page_count

                ).title

                shortest_book = min(

                    completed_books,

                    key=lambda b: b.page_count

                ).title

            return {

            "pages_read": total_pages,

            "active_books": active_books,

            "average_progress": average_progress,

            "longest_book": longest_book or "-",

            "shortest_book": shortest_book or "-"

        }

        finally:

            session.close()

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
                ).count()

            }

        finally:

            session.close()

    @staticmethod
    def get_statistics():

        library = (
            StatisticsService
            .get_library_statistics()
        )

        reading = (
            StatisticsService
            .get_reading_statistics()
        )

        journal = (
            StatisticsService
            .get_journal_statistics()
        )

        return {

            # Dashboard compatibility

            "books": library["total_books"],

            "notes": journal["notes"],

            "quotes": journal["quotes"],

            # Belum punya Reading Session model
            "reading_sessions": 0,

            "pages_read": reading["pages_read"],

            # Belum punya Focus/Timer
            "reading_minutes": 0,

            # Statistics Page

            **library,

            **reading,

            **journal

        }