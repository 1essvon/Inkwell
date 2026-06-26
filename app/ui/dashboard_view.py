from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QProgressBar,
    QGridLayout
)

from app.ui.components.stat_card import (
    StatCard
)

from app.ui.components.info_card import (
    InfoCard
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

        self.title.setObjectName(
            "pageTitle"
        )

        layout.addWidget(self.title)

        self.current_card = InfoCard()

        layout.addWidget(
            self.current_card
        )

        self.progress = QProgressBar()

        layout.addWidget(
            self.progress
        )

        layout.addWidget(
            self.current_card
        )

        layout.addWidget(
            self.progress
        )

        self.stats_layout = QGridLayout()

        layout.addLayout(
            self.stats_layout
        )

        layout.addStretch()

        self.setLayout(layout)

        self.refresh()

    def refresh(self):

        book = BookService.get_current_reading()

        if book:

            percent = int(
                (book.current_page / book.page_count) * 100
            )

            self.current_card.set_data(

                "Continue Reading",

                book.author,

                f"{book.title}\n\nPage {book.current_page} / {book.page_count}"

            )

            self.progress.setValue(
                percent
            )

        else:

            self.current_card.set_data(

                "Continue Reading",

                "",

                "No active reading."

            )

            self.progress.setValue(0)

        stats = StatisticsService.get_statistics()

        while self.stats_layout.count():

            item = self.stats_layout.takeAt(0)

            if item.widget():

                item.widget().deleteLater()

        cards = [

            ("Books", stats["books"]),

            ("Notes", stats["notes"]),

            ("Quotes", stats["quotes"]),

            ("Sessions", stats["reading_sessions"]),

            ("Pages", stats["pages_read"]),

            ("Minutes", stats["reading_minutes"])

        ]

        for index, (title, value) in enumerate(cards):

            row = index // 3

            col = index % 3

            self.stats_layout.addWidget(

                StatCard(
                    title,
                    str(value)
                ),

                row,

                col
            )