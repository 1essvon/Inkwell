from app.database.session import SessionLocal
from app.models.note import Note
from app.models.book import Book
from datetime import datetime
from sqlalchemy.orm import joinedload


class NoteService:

    @staticmethod
    def get_all_notes():

        session = SessionLocal()

        try:
            return (

                session.query(Note)

                .options(

                    joinedload(
                        Note.book
                    )

                )

                .order_by(
                    Note.updated_at.desc()
                )

                .all()

            )
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

                .options(

                    joinedload(
                        Note.book
                    )

                )

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

        page: int,

        title: str,

        content: str = "",

    ):

        session = SessionLocal()

        try:

            note = Note(

                book_id=book_id,

                page=page,

                title=title,

                content=content,

            )

            session.add(
                note
            )

            session.commit()

            session.refresh(
                note
            )

            return note

        finally:

            session.close()

    @staticmethod
    def create_quick_note(

        book_id: int,

        content: str,

        current_page: int,

    ):

        title = (
            f"Reading • Page {current_page}"
        )

        return NoteService.create_note(

            book_id=book_id,

            page=current_page,

            title=title,

            content=content,

        )

    @staticmethod
    def get_note(
        note_id: int,
    ):

        session = SessionLocal()

        try:

            return (

                session.query(Note)

                .options(

                    joinedload(
                        Note.book
                    )

                )

                .filter(
                    Note.id == note_id
                )

                .first()

            )

        finally:

            session.close()

    @staticmethod
    def update_note(

        note_id: int,

        title: str,

        content: str,

    ):

        session = SessionLocal()

        try:

            note = session.get(
                Note,
                note_id,
            )

            if note is None:

                return None

            note.title = title

            note.content = content

            session.commit()

            session.refresh(
                note
            )

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