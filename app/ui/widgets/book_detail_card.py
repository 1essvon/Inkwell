from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
)

from app.models.book import Book

from app.ui.components.status_badge import StatusBadge
from app.ui.components.book_progress import BookProgress


class BookDetailCard(QWidget):

    def __init__(self):
        super().__init__()

        self.setup_ui()

        self.clear()

    # ==================================================
    # UI
    # ==================================================

    def setup_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(8)

        # ----------------------------------
        # Title
        # ----------------------------------

        self.title = QLabel()
        self.title.setObjectName(
            "bookTitle"
        )

        self.author = QLabel()
        self.author.setObjectName(
            "secondaryText"
        )

        # ----------------------------------
        # Status
        # ----------------------------------

        self.status = StatusBadge()

        # ----------------------------------
        # Progress
        # ----------------------------------

        self.progress = BookProgress()

        # ----------------------------------
        # Metadata
        # ----------------------------------

        self.isbn = QLabel()

        self.publisher = QLabel()

        self.genre = QLabel()

        self.rating = QLabel()

        # ----------------------------------
        # Layout
        # ----------------------------------

        layout.addWidget(self.title)
        layout.addWidget(self.author)

        layout.addSpacing(8)

        layout.addWidget(self.status)

        layout.addWidget(self.progress)

        layout.addSpacing(8)

        layout.addWidget(self.isbn)
        layout.addWidget(self.publisher)
        layout.addWidget(self.genre)
        layout.addWidget(self.rating)

    # ==================================================
    # Public API
    # ==================================================

    def set_book(
        self,
        book: Book,
    ):

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
            f"ISBN: {book.isbn or '-'}"
        )

        self.publisher.setText(
            f"Publisher: {book.publisher or '-'}"
        )

        self.genre.setText(
            f"Genre: {book.genre or '-'}"
        )

        self.rating.setText(
            f"Rating: {book.rating or '-'}"
        )

    def clear(self):

        self.title.setText(
            "No Book Selected"
        )

        self.author.clear()

        self.status.clear()

        self.progress.clear()

        self.isbn.clear()

        self.publisher.clear()

        self.genre.clear()

        self.rating.clear()