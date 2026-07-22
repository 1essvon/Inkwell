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
from app.services.quote_service import QuoteService


class AddQuoteDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setWindowTitle(
            "Add Quote"
        )

        self.resize(
            550,
            500,
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

        self.quote_input = QTextEdit()

        self.quote_input.setPlaceholderText(
            "Enter quote..."
        )

        form.addRow(
            "Quote",
            self.quote_input,
        )

        self.note_input = QTextEdit()

        self.note_input.setPlaceholderText(
            "Personal reflection..."
        )

        form.addRow(
            "Reflection",
            self.note_input,
        )

        self.tags_input = QLineEdit()

        self.tags_input.setPlaceholderText(
            "productivity, habits, mindset"
        )

        form.addRow(
            "Tags",
            self.tags_input,
        )

        layout.addLayout(
            form
        )

        self.save_button = QPushButton(
            "Save"
        )

        self.save_button.clicked.connect(
            self.save_quote
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

    def save_quote(self):

        if self.book_combo.currentIndex() == -1:

            return

        content = (

            self.quote_input

            .toPlainText()

            .strip()

        )

        if not content:

            return

        quote = QuoteService.create_quote(

            book_id=self.book_combo.currentData(),

            page=self.page_input.value(),

            content=content,

        )

        QuoteService.update_quote(

            quote_id=quote.id,

            note=self.note_input.toPlainText().strip(),

            tags=self.tags_input.text().strip(),

        )

        self.accept()