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