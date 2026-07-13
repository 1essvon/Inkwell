from PySide6.QtWidgets import (
    QGridLayout,
    QWidget,
)

from app.services.statistics_service import (
    StatisticsService,
)

from app.ui.components.metric_card import (
    MetricCard,
)

class StatisticsGrid(QWidget):

    COLUMNS = 3

    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.refresh()

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

        for column in range(self.COLUMNS):

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

    def refresh(self):

        while self.grid_layout.count():

            item = self.grid_layout.takeAt(0)

            if item.widget():

                item.widget().deleteLater()

        stats = StatisticsService.get_statistics()

        metrics = [

            (
                "Books",
                stats["books"],
                "In Library",
            ),

            (
                "Notes",
                stats["notes"],
                "Saved",
            ),

            (
                "Quotes",
                stats["quotes"],
                "Collected",
            ),

            (
                "Sessions",
                stats["reading_sessions"],
                "Completed",
            ),

            (
                "Pages",
                stats["pages_read"],
                "Read",
            ),

            (
                "Minutes",
                stats["reading_minutes"],
                "Reading Time",
            ),

        ]

        for index, (

            title,

            value,

            subtitle,

        ) in enumerate(metrics):

            row = index // self.COLUMNS

            column = index % self.COLUMNS

            self.grid_layout.addWidget(

                MetricCard(

                    title=title,

                    value=str(value),

                    subtitle=subtitle,

                ),

                row,

                column,

            )