from PySide6.QtWidgets import (
    QComboBox,
    QDialog,
    QFormLayout,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QTextEdit,
    QVBoxLayout,
)

from app.services.book_service import BookService
from app.services.note_service import NoteService


class AddNoteDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle(
            "Add Note"
        )

        self.resize(
            500,
            420,
        )

        self.setup_ui()

        self.load_books()

    # ======================================
    # UI
    # ======================================

    def setup_ui(self):

        layout = QVBoxLayout(self)

        form = QFormLayout()

        self.book_combo = QComboBox()

        form.addRow(
            "Book",
            self.book_combo,
        )

        self.page_input = QSpinBox()

        self.page_input.setMinimum(
            1
        )

        self.page_input.setMaximum(
            9999
        )

        form.addRow(
            "Page",
            self.page_input,
        )

        self.title_input = QLineEdit()

        form.addRow(
            "Title",
            self.title_input,
        )

        self.content_input = QTextEdit()

        form.addRow(
            "Content",
            self.content_input,
        )

        layout.addLayout(
            form
        )

        self.save_button = QPushButton(
            "Save"
        )

        self.save_button.clicked.connect(
            self.save_note
        )

        layout.addWidget(
            self.save_button
        )

    # ======================================
    # Data
    # ======================================

    def load_books(self):

        self.book_combo.clear()

        books = BookService.get_all_books()

        for book in books:

            self.book_combo.addItem(

                book.title,

                book.id,

            )

    # ======================================
    # Actions
    # ======================================

    def save_note(self):

        if self.book_combo.currentIndex() == -1:

            return

        title = self.title_input.text().strip()

        if not title:

            title = "Untitled"

        NoteService.create_note(

            book_id=self.book_combo.currentData(),

            page=self.page_input.value(),

            title=title,

            content=self.content_input.toPlainText().strip(),

        )

        self.accept()