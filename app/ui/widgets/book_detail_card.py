from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QFrame,
)

from app.models.book import Book

from app.ui.components.book_cover import BookCover
from app.ui.components.book_progress import BookProgress
from app.ui.components.status_badge import StatusBadge


class BookDetailCard(QWidget):

    def __init__(self):
        super().__init__()

        self.setup_ui()

        self.clear()

    # ==================================================
    # UI
    # ==================================================

    def setup_ui(self):

        root = QVBoxLayout(self)

        root.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        root.setSpacing(20)

        # -------------------------------------------------
        # Header
        # -------------------------------------------------

        header = QHBoxLayout()

        header.setSpacing(20)

        self.cover = BookCover(
            size="large"
        )

        info_layout = QVBoxLayout()

        info_layout.setSpacing(8)

        self.title = QLabel()

        self.title.setObjectName(
            "bookTitle"
        )

        self.author = QLabel()

        self.author.setObjectName(
            "secondaryText"
        )

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

        info_layout.addStretch()

        info_layout.addWidget(
            self.title
        )

        info_layout.addWidget(
            self.author
        )

        info_layout.addLayout(
            status_layout
        )

        info_layout.addStretch()

        header.addWidget(
            self.cover
        )

        header.addLayout(
            info_layout,
            1,
        )

        # -------------------------------------------------
        # Progress
        # -------------------------------------------------

        self.progress = BookProgress()

        # -------------------------------------------------
        # Divider
        # -------------------------------------------------

        divider = QFrame()

        divider.setFrameShape(
            QFrame.Shape.HLine
        )

        divider.setObjectName(
            "divider"
        )

        # -------------------------------------------------
        # Metadata
        # -------------------------------------------------

        metadata = QGridLayout()

        metadata.setHorizontalSpacing(
            40
        )

        metadata.setVerticalSpacing(
            14
        )

        self.isbn_title = QLabel(
            "ISBN"
        )

        self.publisher_title = QLabel(
            "Publisher"
        )

        self.genre_title = QLabel(
            "Genre"
        )

        self.rating_title = QLabel(
            "Rating"
        )

        for label in (

            self.isbn_title,

            self.publisher_title,

            self.genre_title,

            self.rating_title,

        ):

            label.setObjectName(
                "secondaryText"
            )

        self.isbn = QLabel()

        self.publisher = QLabel()

        self.genre = QLabel()

        self.rating = QLabel()

        metadata.addWidget(
            self.isbn_title,
            0,
            0,
        )

        metadata.addWidget(
            self.publisher_title,
            0,
            1,
        )

        metadata.addWidget(
            self.isbn,
            1,
            0,
        )

        metadata.addWidget(
            self.publisher,
            1,
            1,
        )

        metadata.addWidget(
            self.genre_title,
            2,
            0,
        )

        metadata.addWidget(
            self.rating_title,
            2,
            1,
        )

        metadata.addWidget(
            self.genre,
            3,
            0,
        )

        metadata.addWidget(
            self.rating,
            3,
            1,
        )

        # -------------------------------------------------
        # Assemble
        # -------------------------------------------------

        root.addLayout(
            header
        )

        root.addWidget(
            self.progress
        )

        root.addWidget(
            divider
        )

        root.addLayout(
            metadata
        )

        root.addStretch()

    # ==================================================
    # Public API
    # ==================================================

    def set_book(
        self,
        book: Book,
    ):

        self.cover.set_cover(
            book.cover_path
        )

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

        self.isbn.setText(
            book.isbn or "-"
        )

        self.publisher.setText(
            book.publisher or "-"
        )

        self.genre.setText(
            book.genre or "-"
        )

        self.rating.setText(
            str(book.rating or "-")
        )

    def clear(self):

        self.cover.clear()

        self.title.setText(
            "No Book Selected"
        )

        self.author.clear()

        self.status.clear()

        self.progress.clear()

        self.isbn.setText("-")

        self.publisher.setText("-")

        self.genre.setText("-")

        self.rating.setText("-")