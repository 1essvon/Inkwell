from PySide6.QtWidgets import (
    QLabel
)

from app.ui.components.base_card import (
    BaseCard
)


class BookCard(BaseCard):

    def __init__(
        self,
        title,
        author,
        progress
    ):

        super().__init__()

        self.title = QLabel(title)
        self.title.setObjectName(
            "bookTitle"
        )

        self.author = QLabel(author)
        self.author.setObjectName(
            "bookAuthor"
        )

        self.progress = QLabel(progress)
        self.progress.setObjectName(
            "bookProgress"
        )

        self.layout.addWidget(
            self.title
        )

        self.layout.addWidget(
            self.author
        )

        self.layout.addWidget(
            self.progress
        )