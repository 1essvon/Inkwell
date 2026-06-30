"""
File:
    reading_goal_card.py

Purpose:
    Menampilkan progres target membaca.

Responsibilities:
    - Menampilkan jumlah buku selesai
    - Menghitung progress

Does NOT:
    - Menyimpan target pengguna
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QProgressBar
)

from app.services.book_service import BookService
from app.constants.book_status import BookStatus

class ReadingGoalCard(QWidget):

    GOAL = 20

    def __init__(self):
        super().__init__()

        self.setup_ui()

        self.refresh()

    def setup_ui(self):

        layout = QVBoxLayout()

        self.title = QLabel(
            "Reading Goal"
        )

        self.title.setObjectName(
            "cardTitle"
        )

        self.progress_text = QLabel()

        self.progress = QProgressBar()

        layout.addWidget(
            self.title
        )

        layout.addWidget(
            self.progress_text
        )

        layout.addWidget(
            self.progress
        )

        self.setLayout(
            layout
        )

    def refresh(self):

        summary = BookService.get_status_summary()

        completed = summary[
            BookStatus.COMPLETED
        ]

        percent = int(
            completed / self.GOAL * 100
        )

        if percent > 100:

            percent = 100

        self.progress_text.setText(

            f"{completed} / {self.GOAL} books"

        )

        self.progress.setValue(
            percent
        )