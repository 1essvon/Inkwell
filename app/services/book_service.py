from app.database.session import SessionLocal
from app.models.book import Book


class BookService:

    @staticmethod
    def get_all_books():
        session = SessionLocal()

        try:
            return session.query(Book).all()
        finally:
            session.close()

    @staticmethod
    def create_book(title: str, author: str):
        session = SessionLocal()

        try:
            book = Book(
                title=title,
                author=author
            )

            session.add(book)
            session.commit()

            return book

        finally:
            session.close()

    @staticmethod
    def get_book(book_id: int):
        session = SessionLocal()

        try:
            return session.get(Book, book_id)
        finally:
            session.close()

    @staticmethod
    def update_book(
        book_id: int,
        title: str,
        author: str
    ):
        session = SessionLocal()

        try:
            book = session.get(Book, book_id)

            if not book:
                return None

            book.title = title
            book.author = author

            session.commit()

            return book

        finally:
            session.close()