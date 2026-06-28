"""
File:
    add_book_dialog.py

Purpose:
    Dialog untuk menambahkan buku baru.

Responsibilities:
    - Mengambil input data buku
    - Memvalidasi input sederhana
    - Memanggil BookService

Does NOT:
    - Mengakses database secara langsung
"""

from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSpinBox,
    QComboBox
)

from app.services.book_service import BookService

from app.constants.book_status import (
    BookStatus
)


class AddBookDialog(QDialog):

    # ----------------------------------
    # Initialization
    # ----------------------------------

    def __init__(self):
        super().__init__()

        self.setup_ui()

    # ----------------------------------
    # UI
    # ----------------------------------

    def setup_ui(self):

        self.setWindowTitle(
            "Add Book"
        )

        layout = QVBoxLayout()

        # Title

        layout.addWidget(
            QLabel("Title")
        )

        self.title_input = QLineEdit()

        layout.addWidget(
            self.title_input
        )

        # Author

        layout.addWidget(
            QLabel("Author")
        )

        self.author_input = QLineEdit()

        layout.addWidget(
            self.author_input
        )

        # ISBN

        layout.addWidget(
            QLabel("ISBN")
        )

        self.isbn_input = QLineEdit()

        layout.addWidget(
            self.isbn_input
        )

        # Publisher

        layout.addWidget(
            QLabel("Publisher")
        )

        self.publisher_input = QLineEdit()

        layout.addWidget(
            self.publisher_input
        )

        # Genre

        layout.addWidget(
            QLabel("Genre")
        )

        self.genre_input = QLineEdit()

        layout.addWidget(
            self.genre_input
        )

        # Page Count

        layout.addWidget(
            QLabel("Page Count")
        )

        self.page_count_input = QSpinBox()

        self.page_count_input.setMaximum(
            100000
        )

        layout.addWidget(
            self.page_count_input
        )

        # Status

        layout.addWidget(
            QLabel("Status")
        )

        self.status_combo = QComboBox()

        self.status_combo.addItems(
            BookStatus.ALL
        )

        self.status_combo.setCurrentText(
            BookStatus.WANT_TO_READ
        )

        layout.addWidget(
            self.status_combo
        )

        # Save Button

        self.save_button = QPushButton(
            "Save"
        )

        self.save_button.clicked.connect(
            self.save_book
        )

        layout.addWidget(
            self.save_button
        )

        self.setLayout(
            layout
        )

    # ----------------------------------
    # Events
    # ----------------------------------

    def save_book(self):

        title = self.title_input.text().strip()

        author = self.author_input.text().strip()

        if not title:

            return

        BookService.create_book(

            title=title,

            author=author,

            isbn=self.isbn_input.text().strip(),

            publisher=self.publisher_input.text().strip(),

            genre=self.genre_input.text().strip(),

            page_count=self.page_count_input.value(),

            status=self.status_combo.currentText()

        )

        self.accept()