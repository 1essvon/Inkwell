from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QListWidget,
    QLabel,
    QComboBox
)
from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtWidgets import QHBoxLayout

from app.services.note_service import NoteService
from app.ui.dialogs.add_note_dialog import AddNoteDialog
from app.ui.journal.note_detail_view import (
    NoteDetailView
)
from app.services.book_service import (
    BookService
)


class NotesView(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(
            QLabel("Book")
        )

        self.book_filter = QComboBox()

        layout.addWidget(
            self.book_filter
        )

        self.add_note_button = QPushButton(
            "Add Note"
        )

        self.delete_note_button = QPushButton(
            "Delete Note"
        )

        self.add_note_button.clicked.connect(
            self.open_add_note_dialog
        )

        self.delete_note_button.clicked.connect(
            self.delete_selected_note
        )

        self.note_list = QListWidget()

        self.note_list.itemClicked.connect(
            self.show_note_details
        )

        self.detail_view = NoteDetailView()

        button_layout = QHBoxLayout()

        button_layout.addWidget(
            self.add_note_button
        )

        button_layout.addWidget(
            self.delete_note_button
        )

        layout.addLayout(
            button_layout
        )

        content_layout = QHBoxLayout()

        content_layout.addWidget(
            self.note_list,
            1
        )

        content_layout.addWidget(
            self.detail_view,
            3
        )

        layout.addLayout(
            content_layout
        )

        self.load_books()

        self.book_filter.currentIndexChanged.connect(
            self.load_notes
        )

        self.load_notes()

        self.setLayout(layout)

        self.selected_note = None

    def load_books(self):

        self.book_filter.clear()

        self.book_filter.addItem(
            "All Books",
            None
        )

        books = BookService.get_all_books()

        for book in books:

            self.book_filter.addItem(

                book.title,

                book.id

            )

    def load_notes(self):

        self.note_list.clear()

        book_id = self.book_filter.currentData()

        if book_id is None:

            notes = NoteService.get_all_notes()

        else:

            notes = NoteService.get_notes_for_book(
                book_id
            )

        for note in notes:

            item = QListWidgetItem(
                note.title
            )

            item.setData(
                1,
                note.id
            )

            self.note_list.addItem(
                item
            )

        if notes:

            first_note = notes[0]

            self.selected_note = first_note

            self.detail_view.display_note(
                first_note
            )


    def open_add_note_dialog(self):

        book_id = self.book_filter.currentData()

        if book_id is None:

            return

        dialog = AddNoteDialog(
            book_id
        )

        if dialog.exec():
            self.load_notes()

    def show_note_details(self, item):

        note_id = item.data(1)

        note = NoteService.get_note(
            note_id
        )

        if note:
            self.selected_note = note

            self.detail_view.display_note(
                note
            )

    def delete_selected_note(self):

        if not self.selected_note:
            return

        NoteService.delete_note(
            self.selected_note.id
        )

        self.selected_note = None

        self.load_notes()

        self.detail_view.clear()