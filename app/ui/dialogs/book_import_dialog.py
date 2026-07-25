from PySide6.QtWidgets import (
    QDialog,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QListWidget,
    QListWidgetItem,
    QTextEdit,
    QMessageBox,
)

from PySide6.QtCore import Qt

from PySide6.QtGui import (
    QPixmap,
)

from urllib.request import urlopen

from app.services.book_service import BookService

from app.services.thumbnail_loader import (
    ThumbnailLoader,
)

from app.services.google_books_service import (
    GoogleBooksService,
)

class BookImportDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.setup_ui()
        self.connect_signals()

        self.thumbnail_loader = ThumbnailLoader()

        self.thumbnail_loader.loaded.connect(
            self.on_thumbnail_loaded
        )

        self.thumbnail_loader.failed.connect(
            self.on_thumbnail_failed
        )

    # ==================================================
    # UI
    # ==================================================

    def setup_ui(self):

        self.setWindowTitle("Import Book")
        self.resize(900, 550)

        root = QVBoxLayout(self)

        # ----------------------------
        # Header
        # ----------------------------

        title = QLabel("Import Book")
        title.setObjectName("pageTitle")

        root.addWidget(title)

        root.addWidget(
            QLabel("Search by title, author, or ISBN")
        )

        # ----------------------------
        # Search
        # ----------------------------

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
            self.search_button,
        )

        root.addLayout(search_layout)

        # ----------------------------
        # Content
        # ----------------------------

        content_layout = QHBoxLayout()

        self.results = QListWidget()

        content_layout.addWidget(
            self.results,
            1,
        )

        content_layout.addWidget(
            self.create_preview_panel(),
            2,
        )

        root.addLayout(
            content_layout,
            1,
        )

        # ----------------------------
        # Bottom Buttons
        # ----------------------------

        bottom = QHBoxLayout()

        bottom.addStretch()

        self.cancel_button = QPushButton(
            "Cancel"
        )

        self.import_button = QPushButton(
            "Import"
        )

        self.import_button.setEnabled(False)

        bottom.addWidget(
            self.cancel_button
        )

        bottom.addWidget(
            self.import_button
        )

        root.addLayout(bottom)

        self.clear_preview()

    def create_preview_panel(self):

        panel = QWidget()

        layout = QVBoxLayout(panel)

        self.cover_label = QLabel()

        self.cover_label.setFixedSize(
            160,
            220,
        )

        self.cover_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.cover_label.setStyleSheet("""
            border: 1px solid #666;
        """)

        layout.addWidget(
            self.cover_label,
            alignment=Qt.AlignmentFlag.AlignCenter
        )

        layout.addWidget(QLabel("Title"))
        self.title_label = QLabel()

        layout.addWidget(self.title_label)

        layout.addWidget(QLabel("Author"))
        self.author_label = QLabel()

        layout.addWidget(self.author_label)

        layout.addWidget(QLabel("Publisher"))
        self.publisher_label = QLabel()

        layout.addWidget(self.publisher_label)

        layout.addWidget(QLabel("Year"))
        self.year_label = QLabel()

        layout.addWidget(self.year_label)

        layout.addWidget(QLabel("Pages"))
        self.pages_label = QLabel()

        layout.addWidget(self.pages_label)

        layout.addWidget(QLabel("Genre"))
        self.genre_label = QLabel()

        layout.addWidget(self.genre_label)

        layout.addWidget(QLabel("Description"))

        self.description = QTextEdit()
        self.description.setReadOnly(True)

        layout.addWidget(
            self.description,
            1,
        )

        return panel

    def clear_preview(self):

        self.cover_label.clear()
        self.cover_label.setText("No Cover")

        self.title_label.setText("-")
        self.author_label.setText("-")
        self.publisher_label.setText("-")
        self.year_label.setText("-")
        self.pages_label.setText("-")
        self.genre_label.setText("-")

        self.description.clear()

    def load_cover(
        self,
        url,
    ):

        self.thumbnail_loader.load(
            url
        )

    def update_preview(self):

        book = self.selected_book()

        if book is None:

            self.clear_preview()

            return

        self.title_label.setText(
            book.title or "-"
        )

        self.author_label.setText(
            ", ".join(book.authors) or "-"
        )

        self.publisher_label.setText(
            book.publisher or "-"
        )

        self.year_label.setText(
            str(book.published_year or "-")
        )

        self.pages_label.setText(
            str(book.page_count or "-")
        )

        self.genre_label.setText(
            book.genre or "-"
        )

        self.description.setPlainText(
            book.description or ""
        )

        self.load_cover(
            book.thumbnail
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
            self.on_selection_changed
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

        self.clear_preview()

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

        if self.results.count():

            self.results.setCurrentRow(0)

    def import_selected(self):

        google_book = self.selected_book()

        if google_book is None:
            return

        duplicate = BookService.find_duplicate(
            google_book
        )

        if duplicate:

            QMessageBox.information(
                self,
                "Duplicate Book",
                "This book already exists in your library."
            )

            return

        BookService.create_from_google_book(
            google_book
        )

        self.accept()

    def update_buttons(self):

        self.import_button.setEnabled(
            self.results.currentRow() >= 0
        )

    def on_selection_changed(self):

        self.update_buttons()

        self.update_preview()

    def selected_book(self):

        item = self.results.currentItem()

        if item is None:
            return None

        return item.data(
            Qt.ItemDataRole.UserRole
        )

    def on_thumbnail_loaded(
        self,
        pixmap,
    ):

        pixmap = pixmap.scaled(

            self.cover_label.size(),

            Qt.AspectRatioMode.KeepAspectRatio,

            Qt.TransformationMode.SmoothTransformation,

        )

        self.cover_label.setPixmap(
            pixmap
        )

    def on_thumbnail_failed(self):

        self.cover_label.clear()

        self.cover_label.setText(
            "No Cover"
        ) 