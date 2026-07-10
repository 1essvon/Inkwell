from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
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
            "🔥 Reading Streak"
        )

        self.title.setObjectName(
            "cardTitle"
        )

        self.current_label = QLabel()

        self.best_label = QLabel()

        self.last_read_label = QLabel()

        self.layout.addWidget(
            self.title
        )

        self.layout.addWidget(
            self.current_label
        )

        self.layout.addWidget(
            self.best_label
        )

        self.layout.addWidget(
            self.last_read_label
        )

        self.layout.addStretch()

    def refresh(self):

        stats = StatisticsService.get_statistics()

        current = stats["reading_streak"]

        best = stats["best_streak"]

        last_read = stats["last_read"]

        if last_read is None:

            last_text = "Never"

        else:

            last_text = last_read.strftime(
                "%d %b %Y"
            )

        self.current_label.setText(

            f"Current : {current} day(s)"

        )

        self.best_label.setText(

            f"Best : {best} day(s)"

        )

        self.last_read_label.setText(

            f"Last Read : {last_text}"

        )