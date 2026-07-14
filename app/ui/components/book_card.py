from PySide6.QtWidgets import (
    QLabel,
    QProgressBar,
    QHBoxLayout
)

from app.constants.book_status import BookStatus
from app.models.book import Book
from app.ui.components.base_card import BaseCard

class BookCard(BaseCard):

    STATUS_OBJECT_NAMES = {

        BookStatus.READING:
            "badgeReading",

        BookStatus.COMPLETED:
            "badgeFinished",

        BookStatus.WANT_TO_READ:
            "badgeWaiting",

        BookStatus.PAUSED:
            "badgePaused",

        BookStatus.DROPPED:
            "badgeDanger",

    }

    def __init__(
        self,
        book: Book,
    ):

        super().__init__()

        self.book = book

        self.setup_ui()

        self.populate_data()

    def setup_ui(self):

        # ======================
        # Title
        # ======================

        self.title = QLabel()

        self.title.setObjectName(
            "bookTitle"
        )

        # ======================
        # Author
        # ======================

        self.author = QLabel()

        self.author.setObjectName(
            "secondaryText"
        )

        # ======================
        # Status
        # ======================

        self.status = QLabel()

        self.status.adjustSize()

        self.status.setMinimumWidth(90)

        # ======================
        # Progress
        # ======================

        self.progress = QProgressBar()

        self.progress.setTextVisible(
            False
        )

        self.progress_text = QLabel()

        self.progress_text.setObjectName(
            "captionText"
        )

        # ======================
        # Layout
        # ======================

        self.layout.setSpacing(
            10
        )

        self.layout.addWidget(
            self.title
        )

        self.layout.addWidget(
            self.author
        )

        self.status_layout = QHBoxLayout()

        self.status_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self.status_layout.addWidget(
            self.status
        )

        self.status_layout.addStretch()

        self.layout.addLayout(
            self.status_layout
        )

        self.layout.addWidget(
            self.progress
        )

        self.layout.addWidget(
            self.progress_text
        )

    def populate_data(self):

        # ======================
        # Title
        # ======================

        self.title.setText(
            self.book.title
        )

        # ======================
        # Author
        # ======================

        self.author.setText(
            self.book.author
        )

        # ======================
        # Progress
        # ======================

        current = self.book.current_page or 0

        total = self.book.page_count or 0

        percent = self.calculate_progress(
            current,
            total,
        )

        self.progress.setValue(
            percent
        )

        self.progress_text.setText(
            f"{current} / {total} pages"
        )

        # ======================
        # Status
        # ======================

        status = self.book.status

        self.status.setText(
            status
        )

    def calculate_progress(
        self,
        current,
        total,
    ):

        if total <= 0:

            return 0

        return int(

            current / total * 100

        )
    
    def get_status_object_name(
        self,
        status,
    ):

        return self.STATUS_OBJECT_NAMES.get(

            status,

            "badgeDefault",

        )