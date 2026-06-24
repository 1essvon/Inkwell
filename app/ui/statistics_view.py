from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel
)

from app.services.statistics_service import (
    StatisticsService
)


class StatisticsView(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        stats = (
            StatisticsService
            .get_statistics()
        )

        self.books_label = QLabel(
            f"Books: {stats['books']}"
        )

        self.notes_label = QLabel(
            f"Notes: {stats['notes']}"
        )

        self.quotes_label = QLabel(
            f"Quotes: {stats['quotes']}"
        )

        self.sessions_label = QLabel(
            f"Reading Sessions: {stats['reading_sessions']}"
        )

        self.pages_label = QLabel(
            f"Pages Read: {stats['pages_read']}"
        )

        self.minutes_label = QLabel(
            f"Reading Time: {stats['reading_minutes']} min"
        )

        layout.addWidget(
            self.books_label
        )

        layout.addWidget(
            self.notes_label
        )

        layout.addWidget(
            self.quotes_label
        )

        layout.addWidget(
            self.sessions_label
        )

        layout.addWidget(
            self.pages_label
        )

        layout.addWidget(
            self.minutes_label
        )

        layout.addStretch()

        self.setLayout(layout)