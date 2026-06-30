"""
File:
    library_summary_card.py

Purpose:
    Menampilkan ringkasan jumlah buku berdasarkan status.

Responsibilities:
    - Menampilkan jumlah buku per status
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

from app.constants.book_status import (
    BookStatus
)

class LibrarySummaryCard(QWidget):

    def __init__(self):
        super().__init__()

        self.setup_ui()

        self.refresh()

    def setup_ui(self):

        layout = QVBoxLayout()

        self.title = QLabel(
            "Library Summary"
        )

        self.reading = QLabel()

        self.want_to_read = QLabel()

        self.completed = QLabel()

        self.paused = QLabel()

        self.dropped = QLabel()

        layout.addWidget(self.title)

        layout.addWidget(self.reading)

        layout.addWidget(self.want_to_read)

        layout.addWidget(self.completed)

        layout.addWidget(self.paused)

        layout.addWidget(self.dropped)

        self.setLayout(layout)

    def refresh(self):

        summary = BookService.get_status_summary()

        self.reading.setText(
            f"📖 Reading : {summary[BookStatus.READING]}"
        )

        self.want_to_read.setText(
            f"📚 Want To Read : {summary[BookStatus.WANT_TO_READ]}"
        )

        self.completed.setText(
            f"✅ Completed : {summary[BookStatus.COMPLETED]}"
        )

        self.paused.setText(
            f"⏸ Paused : {summary[BookStatus.PAUSED]}"
        )

        self.dropped.setText(
            f"❌ Dropped : {summary[BookStatus.DROPPED]}"
        )