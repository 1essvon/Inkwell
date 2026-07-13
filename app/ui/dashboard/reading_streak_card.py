from PySide6.QtWidgets import (
    QLabel,
)

from app.services.statistics_service import (
    StatisticsService,
)

from app.ui.components.base_card import (
    BaseCard,
)

class ReadingStreakCard(BaseCard):

    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.refresh()

    def setup_ui(self):

        self.title = QLabel(
            "Reading Streak"
        )

        self.title.setObjectName(
            "cardTitle"
        )

        self.layout.addWidget(
            self.title
        )

        self.current_title = QLabel(
            "Current"
        )

        self.current_title.setObjectName(
            "secondaryText"
        )

        self.layout.addWidget(
            self.current_title
        )

        self.current_value = QLabel()

        self.current_value.setObjectName(
            "bookTitle"
        )

        self.layout.addWidget(
            self.current_value
        )

        self.best_title = QLabel(
            "Best"
        )

        self.best_title.setObjectName(
            "secondaryText"
        )

        self.layout.addWidget(
            self.best_title
        )

        self.best_value = QLabel()

        self.best_value.setObjectName(
            "bookTitle"
        )

        self.layout.addWidget(
            self.best_value
        )

        self.last_title = QLabel(
            "Last Read"
        )

        self.last_title.setObjectName(
            "secondaryText"
        )

        self.layout.addWidget(
            self.last_title
        )

        self.last_value = QLabel()

        self.last_value.setObjectName(
            "bookTitle"
        )

        self.layout.addWidget(
            self.last_value
        )

        self.layout.addStretch()

    def refresh(self):

        stats = StatisticsService.get_statistics()

        current = stats[
            "reading_streak"
        ]

        best = stats[
            "best_streak"
        ]

        last_read = stats[
            "last_read"
        ]

        if last_read:

            last_text = last_read.strftime(
                "%d %b %Y"
            )

        else:

            last_text = "Never"

        self.current_value.setText(
            f"{current} day(s)"
        )

        self.best_value.setText(
            f"{best} day(s)"
        )

        self.last_value.setText(
            last_text
        )