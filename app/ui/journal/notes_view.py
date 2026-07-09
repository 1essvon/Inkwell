from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QListWidget,
    QLabel,
    QComboBox,
    QScrollArea,
    QListWidgetItem,
    QHBoxLayout
)

from app.services.note_service import NoteService
from app.ui.dialogs.add_note_dialog import AddNoteDialog
from app.ui.journal.note_detail_view import (
    NoteDetailView
)
from app.services.book_service import (
    BookService
)

from app.ui.components.page_header import (
    PageHeader,
)

from app.ui.components.toolbar import (
    Toolbar,
)

from app.ui.components.empty_state import (
    EmptyState,
)


class NotesView(QWidget):

    def __init__(self):
        super().__init__()

        root_layout = QVBoxLayout()

        scroll = QScrollArea()

        scroll.setWidgetResizable(True)

        content = QWidget()

        layout = QVBoxLayout()

        layout.addWidget(

            PageHeader(

                "Notes"

            )

        )

        content.setLayout(layout)

        scroll.setWidget(content)

        root_layout.addWidget(scroll)

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

        self.empty_state = EmptyState(

            icon="📝",

            title="No Notes Yet",

            subtitle=(
                "Create your first note\n"
                "to keep track of your ideas."
            )

        )

        self.empty_state.hide()

        self.note_list.itemClicked.connect(
            self.show_note_details
        )

        self.detail_view = NoteDetailView()

        toolbar = Toolbar()

        toolbar.add_stretch()

        toolbar.add_widget(
            self.add_note_button
        )

        toolbar.add_widget(
            self.delete_note_button
        )

        layout.addWidget(
            toolbar
        )

        content_layout = QHBoxLayout()

        content_layout.addWidget(
            self.note_list,
            1
        )

        content_layout.addWidget(
            self.empty_state,
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

        self.setLayout(root_layout)

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
            
        else:

            self.selected_note = None

            self.detail_view.clear()

        self.update_empty_state()


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

    def update_empty_state(self):

        has_notes = (
            self.note_list.count() > 0
        )

        self.note_list.setVisible(
            has_notes
        )

        self.detail_view.setVisible(
            has_notes
        )

        self.empty_state.setVisible(
            not has_notes
        )