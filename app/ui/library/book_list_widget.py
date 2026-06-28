"""
File:
    book_list_widget.py

Purpose:
    Menampilkan daftar buku pada Library.

Responsibilities:
    - Menampilkan BookCard
    - Mengelola QListWidget
    - Mengirim signal saat buku dipilih

Does NOT:
    - Menampilkan detail buku
    - Membuka dialog
    - Menghapus data
"""

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListWidget,
    QListWidgetItem,
    QSizePolicy
)

from app.services.book_service import BookService
from app.ui.components.book_card import BookCard


class BookListWidget(QWidget):

    bookSelected = Signal(object)

    # ----------------------------------
    # Initialization
    # ----------------------------------

    def __init__(self):
        super().__init__()

        self.setup_ui()

    # ----------------------------------
    # UI
    # ----------------------------------

    def setup_ui(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(
            0, 0, 0, 0
        )

        layout.setSpacing(0)

        self.list_widget = QListWidget()

        self.list_widget.setSpacing(10)

        self.list_widget.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        self.list_widget.itemClicked.connect(
            self.on_item_clicked
        )

        layout.addWidget(
            self.list_widget
        )

        self.setLayout(
            layout
        )

        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

    # ----------------------------------
    # Data
    # ----------------------------------

    def refresh(self):

        self.list_widget.clear()

        books = BookService.get_all_books()

        for book in books:

            self.add_book(book)

    def add_book(
        self,
        book
    ):

        card = BookCard(book)

        item = QListWidgetItem()

        item.setSizeHint(
            card.sizeHint()
        )

        item.setData(
            1,
            book.id
        )

        self.list_widget.addItem(
            item
        )

        self.list_widget.setItemWidget(
            item,
            card
        )

    def current_book(self):

        item = self.list_widget.currentItem()

        if item is None:

            return None

        return BookService.get_book(
            item.data(1)
        )

    # ----------------------------------
    # Events
    # ----------------------------------

    def on_item_clicked(
        self,
        item
    ):

        book = BookService.get_book(
            item.data(1)
        )

        self.bookSelected.emit(
            book
        )