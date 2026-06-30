"""
File:
    reading_book_card.py

Purpose:
    Mini card untuk daftar buku yang sedang dibaca.

Responsibilities:
    - Menampilkan judul
    - Menampilkan progress halaman
    - Menampilkan status

Does NOT:
    - Mengakses database
"""

from PySide6.QtWidgets import (
    QLabel
)

from app.models.book import Book

from app.ui.components.base_card import (
    BaseCard
)

class ReadingBookCard(BaseCard):

    def __init__(
        self,
        book: Book
    ):
        super().__init__()

        self.book = book

        self.setup_ui()

    def setup_ui(self):

        title = QLabel(
            f"📖 {self.book.title}"
        )

        title.setObjectName(
            "bookTitle"
        )

        current = self.book.current_page or 0

        total = self.book.page_count or 0

        progress = QLabel(
            f"{current} / {total}"
        )

        progress.setObjectName(
            "bookProgress"
        )

        status = QLabel(
            self.book.status
        )

        status.setObjectName(
            "summaryItem"
        )

        self.layout.addWidget(
            title
        )

        self.layout.addWidget(
            progress
        )

        self.layout.addWidget(
            status
        )

    