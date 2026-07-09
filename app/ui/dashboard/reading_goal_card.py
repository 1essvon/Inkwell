from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QProgressBar,
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


class ReadingGoalCard(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.refresh()

    def setup_ui(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(
            8,
        )

        self.title = QLabel(
            "Reading Goal"
        )

        self.title.setObjectName(
            "cardTitle"
        )

        self.progress_text = QLabel()

        self.progress = QProgressBar()

        layout.addWidget(
            self.title
        )

        layout.addWidget(
            self.progress_text
        )

        layout.addWidget(
            self.progress
        )

        self.setLayout(
            layout)

    def refresh(self):

        settings = SettingsService.get()

        goal = settings.reading_goal_books

        summary = BookService.get_status_summary()

        completed = summary[
            BookStatus.COMPLETED
        ]

        if goal > 0:

            percent = int(
                completed / goal * 100
            )

        else:

            percent = 0

        percent = max(
            0,
            min(
                percent,
                100,
            ),
        )

        if completed >= goal:

            status = "🎉 Goal achieved!"

        else:

            remaining = goal - completed

            status = (
                f"{remaining} books to go"
            )

        self.progress_text.setText(

            f"{completed} / {goal} books\n"
            f"{status}"

        )

        self.progress.setValue(
            percent
        )