from PySide6.QtWidgets import (
    QGridLayout,
    QWidget,
)

from app.ui.components.metric_card import (
    MetricCard,
)


class StatisticsGrid(QWidget):

    COLUMNS = 3

    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.set_data(
            {
                "books": 0,
                "notes": 0,
                "quotes": 0,
                "sessions": 0,
                "pages_read": 0,
                "reading_minutes": 0,
            }
        )

    # ==================================================
    # UI
    # ==================================================

    def setup_ui(self):

        self.grid_layout = QGridLayout()

        self.grid_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self.grid_layout.setHorizontalSpacing(
            20,
        )

        self.grid_layout.setVerticalSpacing(
            20,
        )

        for column in range(
            self.COLUMNS
        ):

            self.grid_layout.setColumnStretch(
                column,
                1,
            )

        for row in range(2):

            self.grid_layout.setRowStretch(
                row,
                1,
            )

        self.setLayout(
            self.grid_layout
        )

        self.books_card = MetricCard(
            title="Books",
            value="0",
            subtitle="In Library",
        )

        self.notes_card = MetricCard(
            title="Notes",
            value="0",
            subtitle="Saved",
        )

        self.quotes_card = MetricCard(
            title="Quotes",
            value="0",
            subtitle="Collected",
        )

        self.sessions_card = MetricCard(
            title="Sessions",
            value="0",
            subtitle="Completed",
        )

        self.pages_card = MetricCard(
            title="Pages",
            value="0",
            subtitle="Read",
        )

        self.minutes_card = MetricCard(
            title="Minutes",
            value="0",
            subtitle="Reading Time",
        )

        cards = [

            self.books_card,

            self.notes_card,

            self.quotes_card,

            self.sessions_card,

            self.pages_card,

            self.minutes_card,

        ]

        for index, card in enumerate(cards):

            row = index // self.COLUMNS

            column = index % self.COLUMNS

            self.grid_layout.addWidget(
                card,
                row,
                column,
            )

    # ==================================================
    # Public API
    # ==================================================

    def set_data(
        self,
        summary: dict,
    ):

        self.books_card.set_value(
            summary.get(
                "books",
                0,
            )
        )

        self.notes_card.set_value(
            summary.get(
                "notes",
                0,
            )
        )

        self.quotes_card.set_value(
            summary.get(
                "quotes",
                0,
            )
        )

        self.sessions_card.set_value(
            summary.get(
                "sessions",
                0,
            )
        )

        self.pages_card.set_value(
            summary.get(
                "pages_read",
                0,
            )
        )

        self.minutes_card.set_value(
            summary.get(
                "reading_minutes",
                0,
            )
        )