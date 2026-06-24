from app.database.session import SessionLocal
from app.models.quote import Quote


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
    def create_quote(
        quote_text: str,
        source: str = "",
        page_number: int | None = None
    ):

        session = SessionLocal()

        try:

            quote = Quote(
                quote_text=quote_text,
                source=source or None,
                page_number=page_number
            )

            session.add(
                quote
            )

            session.commit()

            return quote

        finally:
            session.close()