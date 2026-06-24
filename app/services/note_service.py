from app.database.session import SessionLocal
from app.models.note import Note


class NoteService:

    @staticmethod
    def get_all_notes():

        session = SessionLocal()

        try:
            return session.query(Note).all()
        finally:
            session.close()

    @staticmethod
    def create_note(title: str):

        session = SessionLocal()

        try:
            note = Note(
                title=title
            )

            session.add(note)
            session.commit()

            return note

        finally:
            session.close()

    @staticmethod
    def get_note(note_id: int):

        session = SessionLocal()

        try:
            return session.get(Note, note_id)
        finally:
            session.close()

    @staticmethod
    def update_note(
        note_id: int,
        content: str
    ):

        session = SessionLocal()

        try:
            note = session.get(
                Note,
                note_id
            )

            if not note:
                return None

            note.content = content

            session.commit()

            return note

        finally:
            session.close()
        
    @staticmethod
    def delete_note(note_id: int):

        session = SessionLocal()

        try:
            note = session.get(
                Note,
                note_id
            )

            if note:
                session.delete(note)
                session.commit()

        finally:
            session.close()