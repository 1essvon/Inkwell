from PySide6.QtWidgets import (
    QLabel,
    QProgressBar
)

from app.models.book import Book

from app.ui.components.base_card import (
    BaseCard
)

class ReadingBookCard(BaseCard):

    def __init__(
        self,
        book: Book
    ):
        super().__init__()

        self.book = book

        self.setup_ui()

    def setup_ui(self):

        current = self.book.current_page or 0

        total = self.book.page_count or 0

        percent = 0

        if total > 0:

            percent = int(
                (current / total) * 100
            )

        # ==========================
        # Title
        # ==========================

        title = QLabel(
            f"📖 {self.book.title}"
        )

        title.setObjectName(
            "bookTitle"
        )

        self.layout.addWidget(
            title
        )

        # ==========================
        # Author
        # ==========================

        author = QLabel(
            self.book.author
        )

        author.setObjectName(
            "secondaryText"
        )

        self.layout.addWidget(
            author
        )

        self.layout.addSpacing(8)

        # ==========================
        # Progress
        # ==========================

        progress = QLabel(
            f"{current} / {total} pages"
        )

        progress.setObjectName(
            "bookProgress"
        )

        self.layout.addWidget(
            progress
        )

        bar = QProgressBar()

        bar.setRange(
            0,
            100
        )

        bar.setValue(
            percent
        )

        bar.setTextVisible(
            False
        )

        self.layout.addWidget(
            bar
        )

        percent_label = QLabel(
            f"{percent}%"
        )

        percent_label.setObjectName(
            "secondaryText"
        )

        self.layout.addWidget(
            percent_label
        )

        self.layout.addSpacing(8)

        # ==========================
        # Status
        # ==========================

        status = QLabel(
            f"● {self.book.status.title()}"
        )

        status.setObjectName(
            "summaryItem"
        )

        self.layout.addWidget(
            status
        )