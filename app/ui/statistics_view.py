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

        self.books_label = QLabel()
        self.notes_label = QLabel()
        self.quotes_label = QLabel()
        self.sessions_label = QLabel()
        self.pages_label = QLabel()
        self.minutes_label = QLabel()

        layout.addWidget(self.books_label)
        layout.addWidget(self.notes_label)
        layout.addWidget(self.quotes_label)

        layout.addSpacing(12)

        layout.addWidget(self.sessions_label)
        layout.addWidget(self.pages_label)
        layout.addWidget(self.minutes_label)

        layout.addStretch()

        self.setLayout(layout)

        self.refresh()

    def refresh(self):

        stats = StatisticsService.get_statistics()

        self.books_label.setText(
            f"Books: {stats['books']}"
        )

        self.notes_label.setText(
            f"Notes: {stats['notes']}"
        )

        self.quotes_label.setText(
            f"Quotes: {stats['quotes']}"
        )

        self.sessions_label.setText(
            f"Reading Sessions: {stats['reading_sessions']}"
        )

        self.pages_label.setText(
            f"Pages Read: {stats['pages_read']}"
        )

        self.minutes_label.setText(
            f"Reading Time: {stats['reading_minutes']} min"
        )