from app.database.session import SessionLocal
from app.models.note import Note
from app.models.book import Book
from datetime import datetime


class NoteService:

    @staticmethod
    def get_all_notes():

        session = SessionLocal()

        try:
            return session.query(Note).all()
        finally:
            session.close()

    @staticmethod
    def get_notes_for_book(

        book_id: int

    ):

        session = SessionLocal()

        try:

            return (

                session.query(Note)

                .filter(
                    Note.book_id == book_id
                )

                .order_by(
                    Note.updated_at.desc()
                )

                .all()

            )

        finally:

            session.close()

    @staticmethod
    def create_note(
        book_id: int,
        title: str,
        content: str = ""
    ):
        session = SessionLocal()

        try:
            note = Note(
            book_id=book_id,
            title=title,
            content=content
        )

            session.add(note)
            session.commit()

            return note

        finally:
            session.close()

    @staticmethod
    def create_quick_note(

        book_id: int,

        content: str,

        current_page: int

    ):

        title = (
            f"Reading • Page {current_page}"
        )

        return NoteService.create_note(

            book_id=book_id,

            title=title,

            content=content

        )

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