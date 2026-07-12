from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
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

class ContinueReadingWidget(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.refresh()

    def setup_ui(self):

        root = QVBoxLayout(self)

        root.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self.card = BaseCard()

        root.addWidget(
            self.card
        )

        self.title_label = QLabel(
            "Continue Reading"
        )

        font = self.title_label.font()

        font.setBold(True)

        self.title_label.setFont(font)

        self.card.layout.addWidget(
            self.title_label
        )

        content = QHBoxLayout()

        content.setSpacing(
            16
        )

        self.card.layout.addLayout(
            content
        )

        self.cover = QLabel(
            "Cover"
        )

        self.cover.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.cover.setFixedSize(
            90,
            130,
        )

        self.cover.setObjectName(
            "bookCover"
        )

        content.addWidget(
            self.cover
        )

        right = QVBoxLayout()

        right.setSpacing(
            8
        )

        content.addLayout(
            right,
            1,
        )

        self.book_title = QLabel()

        font = self.book_title.font()

        font.setPointSize(
            12
        )

        font.setBold(
            True
        )

        self.book_title.setFont(
            font
        )

        right.addWidget(
            self.book_title
        )

        self.author = QLabel()

        self.author.setObjectName(
            "secondaryText"
        )

        right.addWidget(
            self.author
        )

        self.page = QLabel()

        self.page.setObjectName(
            "secondaryText"
        )

        right.addWidget(
            self.page
        )

        self.progress = ProgressBar()

        right.addWidget(
            self.progress
        )

        self.button = QPushButton(
            "Continue Reading"
        )

        right.addWidget(
            self.button,
            alignment=Qt.AlignmentFlag.AlignLeft
        )

    def refresh(self):

        book = BookService.get_current_reading()

        if book is None:

            self.book_title.setText(
                "No active reading"
            )

            self.author.clear()

            self.page.clear()

            self.cover.setText(
                "No Cover"
            )

            self.progress.set_value(
                0
            )

            self.button.setEnabled(
                False
            )

            return

        self.button.setEnabled(
            True
        )

        self.cover.setText(
            "Cover"
        )

        self.book_title.setText(
            book.title
        )

        self.author.setText(
            book.author
        )

        self.page.setText(
            f"Page {book.current_page} / {book.page_count}"
        )

        self.progress.set_progress(
            current=book.current_page,
            total=book.page_count,
        )