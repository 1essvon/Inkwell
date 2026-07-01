from app.database.session import SessionLocal
from app.models.quote import Quote
from app.models.book import Book

class QuoteService:

    @staticmethod
    def get_all_quotes():

        session = SessionLocal()

        try:
            return session.query(
                Quote
            ).all()

        finally:
            session.close()

    @staticmethod
    def get_quotes_for_book(

        book_id: int

    ):

        session = SessionLocal()

        try:

            return (

                session.query(Quote)

                .filter(
                    Quote.book_id == book_id
                )

                .order_by(
                    Quote.created_at.desc()
                )

                .all()

            )

        finally:

            session.close()

    @staticmethod
    def get_quote(
        quote_id: int
    ):

        session = SessionLocal()

        try:
            return session.get(
                Quote,
                quote_id
            )

        finally:
            session.close()

    @staticmethod
    def create_quote(
        book_id: int,
        content: str,
        page: int
    ):

        session = SessionLocal()

        try:
            quote = Quote(

            book_id=book_id,

            content=content,

            page=page

        )

            session.add(
                quote
            )

            session.commit()

            return quote

        finally:
            session.close()

    @staticmethod
    def create_quick_quote(

        book_id: int,

        content: str,

        page: int

    ):

        return QuoteService.create_quote(

            book_id=book_id,

            content=content,

            page=page

        )

    @staticmethod
    def delete_quote(
        quote_id: int
    ):

        session = SessionLocal()

        try:

            quote = session.get(
                Quote,
                quote_id
            )

            if quote:

                session.delete(
                    quote
                )

                session.commit()

        finally:
            session.close()

    

    