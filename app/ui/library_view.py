from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QListWidget
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtWidgets import QMessageBox

from app.ui.components.book_card import (
    BookCard
)
from app.ui.dialogs.add_book_dialog import AddBookDialog
from app.ui.book_detail_view import BookDetailView
from app.services.book_service import BookService
from app.ui.dialogs.edit_book_dialog import EditBookDialog



class LibraryView(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.add_book_button = QPushButton("Add Book")

        self.add_book_button.clicked.connect(
            self.open_add_book_dialog
        )

        self.layout.addWidget(self.add_book_button)

        self.selected_book = None

        self.edit_button = QPushButton("Edit Book")

        self.edit_button.clicked.connect(
            self.open_edit_dialog
        )

        self.layout.addWidget(self.edit_button)

        self.delete_button = QPushButton(
            "Delete Book"
        )

        self.delete_button.clicked.connect(
            self.delete_selected_book
        )

        self.layout.addWidget(
            self.delete_button
        )

        self.book_list = QListWidget()

        self.layout.addWidget(self.book_list)

        self.setLayout(self.layout)

        self.refresh()

        self.detail_view = BookDetailView()

        self.layout.addWidget(self.detail_view)

        self.book_list.itemClicked.connect(
            self.show_book_details
)

    def load_books(self):
        books = BookService.get_all_books()

        self.book_list.clear()

        for book in books:
            progress = f"{book.current_page or 0} / {book.page_count or 0}"

            item = QListWidgetItem()

            widget = BookCard(
                book.title,
                book.author,
                progress
            )

            item.setSizeHint(
                widget.sizeHint()
            )

            item.setData(
                1,
                book.id
            )

            self.book_list.addItem(item)

            self.book_list.setItemWidget(
                item,
                widget
            )

    def open_add_book_dialog(self):
        dialog = AddBookDialog()

        if dialog.exec():
            self.refresh()

    def show_book_details(self, item):
        book_id = item.data(1)

        book = BookService.get_book(book_id)

        if book:
            self.selected_book = book
            self.detail_view.display_book(book)

    def open_edit_dialog(self):

        if not self.selected_book:
            return

        dialog = EditBookDialog(
            self.selected_book
        )

        if dialog.exec():

            self.refresh()

            refreshed_book = BookService.get_book(
                self.selected_book.id
            )

            self.selected_book = refreshed_book

            self.detail_view.display_book(
                refreshed_book
            )

    def delete_selected_book(self):

        if not self.selected_book:
            return

        reply = QMessageBox.question(
            self,
            "Delete Book",
            f'Delete "{self.selected_book.title}"?',
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:

            BookService.delete_book(
                self.selected_book.id
            )

            self.selected_book = None

            self.refresh()

            self.detail_view.clear()

    def refresh(self):

        self.load_books()

        if not self.selected_book:
            return

        refreshed = BookService.get_book(
            self.selected_book.id
        )

        if refreshed:

            self.selected_book = refreshed

            self.detail_view.display_book(
                refreshed
            )