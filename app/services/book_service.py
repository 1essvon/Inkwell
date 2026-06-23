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