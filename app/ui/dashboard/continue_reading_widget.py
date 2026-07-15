from PySide6.QtCore import Signal

from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
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

from app.ui.components.progress_bar import (
    ProgressBar,
)


class ContinueReadingWidget(BaseCard):

    continue_requested = Signal()

    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.refresh()

    def setup_ui(self):

        self.title = QLabel(
            "Continue Reading"
        )

        self.title.setObjectName(
            "cardTitle"
        )

        self.layout.addWidget(
            self.title
        )

        self.book_title = QLabel()

        self.book_title.setObjectName(
            "bookTitle"
        )

        self.layout.addWidget(
            self.book_title
        )

        self.author = QLabel()

        self.author.setObjectName(
            "secondaryText"
        )

        self.layout.addWidget(
            self.author
        )

        self.progress = ProgressBar()

        self.layout.addWidget(
            self.progress
        )

        self.progress_text = QLabel()

        self.progress_text.setObjectName(
            "captionText"
        )

        self.layout.addWidget(
            self.progress_text
        )

        self.button = QPushButton(
            "Continue Reading"
        )

        self.button.setObjectName(
            "primaryButton"
        )

        self.button.clicked.connect(
            self.continue_requested.emit
        )

        self.layout.addWidget(
            self.button
        )

        self.layout.addStretch()

    def refresh(self):

        books = [

            book

            for book in BookService.get_all_books()

            if book.status == BookStatus.READING

        ]

        if not books:

            self.book_title.setText(
                "No active book"
            )

            self.author.setText(
                "Start reading from your library."
            )

            self.progress.set_progress(
                current=0,
                total=1,
            )

            self.progress_text.setText(
                "0 / 0 pages"
            )

            self.button.setText(
                "Browse Library"
            )

            self.button.setEnabled(
                False
            )

            return

        book = max(

            books,

            key=lambda item: item.current_page,

        )

        self.book_title.setText(
            book.title
        )

        self.author.setText(
            book.author
        )

        current = max(
            book.current_page or 0,
            0,
        )

        total = max(
            book.page_count or 0,
            1,
        )

        self.progress.set_progress(
            current=current,
            total=total,
        )

        self.progress_text.setText(
            f"{current} / {total} pages"
        )

        self.button.setText(
            "Continue Reading"
        )

        self.button.setEnabled(
            True
        )