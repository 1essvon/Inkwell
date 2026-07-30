from app.database.session import SessionLocal

import app.models

from app.models.book import Book

from app.constants.book_status import (
    BookStatus
)

from app.services.cover_service import CoverService

from app.services.google_books_service import (
    GoogleBooksService,
)


class BookService:

    # ----------------------------------
    # Get
    # ----------------------------------

    @staticmethod
    def get_all_books():

        session = SessionLocal()

        try:

            return (
                session.query(Book)
                .all()
            )

        finally:

            session.close()

    @staticmethod
    def get_book(
        book_id: int
    ):

        session = SessionLocal()

        try:

            return session.get(
                Book,
                book_id
            )

        finally:

            session.close()

    # ----------------------------------
    # Create
    # ----------------------------------

    @staticmethod
    def create_book(
        title,
        author,
        isbn="",
        publisher="",
        published_year=None,
        genre="",
        description="",
        page_count=None,
        cover_path=None,
        status=BookStatus.WANT_TO_READ,
    ):
    

        session = SessionLocal()

        try:

            book = Book(

                title=title,

                author=author,

                isbn=isbn or None,

                publisher=publisher or None,

                genre=genre or None,

                page_count=page_count if page_count > 0 else None,

                status=status

            )

            session.add(
                book
            )

            session.commit()

            return book

        finally:

            session.close()

    # ----------------------------------
    # Update
    # ----------------------------------

    @staticmethod
    def update_book(

        book_id: int,

        title: str,

        author: str,

        status: str

    ):

        session = SessionLocal()

        try:

            book = session.get(
                Book,
                book_id
            )

            if not book:

                return None

            book.title = title

            book.author = author

            book.status = status

            if status == BookStatus.COMPLETED:

                book.current_page = book.page_count or 0

            elif status == BookStatus.WANT_TO_READ:

                book.current_page = 0

            session.commit()

            return book

        finally:

            session.close()

    @staticmethod
    def update_current_page(

        book_id: int,

        current_page: int

    ):

        session = SessionLocal()

        try:

            book = session.get(
                Book,
                book_id
            )

            if book:

                book.current_page = current_page

                session.commit()

        finally:

            session.close()

    # ----------------------------------
    # Delete
    # ----------------------------------

    @staticmethod
    def delete_book(
        book_id: int
    ):

        session = SessionLocal()

        try:

            book = session.get(
                Book,
                book_id
            )

            if not book:

                return False

            session.delete(
                book
            )

            session.commit()

            return True

        finally:

            session.close()

    # ----------------------------------
    # Reading
    # ----------------------------------
    
    @staticmethod
    def get_current_reading():

        session = SessionLocal()

        try:

            return (

                session.query(Book)

                .filter(

                    Book.status == BookStatus.READING

                )

                .order_by(

                    Book.updated_at.desc()

                )

                .first()

            )

        finally:

            session.close()

    @staticmethod
    def get_status_summary():

        session = SessionLocal()

        try:

            books = session.query(Book).all()

            summary = {

                BookStatus.READING: 0,

                BookStatus.WANT_TO_READ: 0,

                BookStatus.COMPLETED: 0,

                BookStatus.PAUSED: 0,

                BookStatus.DROPPED: 0,

            }

            for book in books:

                if book.status in summary:

                    summary[book.status] += 1

            return summary

        finally:

            session.close()

    @staticmethod
    def get_recent_books(
        limit=5
    ):

        session = SessionLocal()

        try:

            return (

                session.query(Book)

                .order_by(
                    Book.updated_at.desc()
                )

                .limit(limit)

                .all()

            )

        finally:

            session.close()

    @staticmethod
    def get_reading_books():

        session = SessionLocal()

        try:

            return (

                session.query(Book)

                .filter(
                    Book.status == BookStatus.READING
                )

                .order_by(
                    Book.updated_at.desc()
                )

                .all()

            )

        finally:

            session.close()

    @classmethod
    def create_from_google_book(
        cls,
        google_book,
    ):

        author = ""

        if google_book.authors:

            author = ", ".join(
                google_book.authors
            )

        cover_path = None

        if google_book.thumbnail:

            cover_path = CoverService.download(
                google_book.thumbnail
            )

        return cls.create_book(

            title=google_book.title,

            author=author,

            isbn=google_book.isbn,

            publisher=google_book.publisher,

            published_year=google_book.published_year,

            genre=google_book.genre,

            description=google_book.description,

            page_count=google_book.page_count,

            cover_path=cover_path,

        )

    @classmethod
    def refresh_metadata(
        cls,
        book_id: int,
    ):

        session = SessionLocal()

        try:

            book = session.get(
                Book,
                book_id,
            )

            if book is None:

                return None

            results = GoogleBooksService.search(
                book.title
            )

            if not results:

                return book

            google_book = results[0]

            author = ""

            if google_book.authors:

                author = ", ".join(
                    google_book.authors
                )

            cover_path = book.cover_path

            if google_book.thumbnail:

                cover_path = CoverService.download(
                    google_book.thumbnail
                )

            book.title = google_book.title

            book.author = author

            book.isbn = google_book.isbn

            book.publisher = google_book.publisher

            book.published_year = (
                google_book.published_year
            )

            book.genre = google_book.genre

            book.description = (
                google_book.description
            )

            book.page_count = (
                google_book.page_count
            )

            book.cover_path = cover_path

            session.commit()

            return book

        finally:

            session.close()

    @staticmethod
    def find_duplicate(
        google_book,
    ):

        session = SessionLocal()

        try:

            # ------------------------------
            # Check ISBN
            # ------------------------------

            if google_book.isbn:

                book = (
                    session.query(Book)
                    .filter(
                        Book.isbn == google_book.isbn
                    )
                    .first()
                )

                if book:

                    return book

            # ------------------------------
            # Check Title + Author
            # ------------------------------

            author = ", ".join(
                google_book.authors
            )

            return (

                session.query(Book)

                .filter(

                    Book.title == google_book.title,

                    Book.author == author,

                )

                .first()

            )

        finally:

            session.close()