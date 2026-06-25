from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel
)

from app.services.statistics_service import (
    StatisticsService
)
from app.services.book_service import (
    BookService
)


class DashboardView(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.title = QLabel("Dashboard")

        self.title.setStyleSheet("""
            font-size:24px;
            font-weight:bold;
        """)

        layout.addWidget(self.title)

        self.current_book = QLabel()

        layout.addWidget(
            self.current_book
        )

        self.stats = QLabel()

        layout.addWidget(self.stats)

        layout.addStretch()

        self.setLayout(layout)

        self.refresh()

    def refresh(self):

        book = BookService.get_current_reading()

        if book:

            self.current_book.setText(
                f"""
        Continue Reading

        📚 {book.title}

        Page {book.current_page} / {book.page_count}
        """
            )

        else:

            self.current_book.setText(
                "No active reading."
            )

        stats = StatisticsService.get_statistics()

        self.stats.setText(
            f"""
            Books : {stats['books']}

            Notes : {stats['notes']}

            Quotes : {stats['quotes']}

            Reading Sessions : {stats['reading_sessions']}

            Pages Read : {stats['pages_read']}

            Reading Time : {stats['reading_minutes']} min
            """
                    )