from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
    QGridLayout,
    QFrame,
    QScrollArea
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

        root.setContentsMargins(16, 16, 16, 16)
        root.setSpacing(20)

        # ==================================================
        # Cover
        # ==================================================

        self.cover = BookCover("large")

        # ==================================================
        # Title
        # ==================================================

        self.title = QLabel()
        self.title.setObjectName("bookTitle")

        self.author = QLabel()
        self.author.setObjectName("secondaryText")

        # ==================================================
        # Status
        # ==================================================

        self.status = StatusBadge()

        status_row = QHBoxLayout()
        status_row.setContentsMargins(0, 0, 0, 0)

        status_row.addWidget(self.status)
        status_row.addStretch()

        # ==================================================
        # Progress
        # ==================================================

        self.progress = BookProgress()

        self.progress_text = QLabel()
        self.progress_text.setObjectName("secondaryText")

        # ==================================================
        # Metadata
        # ==================================================

        metadata_title = QLabel("Book Information")
        metadata_title.setObjectName("secondaryText")

        form = QGridLayout()
        form.setHorizontalSpacing(20)
        form.setVerticalSpacing(8)

        labels = [
            "Publisher",
            "Year",
            "Pages",
            "ISBN",
            "Genre",
            "Rating",
        ]

        self.publisher = QLabel()
        self.year = QLabel()
        self.pages = QLabel()
        self.isbn = QLabel()
        self.genre = QLabel()
        self.rating = QLabel()

        values = [
            self.publisher,
            self.year,
            self.pages,
            self.isbn,
            self.genre,
            self.rating,
        ]

        for row, (label_text, value) in enumerate(zip(labels, values)):

            label = QLabel(label_text)
            label.setObjectName("secondaryText")

            form.addWidget(label, row, 0)
            form.addWidget(value, row, 1)

        # ==================================================
        # Info Layout
        # ==================================================

        info = QVBoxLayout()
        info.setSpacing(8)

        info.addWidget(self.title)
        info.addWidget(self.author)
        info.addLayout(status_row)

        info.addSpacing(8)

        info.addWidget(self.progress)
        info.addWidget(self.progress_text)

        info.addSpacing(12)

        info.addWidget(metadata_title)
        info.addLayout(form)

        info.addStretch()

        # ==================================================
        # Header
        # ==================================================

        header = QHBoxLayout()
        header.setSpacing(24)

        header.addWidget(
            self.cover,
            0,
            Qt.AlignmentFlag.AlignTop,
        )

        header.addLayout(info, 1)

        # ==================================================
        # Divider
        # ==================================================

        divider = QFrame()
        divider.setFrameShape(QFrame.Shape.HLine)
        divider.setObjectName("divider")

        # ==================================================
        # Description
        # ==================================================

        self.description_title = QLabel("Description")
        self.description_title.setObjectName("secondaryText")

        self.description = QLabel()
        self.description.setWordWrap(True)
        self.description.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.description.setMargin(8)

        description_scroll = QScrollArea()
        description_scroll.setWidgetResizable(True)
        description_scroll.setFrameShape(QFrame.Shape.NoFrame)
        description_scroll.setMinimumHeight(140)
        description_scroll.setMaximumHeight(180)
        description_scroll.setWidget(self.description)

        # ==================================================
        # Assemble
        # ==================================================

        root.addLayout(header)
        root.addWidget(divider)

        root.addWidget(self.description_title)
        root.addWidget(self.description)

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

        current = book.current_page or 0
        total = book.page_count or 0

        self.progress_text.setText(
            f"{current} / {total} pages"
        )

        self.isbn.setText(
            book.isbn or "-"
        )

        self.publisher.setText(
            book.publisher or "-"
        )

        self.year.setText(
            str(book.published_year or "-")
        )

        self.pages.setText(
            str(book.page_count or "-")
        )

        self.genre.setText(
            book.genre or "-"
        )

        self.rating.setText(
            str(book.rating or "-")
        )

        self.description.setText(
            book.description or "-"
        )

    def clear(self):

        self.cover.clear()

        self.title.setText(
            "No Book Selected"
        )

        self.author.setText(
            "Select a book to view its details."
        )

        self.status.clear()

        self.progress.clear()

        self.progress_text.clear()

        self.publisher.setText("-")

        self.year.setText("-")

        self.pages.setText("-")

        self.isbn.setText("-")
        
        self.genre.setText("-")

        self.rating.setText("-")

        self.description.setText(
            "Select a book to view its description."
        )