"""
File:
    library_view.py

Purpose:
    Halaman utama Library.

Responsibilities:
    - Menyusun layout
    - Menghubungkan widget
    - Membuka dialog
    - Menghapus buku

Does NOT:
    - Membuat BookCard
    - Menampilkan detail buku
    - Mengelola QListWidget
"""

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
    QSplitter
)

from app.services.book_service import BookService

from app.ui.library.book_list_widget import (
    BookListWidget
)

from app.ui.library.book_detail_widget import (
    BookDetailWidget
)

from app.ui.dialogs.add_book_dialog import (
    AddBookDialog
)

from app.ui.dialogs.edit_book_dialog import (
    EditBookDialog
)


class LibraryView(QWidget):

    # ----------------------------------
    # Initialization
    # ----------------------------------

    def __init__(self):
        super().__init__()

        self.selected_book = None

        self.setup_ui()

        self.setup_connections()

        self.refresh()

    # ----------------------------------
    # UI
    # ----------------------------------

    def setup_ui(self):

        layout = QVBoxLayout()

        title = QLabel("Library")

        title.setObjectName(
            "pageTitle"
        )

        layout.addWidget(title)

        toolbar = QHBoxLayout()

        self.add_button = QPushButton(
            "Add Book"
        )

        self.edit_button = QPushButton(
            "Edit Book"
        )

        self.delete_button = QPushButton(
            "Delete Book"
        )

        toolbar.addWidget(
            self.add_button
        )

        toolbar.addWidget(
            self.edit_button
        )

        toolbar.addWidget(
            self.delete_button
        )

        toolbar.addStretch()

        layout.addLayout(
            toolbar
        )

        layout.addSpacing(
            12
        )

        self.book_list = BookListWidget()

        self.detail_view = BookDetailWidget()

        self.splitter = QSplitter(
            Qt.Horizontal
        )

        self.splitter.setChildrenCollapsible(False)

        self.splitter.setStretchFactor(0, 1)

        self.splitter.setStretchFactor(1, 1)

        self.splitter.addWidget(
            self.book_list
        )

        self.splitter.addWidget(
            self.detail_view
        )

        self.splitter.setSizes([
            450,
            650
        ])

        layout.addWidget(
            self.splitter,
            1
        )

        self.setLayout(
            layout
        )

    # ----------------------------------
    # Connections
    # ----------------------------------

    def setup_connections(self):

        self.add_button.clicked.connect(
            self.open_add_book_dialog
        )

        self.edit_button.clicked.connect(
            self.open_edit_dialog
        )

        self.delete_button.clicked.connect(
            self.delete_selected_book
        )

        self.book_list.bookSelected.connect(
            self.on_book_selected
        )

    # ----------------------------------
    # Events
    # ----------------------------------

    def on_book_selected(
        self,
        book
    ):
        """
        Dipanggil saat user
        memilih sebuah buku.
        """

        self.selected_book = book

        self.detail_view.set_book(
            book
        )

    # ----------------------------------
    # Data
    # ----------------------------------

    def refresh(self):

        self.book_list.refresh()

        if self.selected_book:

            refreshed = BookService.get_book(
                self.selected_book.id
            )

            if refreshed:

                self.selected_book = refreshed

                self.detail_view.set_book(
                    refreshed
                )

    # ----------------------------------
    # Dialog
    # ----------------------------------

    def open_add_book_dialog(self):

        dialog = AddBookDialog()

        if dialog.exec():

            self.refresh()

    def open_edit_dialog(self):

        if self.selected_book is None:

            return

        dialog = EditBookDialog(
            self.selected_book
        )

        if dialog.exec():

            self.refresh()

    # ----------------------------------
    # Delete
    # ----------------------------------

    def delete_selected_book(self):

        if self.selected_book is None:

            return

        reply = QMessageBox.question(
            self,
            "Delete Book",
            f'Delete "{self.selected_book.title}"?',
            QMessageBox.Yes | QMessageBox.No
        )

        if reply != QMessageBox.Yes:

            return

        BookService.delete_book(
            self.selected_book.id
        )

        self.selected_book = None

        self.detail_view.clear()

        self.refresh()