from PySide6.QtWidgets import (
    QLabel,
    QProgressBar
)

from app.constants.book_status import BookStatus
from app.constants.book_status import BookStatus
from app.models.book import Book

from app.ui.components.base_card import (
    BaseCard
)


class BookCard(BaseCard):

    def __init__(
        self,
        book: Book
    ):
        super().__init__()

        self.book = book

        # ======================
        # Title
        # ======================

        self.title = QLabel(
            f"📖 {book.title}"
        )

        self.title.setObjectName(
            "bookTitle"
        )

        # ======================
        # Author
        # ======================

        self.author = QLabel(
            book.author
        )

        self.author.setObjectName(
            "bookAuthor"
        )

        # ======================
        # Progress Text
        # ======================

        current = book.current_page or 0

        total = book.page_count or 0

        self.progress_text = QLabel(
            f"{current} / {total}"
        )

        self.progress_text.setObjectName(
            "bookProgress"
        )

        # ======================
        # Progress Bar
        # ======================

        self.progress = QProgressBar()

        if total > 0:

            percent = int(
                current / total * 100
            )

        else:

            percent = 0

        self.progress.setValue(
            percent
        )

        # ======================
        # Status
        # ======================

        status = book.status

        self.status = QLabel(
            status
        )

        if status == BookStatus.READING:

            self.status.setObjectName(
                "statusReading"
            )

        elif status == BookStatus.COMPLETED:

            self.status.setObjectName(
                "statusFinished"
            )

        elif status == BookStatus.WANT_TO_READ:

            self.status.setObjectName(
                "statusWaiting"
            )

        elif status == BookStatus.PAUSED:

            self.status.setObjectName(
                "statusPaused"
            )

        elif status == BookStatus.DROPPED:

            self.status.setObjectName(
                "statusDropped"
            )

        else:

            self.status.setObjectName(
                "statusUnknown"
            )

        # ======================
        # Layout
        # ======================

        self.layout.addWidget(
            self.title
        )

        self.layout.addWidget(
            self.author
        )

        self.layout.addWidget(
            self.progress_text
        )

        self.layout.addWidget(
            self.progress
        )

        self.layout.addWidget(
            self.status
        )