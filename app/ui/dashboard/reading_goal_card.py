from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel
)

from app.services.book_service import (
    BookService,
)

from app.services.settings_service import (
    SettingsService,
)

from app.constants.book_status import (
    BookStatus,
)

from app.ui.components.base_card import (
    BaseCard,
)

from app.ui.components.progress_bar import (
    ProgressBar,
)


class ReadingGoalCard(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.refresh()

    def setup_ui(self):

        root = QVBoxLayout(self)

        root.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self.card = BaseCard()

        root.addWidget(
            self.card
        )

        self.title = QLabel(
            "Reading Goal"
        )

        self.title.setObjectName(
            "cardTitle"
        )

        self.card.layout.addWidget(
            self.title
        )

        self.progress_text = QLabel()

        self.progress_text.setObjectName(
            "secondaryText"
        )

        self.card.layout.addWidget(
            self.progress_text
        )

        self.progress = ProgressBar()

        self.card.layout.addWidget(
            self.progress
        )

    def refresh(self):

        settings = SettingsService.get()

        goal = settings.reading_goal_books

        summary = BookService.get_status_summary()

        completed = summary[
            BookStatus.COMPLETED
        ]

        remaining = max(
            goal - completed,
            0,
        )

        if goal <= 0:

            self.progress_text.setText(
                "No reading goal configured"
            )

            self.progress.set_value(
                0
            )

            return

        if completed >= goal:

            status = "🎉 Goal achieved!"

        else:

            status = (
                f"{remaining} books remaining"
            )

        self.progress_text.setText(

            f"{completed} / {goal} books\n"
            f"{status}"

        )

        self.progress.set_progress(
            current=completed,
            total=goal,
        )