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