from PySide6.QtCore import Signal

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QSizePolicy
)

from app.models.book import Book

from app.ui.widgets.book_detail_card import (
    BookDetailCard,
)


class BookDetailView(QWidget):

    editRequested = Signal()

    deleteRequested = Signal()

    continueRequested = Signal()

    notesRequested = Signal()

    quotesRequested = Signal()

    def __init__(self):
        super().__init__()

        self.book = None

        self.setup_ui()

        self.setup_connections()

    # ==================================================
    # UI
    # ==================================================

    def setup_ui(self):

        root = QVBoxLayout(self)

        root.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        root.setSpacing(16)

        self.card = BookDetailCard()

        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Ignored,
        )

        root.addWidget(
            self.card,
            1,
        )

        actions = QHBoxLayout()

        actions.setSpacing(8)

        self.continue_button = QPushButton(
            "Continue Reading"
        )

        self.notes_button = QPushButton(
            "Notes"
        )

        self.quotes_button = QPushButton(
            "Quotes"
        )

        self.edit_button = QPushButton(
            "Edit"
        )

        self.delete_button = QPushButton(
            "Delete"
        )

        self.continue_button.setObjectName(
            "primaryButton"
        )

        self.notes_button.setObjectName(
            "secondaryButton"
        )

        self.quotes_button.setObjectName(
            "secondaryButton"
        )

        self.edit_button.setObjectName(
            "secondaryButton"
        )

        self.delete_button.setObjectName(
            "dangerButton"
        )

        actions.addWidget(
            self.continue_button
        )

        actions.addWidget(
            self.notes_button
        )

        actions.addWidget(
            self.quotes_button
        )

        actions.addStretch()

        actions.addWidget(
            self.edit_button
        )

        actions.addWidget(
            self.delete_button
        )

        root.addLayout(
            actions
        )

        self.clear()

    # ==================================================
    # Connections
    # ==================================================

    def setup_connections(self):

        self.continue_button.clicked.connect(
            self.continueRequested.emit
        )

        self.notes_button.clicked.connect(
            self.notesRequested.emit
        )

        self.quotes_button.clicked.connect(
            self.quotesRequested.emit
        )

        self.edit_button.clicked.connect(
            self.editRequested.emit
        )

        self.delete_button.clicked.connect(
            self.deleteRequested.emit
        )

    # ==================================================
    # Public API
    # ==================================================

    def display_book(
        self,
        book: Book,
    ):

        self.book = book

        self.card.set_book(
            book
        )

        enabled = book is not None

        for button in (

            self.continue_button,

            self.notes_button,

            self.quotes_button,

            self.edit_button,

            self.delete_button,

        ):

            button.setEnabled(
                enabled
            )

    def clear(self):

        self.book = None

        self.card.clear()

        for button in (

            self.continue_button,

            self.notes_button,

            self.quotes_button,

            self.edit_button,

            self.delete_button,

        ):

            button.setEnabled(
                False
            )