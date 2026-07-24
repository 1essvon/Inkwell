from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QListWidget,
)

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QListWidgetItem

from app.services.book_service import BookService

from app.services.google_books_service import (
    GoogleBooksService,
)

class BookImportDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.setup_ui()
        self.connect_signals()

    # ==================================================
    # UI
    # ==================================================

    def setup_ui(self):

        self.setWindowTitle("Import Book")

        self.resize(650, 500)

        root = QVBoxLayout(self)

        # ----------------------------
        # Search
        # ----------------------------

        title = QLabel("Import Book")

        title.setObjectName("pageTitle")

        root.addWidget(title)

        root.addWidget(
            QLabel("Search by title, author, or ISBN")
        )

        search_layout = QHBoxLayout()

        self.search_input = QLineEdit()

        self.search_input.setPlaceholderText(
            "Atomic Habits"
        )

        self.search_button = QPushButton(
            "Search"
        )

        search_layout.addWidget(
            self.search_input,
            1,
        )

        search_layout.addWidget(
            self.search_button
        )

        root.addLayout(
            search_layout
        )

        # ----------------------------
        # Results
        # ----------------------------

        self.results = QListWidget()

        root.addWidget(
            self.results,
            1,
        )

        # ----------------------------
        # Bottom buttons
        # ----------------------------

        bottom = QHBoxLayout()

        bottom.addStretch()

        self.cancel_button = QPushButton(
            "Cancel"
        )

        self.import_button = QPushButton(
            "Import"
        )

        self.import_button.setEnabled(
            False
        )

        bottom.addWidget(
            self.cancel_button
        )

        bottom.addWidget(
            self.import_button
        )

        root.addLayout(
            bottom
        )

    # ==================================================
    # Signals
    # ==================================================

    def connect_signals(self):

        self.cancel_button.clicked.connect(
            self.reject
        )

        self.search_button.clicked.connect(
            self.search_books
        )

        self.results.itemSelectionChanged.connect(
            self.update_buttons
        )

        self.import_button.clicked.connect(
            self.import_selected
        )

    # ==================================================
    # Events
    # ==================================================

    def search_books(self):

        query = self.search_input.text().strip()

        if not query:
            return

        self.results.clear()

        books = GoogleBooksService.search(query)

        for book in books:

            authors = ", ".join(book.authors)

            text = f"{book.title}\n{authors}"

            item = QListWidgetItem(text)

            item.setData(
                Qt.ItemDataRole.UserRole,
                book,
            )

            self.results.addItem(item)

    def import_selected(self):

        book = self.selected_book()

        if not book:
            return

        BookService.create_from_google_book(
            book
        )

        self.accept()

    def update_buttons(self):

        self.import_button.setEnabled(
            self.results.currentRow() >= 0
        )

    def selected_book(self):

        item = self.results.currentItem()

        if item is None:
            return None

        return item.data(
            Qt.ItemDataRole.UserRole
        )