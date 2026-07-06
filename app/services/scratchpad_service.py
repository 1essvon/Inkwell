from app.database.session import (
    SessionLocal
)

from app.models.scratchpad_entry import (
    ScratchpadEntry
)


class ScratchpadService:

    @staticmethod
    def get():

        session = SessionLocal()

        try:

            scratchpad = (

                session.query(
                    ScratchpadEntry
                ).first()

            )

            if scratchpad is None:

                scratchpad = ScratchpadEntry(

                    content=""

                )

                session.add(
                    scratchpad
                )

                session.commit()

                session.refresh(
                    scratchpad
                )

            return scratchpad

        finally:

            session.close()

    @staticmethod
    def save(content: str):

        session = SessionLocal()

        try:

            scratchpad = (

                session.query(
                    ScratchpadEntry
                ).first()

            )

            if scratchpad is None:

                scratchpad = ScratchpadEntry(

                    content=content

                )

                session.add(
                    scratchpad
                )

            else:

                scratchpad.content = content

            session.commit()

        finally:

            session.close()

    @staticmethod
    def clear():

        ScratchpadService.save("")