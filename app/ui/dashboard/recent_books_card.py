"""
File:
    recent_books_card.py

Purpose:
    Menampilkan daftar buku terbaru.

Responsibilities:
    - Menampilkan maksimal 5 buku
    - Mengambil data dari BookService

Does NOT:
    - Mengakses database secara langsung
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel
)

from app.services.book_service import BookService

class RecentBooksCard(QWidget):

    # ----------------------------------
    # Initialization
    # ----------------------------------

    def __init__(self):
        super().__init__()

        self.setup_ui()

        self.refresh()

    def setup_ui(self):

        layout = QVBoxLayout()

        self.title = QLabel(
            "Recent Books"
        )

        self.title.setObjectName(
            "cardTitle"
        )

        layout.addWidget(
            self.title
        )

        self.items = []

        for _ in range(5):

            label = QLabel()

            label.setObjectName(
                "summaryItem"
            )

            self.items.append(
                label
            )

            layout.addWidget(
                label
            )

        layout.addStretch()

        self.setLayout(
            layout
        )

    def refresh(self):

        books = BookService.get_recent_books()

        for label in self.items:

            label.clear()

        for label, book in zip(self.items, books):

            label.setText(
                f"📖 {book.title}"
            )