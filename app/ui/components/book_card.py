from PySide6.QtWidgets import (
    QLabel,
    QHBoxLayout,
)

from app.models.book import Book

from app.ui.components.base_card import BaseCard
from app.ui.components.status_badge import StatusBadge
from app.ui.components.book_progress import BookProgress


class BookCard(BaseCard):

    def __init__(
        self,
        book: Book,
    ):
        super().__init__()

        self.book = book

        self.setup_ui()

        self.set_book(book)

    # ==================================================
    # UI
    # ==================================================

    def setup_ui(self):

        self.layout.setSpacing(8)

        # --------------------------
        # Title
        # --------------------------

        self.title = QLabel()
        self.title.setObjectName("bookTitle")

        # --------------------------
        # Author
        # --------------------------

        self.author = QLabel()
        self.author.setObjectName("secondaryText")

        # --------------------------
        # Status
        # --------------------------

        self.status = StatusBadge()

        self.status_layout = QHBoxLayout()
        self.status_layout.setContentsMargins(0, 0, 0, 0)

        self.status_layout.addWidget(self.status)
        self.status_layout.addStretch()

        # --------------------------
        # Progress
        # --------------------------

        self.progress = BookProgress()

        # --------------------------
        # Layout
        # --------------------------

        self.layout.addWidget(self.title)
        self.layout.addWidget(self.author)
        self.layout.addLayout(self.status_layout)
        self.layout.addWidget(self.progress)
        self.layout.addStretch()

        self.adjustSize()

        self.setMinimumHeight(
            self.sizeHint().height()
        )

    # ==================================================
    # Public API
    # ==================================================

    def set_book(
        self,
        book: Book,
    ):

        self.book = book

        self.title.setText(
            book.title
        )

        self.author.setText(
            book.author
        )

        self.status.set_status(
            book.status
        )

        self.progress.set_progress(
            book.current_page,
            book.page_count,
        )