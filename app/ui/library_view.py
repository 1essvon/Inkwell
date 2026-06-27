from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QMessageBox
)

from app.ui.components.book_card import BookCard
from app.ui.book_detail_view import BookDetailView

from app.ui.dialogs.add_book_dialog import AddBookDialog
from app.ui.dialogs.edit_book_dialog import EditBookDialog

from app.services.book_service import BookService


class LibraryView(QWidget):

    def __init__(self):
        super().__init__()

        self.selected_book = None

        root_layout = QVBoxLayout()

        # ======================
        # Title
        # ======================

        title = QLabel("Library")

        title.setObjectName(
            "pageTitle"
        )

        root_layout.addWidget(
            title
        )

        # ======================
        # Toolbar
        # ======================

        toolbar = QHBoxLayout()

        self.add_book_button = QPushButton(
            "Add Book"
        )

        self.edit_button = QPushButton(
            "Edit Book"
        )

        self.delete_button = QPushButton(
            "Delete Book"
        )

        toolbar.addWidget(
            self.add_book_button
        )

        toolbar.addWidget(
            self.edit_button
        )

        toolbar.addWidget(
            self.delete_button
        )

        toolbar.addStretch()

        root_layout.addLayout(
            toolbar
        )

        root_layout.addSpacing(
            12
        )

        # ======================
        # Book List
        # ======================

        self.book_list = QListWidget()

        self.book_list.setSpacing(
            10
        )

        root_layout.addWidget(
            self.book_list,
            2
        )

        # ======================
        # Detail
        # ======================

        self.detail_view = BookDetailView()

        root_layout.addWidget(
            self.detail_view,
            1
        )

        self.setLayout(
            root_layout
        )

        # ======================
        # Events
        # ======================

        self.add_book_button.clicked.connect(
            self.open_add_book_dialog
        )

        self.edit_button.clicked.connect(
            self.open_edit_dialog
        )

        self.delete_button.clicked.connect(
            self.delete_selected_book
        )

        self.book_list.itemClicked.connect(
            self.show_book_details
        )

        self.refresh()

    # ==========================
    # Data
    # ==========================

    def load_books(self):

        self.book_list.clear()

        books = BookService.get_all_books()

        for book in books:

            widget = BookCard(
                book
            )

            item = QListWidgetItem()

            item.setSizeHint(
                widget.sizeHint()
            )

            item.setData(
                1,
                book.id
            )

            self.book_list.addItem(
                item
            )

            self.book_list.setItemWidget(
                item,
                widget
            )

    def refresh(self):

        self.load_books()

        if self.selected_book:

            refreshed = BookService.get_book(
                self.selected_book.id
            )

            if refreshed:

                self.selected_book = refreshed

                self.detail_view.display_book(
                    refreshed
                )

    # ==========================
    # Events
    # ==========================

    def show_book_details(self, item):

        book = BookService.get_book(
            item.data(1)
        )

        if book:

            self.selected_book = book

            self.detail_view.display_book(
                book
            )

    def open_add_book_dialog(self):

        dialog = AddBookDialog()

        if dialog.exec():

            self.refresh()

    def open_edit_dialog(self):

        if not self.selected_book:

            return

        dialog = EditBookDialog(
            self.selected_book
        )

        if dialog.exec():

            self.refresh()

    def delete_selected_book(self):

        if not self.selected_book:

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