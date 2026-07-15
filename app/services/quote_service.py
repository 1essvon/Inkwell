from app.database.session import SessionLocal
from app.models.quote import Quote
from app.models.book import Book
from sqlalchemy.orm import joinedload

class QuoteService:

    @staticmethod
    def get_all_quotes():

        session = SessionLocal()

        try:
            return (

                session.query(Quote)

                .options(

                    joinedload(
                        Quote.book
                    )

                )

                .order_by(
                    Quote.updated_at.desc()
                )

                .all()

            )

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

                .options(

                    joinedload(
                        Quote.book
                    )

                )

                .filter(
                    Quote.book_id == book_id
                )

                .order_by(
                    Quote.updated_at.desc()
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
            return (

                session.query(Quote)

                .options(

                    joinedload(
                        Quote.book
                    )

                )

                .filter(
                    Quote.id == quote_id
                )

                .first()

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

                page=page,

                note="",

                tags="",

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

    @staticmethod
    def update_quote(

        quote_id: int,

        note: str,

        tags: str,

    ):

        session = SessionLocal()

        try:

            quote = session.get(
                Quote,
                quote_id,
            )

            if quote is None:

                return None

            quote.note = note

            quote.tags = tags

            session.commit()

            session.refresh(
                quote
            )

            return quote

        finally:

            session.close()