from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel
)

from app.services.book_service import BookService

class RecentBooksCard(QWidget):

    MAX_ITEMS = 5

    # ----------------------------------
    # Initialization
    # ----------------------------------

    def __init__(self):
        super().__init__()

        self.setup_ui()

        self.refresh()

    def setup_ui(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(
            8,
        )

        self.title = QLabel(
            "Recent Books"
        )

        self.title.setObjectName(
            "cardTitle"
        )

        layout.addWidget(
            self.title
        )

        self.items = []

        for _ in range(self.MAX_ITEMS):

            label = QLabel()

            label.setObjectName(
                "summaryItem"
            )

            self.items.append(
                label
            )

            layout.addWidget(
                label
            )

        layout.addStretch()

        self.setLayout(
            layout
        )

    def refresh(self):

        books = BookService.get_recent_books()

        for label in self.items:

            label.clear()

        if not books:

            self.items[0].setText(
                "No books yet."
            )

            return

        for label, book in zip(
            self.items,
            books,
        ):

            label.setText(
                f"📖 {book.title} — {book.author}"
            )