"""
File:
    edit_book_dialog.py

Purpose:
    Dialog untuk mengubah data buku.

Responsibilities:
    - Menampilkan data buku yang dipilih
    - Mengubah data buku
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
    QComboBox
)

from app.services.book_service import BookService

from app.constants.book_status import (
    BookStatus
)


class EditBookDialog(QDialog):

    # ----------------------------------
    # Initialization
    # ----------------------------------

    def __init__(self, book):
        super().__init__()

        self.book = book

        self.setup_ui()

    # ----------------------------------
    # UI
    # ----------------------------------

    def setup_ui(self):

        self.setWindowTitle(
            "Edit Book"
        )

        layout = QVBoxLayout()

        # -------------------------
        # Title
        # -------------------------

        layout.addWidget(
            QLabel("Title")
        )

        self.title_input = QLineEdit(
            self.book.title
        )

        layout.addWidget(
            self.title_input
        )

        # -------------------------
        # Author
        # -------------------------

        layout.addWidget(
            QLabel("Author")
        )

        self.author_input = QLineEdit(
            self.book.author
        )

        layout.addWidget(
            self.author_input
        )

        # -------------------------
        # Status
        # -------------------------

        layout.addWidget(
            QLabel("Status")
        )

        self.status_combo = QComboBox()

        self.status_combo.addItems(
            BookStatus.ALL
        )

        self.status_combo.setCurrentText(
            self.book.status
        )

        layout.addWidget(
            self.status_combo
        )

        # -------------------------
        # Save Button
        # -------------------------

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

        BookService.update_book(

            book_id=self.book.id,

            title=self.title_input.text().strip(),

            author=self.author_input.text().strip(),

            status=self.status_combo.currentText()

        )

        self.accept()