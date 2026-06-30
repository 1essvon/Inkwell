"""
File:
    reading_book_list_widget.py

Purpose:
    Menampilkan daftar buku yang sedang dibaca.

Responsibilities:
    - Menampilkan ReadingBookCard
    - Memilih buku
    - Mengirim signal saat buku dipilih

Does NOT:
    - Mengontrol progress
    - Mengubah database
"""

from PySide6.QtCore import Signal

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListWidget,
    QListWidgetItem
)

from app.services.book_service import (
    BookService
)

from app.ui.reading.reading_book_card import (
    ReadingBookCard
)

class ReadingBookListWidget(QWidget):

    bookSelected = Signal(object)

    # ----------------------------------
    # Initialization
    # ----------------------------------

    def __init__(self):
        super().__init__()

        self.setup_ui()

        self.setup_connections()

        self.refresh()

    def setup_ui(self):

        layout = QVBoxLayout()

        self.list_widget = QListWidget()

        layout.addWidget(
            self.list_widget
        )

        self.setLayout(
            layout
        )

    def setup_connections(self):

        self.list_widget.itemClicked.connect(
            self.on_item_clicked
        )

    def refresh(
        self,
        selected_id=None
    ):

        self.list_widget.clear()

        books = BookService.get_reading_books()

        for book in books:

            item = self.add_book(book)

            if (
                selected_id is not None
                and
                book.id == selected_id
            ):

                self.list_widget.setCurrentItem(
                    item
                )

    def add_book(
        self,
        book
    ):

        card = ReadingBookCard(
            book
        )

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

        return item

    def current_book(self):

        item = self.list_widget.currentItem()

        if item is None:

            return None

        return BookService.get_book(
            item.data(1)
        )
    
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