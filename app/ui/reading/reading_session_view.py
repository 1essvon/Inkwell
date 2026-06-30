"""
File:
    reading_session_view.py

Purpose:
    Halaman sesi membaca.

Responsibilities:
    - Menampilkan buku yang sedang dibaca
    - Update current page
    - Membuat catatan
    - Menyimpan quote

Does NOT:
    - Mengakses database langsung
"""

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSplitter
)

from app.services.book_service import (
    BookService
)

from app.ui.reading.reading_book_list_widget import (
    ReadingBookListWidget
)

from app.ui.reading.reading_detail_widget import (
    ReadingDetailWidget
)

class ReadingSessionView(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.setup_connections()

        self.refresh()
        

    def setup_ui(self):

        layout = QVBoxLayout()

        self.book_list = ReadingBookListWidget()

        self.detail = ReadingDetailWidget()

        self.splitter = QSplitter(
            Qt.Horizontal
        )

        self.splitter.setChildrenCollapsible(False)

        self.splitter.addWidget(
            self.book_list
        )

        self.splitter.addWidget(
            self.detail
        )

        self.splitter.setStretchFactor(
            0,
            1
        )

        self.splitter.setStretchFactor(
            1,
            2
        )

        self.splitter.setSizes([
            280,
            700
        ])

        layout.addWidget(
            self.splitter
        )

        self.setLayout(
            layout
        )

    def refresh(self):

        self.book_list.refresh()

    def setup_connections(self):

        self.plus_one.clicked.connect(
            lambda: self.add_pages(1)
        )

        self.plus_five.clicked.connect(
            lambda: self.add_pages(5)
        )

        self.plus_ten.clicked.connect(
            lambda: self.add_pages(10)
        ) 

    def add_pages(
        self,
        amount
    ):

        if not self.book:

            return

        current = self.book.current_page or 0

        total = self.book.page_count or 0

        new_page = min(
            current + amount,
            total
        )

        BookService.update_current_page(

            self.book.id,

            new_page

        )

        self.refresh()

    def setup_connections(self):

        self.book_list.bookSelected.connect(

            self.on_book_selected

        )

        self.detail.progressUpdated.connect(

            self.refresh_list

        )

    def on_book_selected(
        self,
        book
    ):

        self.detail.set_book(
            book
        )

    def refresh_list(self):

        if self.detail.book:

            selected_id = self.detail.book.id

        else:

            selected_id = None

        self.book_list.refresh(

            selected_id=selected_id

        )