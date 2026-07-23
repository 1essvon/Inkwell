from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from app.ui.components.base_card import BaseCard
from app.ui.components.empty_state import EmptyState
from app.ui.components.progress_bar import ProgressBar
from app.ui.components.section_header import SectionHeader


class ContinueReadingWidget(BaseCard):

    def __init__(self):
        super().__init__()

        self.setup_ui()

        self.set_data(None)

    # ==================================================
    # UI
    # ==================================================

    def setup_ui(self):

        #
        # Header
        #

        self.header = SectionHeader(
            "Continue Reading"
        )

        self.layout.addWidget(
            self.header
        )

        #
        # Empty State
        #

        self.empty = EmptyState(

            icon="📚",

            title="No active book",

            subtitle=(
                "Start reading a book "
                "to continue your journey."
            ),

        )

        self.layout.addWidget(
            self.empty
        )

        #
        # Content
        #

        self.content = QWidget()

        content_layout = QVBoxLayout(
            self.content
        )

        content_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        content_layout.setSpacing(
            8
        )

        self.book_title = QLabel()

        self.book_title.setObjectName(
            "bookTitle"
        )

        content_layout.addWidget(
            self.book_title
        )

        self.author = QLabel()

        self.author.setObjectName(
            "secondaryText"
        )

        content_layout.addWidget(
            self.author
        )

        self.progress = ProgressBar()

        content_layout.addWidget(
            self.progress
        )

        progress_info = QHBoxLayout()

        self.progress_text = QLabel()

        self.progress_text.setObjectName(
            "captionText"
        )

        progress_info.addWidget(
            self.progress_text
        )

        content_layout.addLayout(
            progress_info
        )


        divider = QFrame()

        divider.setFrameShape(
            QFrame.Shape.HLine
        )

        content_layout.addSpacing(
            4
        )

        content_layout.addWidget(
            divider
        )

        self.status = QLabel()

        self.status.setObjectName(
            "secondaryText"
        )

        self.status.setContentsMargins(
            0,
            4,
            0,
            0,
        )

        self.status.setWordWrap(
            True
        )

        content_layout.addWidget(
            self.status
        )

        self.layout.addWidget(
            self.content
        )

        self.layout.addStretch()

    # ==================================================
    # Public API
    # ==================================================

    def set_data(
        self,
        data,
    ):

        has_book = data is not None

        self.toggle_empty_state(
            has_book
        )

        if not has_book:
            return

        self.book_title.setText(
            data["title"]
        )

        self.author.setText(
            data["author"]
        )

        self.progress.set_progress(
            data["current_page"],
            data["total_pages"],
        )

        self.progress_text.setText(
            data["progress_text"]
        )

        self.status.setText(
            data["status"]
        )