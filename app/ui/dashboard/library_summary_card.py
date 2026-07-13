from PySide6.QtWidgets import (
    QGridLayout,
    QLabel,
)

from app.constants.book_status import (
    BookStatus,
)

from app.services.book_service import (
    BookService,
)

from app.ui.components.base_card import (
    BaseCard,
)

class LibrarySummaryCard(BaseCard):

    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.refresh()

    def setup_ui(self):

        self.title = QLabel(
            "Library Summary"
        )

        self.title.setObjectName(
            "cardTitle"
        )

        self.layout.addWidget(
            self.title
        )

        self.grid = QGridLayout()

        self.grid.setHorizontalSpacing(
            20
        )

        self.grid.setVerticalSpacing(
            12
        )

        self.layout.addLayout(
            self.grid
        )

        self.reading = QLabel()

        self.want = QLabel()

        self.completed = QLabel()

        self.paused = QLabel()

        self.dropped = QLabel()

        labels = [

            self.reading,

            self.want,

            self.completed,

            self.paused,

            self.dropped,

        ]

        for label in labels:

            label.setObjectName(
                "summaryItem"
            )

        self.grid.addWidget(
            self.reading,
            0,
            0,
        )

        self.grid.addWidget(
            self.want,
            1,
            0,
        )

        self.grid.addWidget(
            self.completed,
            2,
            0,
        )

        self.grid.addWidget(
            self.paused,
            3,
            0,
        )

        self.grid.addWidget(
            self.dropped,
            4,
            0,
        )

        self.layout.addStretch()

    def refresh(self):

        summary = BookService.get_status_summary()

        self.reading.setText(
            f"📖 Reading : {summary[BookStatus.READING]}"
        )

        self.want.setText(
            f"📚 Want To Read : {summary[BookStatus.WANT_TO_READ]}"
        )

        self.completed.setText(
            f"✅ Completed : {summary[BookStatus.COMPLETED]}"
        )

        self.paused.setText(
            f"⏸ Paused : {summary[BookStatus.PAUSED]}"
        )

        self.dropped.setText(
            f"❌ Dropped : {summary[BookStatus.DROPPED]}"
        )