from PySide6.QtWidgets import (
    QWidget,
    QGridLayout
)

from app.services.statistics_service import (
    StatisticsService
)

from app.ui.components.stat_card import (
    StatCard
)


class StatisticsGrid(QWidget):

    COLUMNS = 3

    # ----------------------------------
    # Initialization
    # ----------------------------------

    def __init__(self):
        super().__init__()

        self.setup_ui()

        self.refresh()

    # ----------------------------------
    # UI
    # ----------------------------------

    def setup_ui(self):

        self.layout = QGridLayout()

        self.layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self.layout.setColumnStretch(
            0,
            1,
        )

        self.layout.setColumnStretch(
            1,
            1,
        )

        self.layout.setColumnStretch(
            2,
            1,
        )

        self.layout.setRowStretch(0, 1)
        self.layout.setRowStretch(1, 1)

        self.layout.setHorizontalSpacing(20)

        self.layout.setVerticalSpacing(20)

        self.setLayout(
            self.layout
        )

    # ----------------------------------
    # Data
    # ----------------------------------

    def refresh(self):

        while self.layout.count():

            item = self.layout.takeAt(0)

            if item.widget():

                item.widget().deleteLater()

        stats = StatisticsService.get_statistics()

        cards = [
            ("📚", "Books", stats["books"]),
            ("📝", "Notes", stats["notes"]),
            ("💬", "Quotes", stats["quotes"]),
            ("⏱", "Sessions", stats["reading_sessions"]),
            ("📄", "Pages", stats["pages_read"]),
            ("⌛", "Minutes", stats["reading_minutes"]),
        ]

        for index, (icon, title, value) in enumerate(cards):

            row = index // self.COLUMNS

            col = index % self.COLUMNS

            self.layout.addWidget(

                StatCard(
                    title=title,
                    value=str(value),
                    icon=icon,
                ),

                row,

                col
            )