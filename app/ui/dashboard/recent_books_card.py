from PySide6.QtWidgets import (
    QFrame,
    QLabel,
)

from app.services.book_service import (
    BookService,
)

from app.ui.components.base_card import (
    BaseCard,
)

class RecentBooksCard(BaseCard):

    MAX_ITEMS = 5

    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.refresh()

    def setup_ui(self):

        self.title = QLabel(
            "Recent Books"
        )

        self.title.setObjectName(
            "cardTitle"
        )

        self.layout.addWidget(
            self.title
        )

        self.items = []

        for index in range(
            self.MAX_ITEMS
        ):

            title = QLabel()

            title.setObjectName(
                "bookTitle"
            )

            author = QLabel()

            author.setObjectName(
                "secondaryText"
            )

            self.layout.addWidget(
                title
            )

            self.layout.addWidget(
                author
            )

            if index < self.MAX_ITEMS - 1:

                divider = QFrame()

                divider.setFrameShape(
                    QFrame.Shape.HLine
                )

                divider.setObjectName(
                    "divider"
                )

                self.layout.addWidget(
                    divider
                )

            self.items.append(
                (
                    title,
                    author,
                )
            )

        self.layout.addStretch()

    def refresh(self):

        books = BookService.get_recent_books()

        for title, author in self.items:

            title.clear()

            author.clear()

        if not books:

            self.items[0][0].setText(
                "No books yet."
            )

            return

        for (
            title,
            author,
        ), book in zip(
            self.items,
            books,
        ):

            title.setText(
                f"📖 {book.title}"
            )

            author.setText(
                book.author
            )