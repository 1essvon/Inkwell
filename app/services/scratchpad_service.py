from sqlalchemy import desc

from app.database.session import (
    SessionLocal,
)

from app.models.scratchpad_entry import (
    ScratchpadEntry,
)

class ScratchpadService:

    @staticmethod
    def get_all_entries():

        session = SessionLocal()

        try:

            return (

                session.query(
                    ScratchpadEntry
                )

                .order_by(

                    desc(
                        ScratchpadEntry.updated_at
                    )

                )

                .all()

            )

        finally:

            session.close()

    @staticmethod
    def get_entry(
        entry_id,
    ):

        session = SessionLocal()

        try:

            return session.get(
                ScratchpadEntry,
                entry_id,
            )

        finally:

            session.close()

    @staticmethod
    def create_entry(

        title="Untitled",

        content="",

    ):

        session = SessionLocal()

        try:

            entry = ScratchpadEntry(

                title=title,

                content=content,

            )

            session.add(
                entry
            )

            session.commit()

            session.refresh(
                entry
            )

            return entry

        finally:

            session.close()

    @staticmethod
    def update_entry(

        entry_id,

        title,

        content,

    ):

        session = SessionLocal()

        try:

            entry = session.get(

                ScratchpadEntry,

                entry_id,

            )

            if entry is None:

                return None

            entry.title = title

            entry.content = content

            session.commit()

            session.refresh(
                entry
            )

            return entry

        finally:

            session.close()

    @staticmethod
    def delete_entry(
        entry_id,
    ):

        session = SessionLocal()

        try:

            entry = session.get(

                ScratchpadEntry,

                entry_id,

            )

            if entry:

                session.delete(
                    entry
                )

                session.commit()

        finally:

            session.close()