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

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(
            8,
        )

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

        if self.GOAL > 0:

            percent = int(
                completed / self.GOAL * 100
            )

        else:

            percent = 0

        percent = max(
            0,
            min(
                percent,
                100,
            ),
        )

        if completed >= self.GOAL:

            status = "🎉 Goal achieved!"

        else:

            remaining = self.GOAL - completed

            status = f"{remaining} books to go"

        self.progress_text.setText(

            f"{completed} / {self.GOAL} books\n{status}"

        )

        self.progress.setValue(
            percent
        )