from app.database.session import SessionLocal
from app.models.scratchpad_entry import (
    ScratchpadEntry
)


class ScratchpadService:

    @staticmethod
    def get_entry():

        session = SessionLocal()

        try:

            entry = (
                session.query(
                    ScratchpadEntry
                )
                .first()
            )

            return entry

        finally:
            session.close()

    @staticmethod
    def save_content(
        content: str
    ):

        session = SessionLocal()

        try:

            entry = (
                session.query(
                    ScratchpadEntry
                )
                .first()
            )

            if not entry:

                entry = ScratchpadEntry(
                    content=content
                )

                session.add(
                    entry
                )

            else:

                entry.content = content

            session.commit()

        finally:
            session.close()