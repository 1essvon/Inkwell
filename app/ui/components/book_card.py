from PySide6.QtWidgets import (
    QLabel,
    QHBoxLayout,
    QVBoxLayout
)

from app.models.book import Book

from app.ui.components.base_card import BaseCard
from app.ui.components.status_badge import StatusBadge
from app.ui.components.book_progress import BookProgress
from app.ui.components.book_cover import BookCover

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

        self.layout.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        self.layout.setSpacing(12)

        self.setMinimumHeight(160)

        # ----------------------------------
        # Title
        # ----------------------------------

        self.title = QLabel()

        self.title.setObjectName(
            "bookTitle"
        )

        # ----------------------------------
        # Author
        # ----------------------------------

        self.author = QLabel()

        self.author.setObjectName(
            "secondaryText"
        )

        # ----------------------------------
        # Cover
        # ----------------------------------

        self.cover = BookCover("small")

        # ----------------------------------
        # Status
        # ----------------------------------

        self.status = StatusBadge()

        status_layout = QHBoxLayout()

        status_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        status_layout.addWidget(
            self.status
        )

        status_layout.addStretch()

        # ----------------------------------
        # Progress
        # ----------------------------------

        self.progress = BookProgress()

        # ----------------------------------
        # Info Layout
        # ----------------------------------

        info_layout = QVBoxLayout()

        info_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        info_layout.setSpacing(6)

        info_layout.addWidget(
            self.title
        )

        info_layout.addWidget(
            self.author
        )

        info_layout.addSpacing(4)

        info_layout.addLayout(
            status_layout
        )

        info_layout.addWidget(
            self.progress
        )

        # ----------------------------------
        # Root Layout
        # ----------------------------------

        root = QHBoxLayout()

        root.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        root.setSpacing(16)

        root.addWidget(
            self.cover
        )

        root.addLayout(
            info_layout,
        )

        self.layout.addLayout(
            root
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

        self.cover.set_cover(
            book.cover_path
        )

        self.status.set_status(
            book.status
        )

        self.progress.set_progress(
            book.current_page,
            book.page_count,
        )