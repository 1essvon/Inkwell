from PySide6.QtWidgets import (
    QLabel,
    QProgressBar,
    QHBoxLayout,
)

from app.models.book import Book

from app.ui.components.base_card import (
    BaseCard
)
from app.ui.components.icon_provider import (
    SIZE_INLINE,
    pixmap,
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

        title_row = QHBoxLayout()
        title_row.setContentsMargins(0, 0, 0, 0)
        title_row.setSpacing(8)

        book_icon = QLabel()
        book_icon.setObjectName("cardIcon")
        book_icon.setProperty("inkwell_icon_name", "book")
        book_icon.setProperty("inkwell_icon_size", SIZE_INLINE)
        book_icon.setPixmap(
            pixmap("book", size=SIZE_INLINE)
        )

        title = QLabel(self.book.title)

        title.setObjectName(
            "bookTitle"
        )

        title_row.addWidget(book_icon)
        title_row.addWidget(title, 1)
        self.layout.addLayout(title_row)

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
            self.book.status.title()
        )

        status.setObjectName(
            "bookStatus"
        )

        self.layout.addWidget(
            status
        )

    def set_selected(
        self,
        selected: bool,
    ):

        self.setProperty(
            "selected",
            selected,
        )

        self.style().unpolish(
            self
        )

        self.style().polish(
            self
        )

        self.update()