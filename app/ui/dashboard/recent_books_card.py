from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QVBoxLayout,
    QWidget,
)

from app.ui.components.base_card import BaseCard
from app.ui.components.book_list_item import BookListItem
from app.ui.components.empty_state import EmptyState
from app.ui.components.section_header import SectionHeader


class RecentBooksCard(BaseCard):

    MAX_ITEMS = 5

    def __init__(self):
        super().__init__()

        self.setup_ui()

        self.set_data([])

    # ==================================================
    # UI
    # ==================================================

    def setup_ui(self):

        #
        # Header
        #

        self.header = SectionHeader(
            "Recent Books"
        )

        self.layout.addWidget(
            self.header
        )

        #
        # Empty State
        #

        self.empty = EmptyState(

            icon="📚",

            title="No recent books",

            subtitle=(
                "Books you add will\n"
                "appear here."
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
            10
        )

        self.items = []

        for index in range(
            self.MAX_ITEMS
        ):

            item = BookListItem()

            content_layout.addWidget(
                item
            )

            self.items.append(
                item
            )

            if index < self.MAX_ITEMS - 1:

                divider = QFrame()

                divider.setFrameShape(
                    QFrame.Shape.HLine
                )

                divider.setObjectName(
                    "divider"
                )

                content_layout.addWidget(
                    divider
                )

        self.footer = QLabel()

        self.footer.setObjectName(
            "secondaryText"
        )

        content_layout.addWidget(
            self.footer
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
        books,
    ):

        has_books = bool(
            books
        )

        self.toggle_empty_state(
            has_books
        )

        if not has_books:
            return

        for item in self.items:
            item.hide()

        for item, book in zip(
            self.items,
            books,
        ):

            item.set_data(

                title=book["title"],

                subtitle=book["author"],

            )

            item.show()

        self.footer.setText(
            f"{len(books)} recent books"
        )    