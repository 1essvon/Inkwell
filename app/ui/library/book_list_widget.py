"""
File:
    book_list_widget.py

Purpose:
    Menampilkan daftar buku pada halaman Library.

Responsibilities:
    - Mengambil daftar buku dari BookService
    - Menampilkan BookCard
    - Mengelola item yang dipilih

Does NOT:
    - Mengedit database
    - Membuka dialog
    - Menampilkan detail buku
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea
)

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListWidget,
    QListWidgetItem
)

from app.models import book
from app.services.book_service import BookService

from app.ui.components.book_card import BookCard

from app.services.book_service import BookService

from app.ui.components.book_card import BookCard


class BookListWidget(QWidget):
    """
    Widget yang menampilkan seluruh daftar buku.

    Widget ini hanya bertanggung jawab
    terhadap list buku.
    """

    def __init__(self):
        """
        Dipanggil sekali
        saat widget dibuat.
        """

        super().__init__()

        self.setup_ui()

        self.refresh()

    # ----------------------------------
    # UI
    # ----------------------------------

    def setup_ui(self):
        """
        Membuat seluruh layout.
        """

        self.layout = QVBoxLayout()

        self.list_widget = QListWidget()

        self.list_widget.setSpacing(
            10
        )

        self.layout.addWidget(
            self.list_widget
        )

        self.setLayout(
            self.layout
        )

    # ----------------------------------
    # Helpers
    # ----------------------------------

    def clear(self):
        """
        Menghapus seluruh item.
        """

        self.list_widget.clear()

    # ----------------------------------
    # Data
    # ----------------------------------

    def refresh(self):
        """
        Akan diisi pada sprint berikutnya.

        Tugas:
        - hapus seluruh BookCard
        - ambil data dari BookService
        - tampilkan ulang BookCard
        """

        self.clear()

        books = BookService.get_all_books()

        for book in books:

            self.add_book(book)

    def current_book(self):
        """
        Mengembalikan buku
        yang sedang dipilih.

        """

        item = self.list_widget.currentItem()

        if item is None:

            return None

        return BookService.get_book(
            item.data(1)
        )
    
    @property
    def list(self):
        """
        Mengembalikan QListWidget internal.
        """

        return self.list_widget
    
    def add_book(
        self,
        book
    ):
        """
        Membuat satu BookCard
        lalu memasukkannya
        ke daftar.
        """

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