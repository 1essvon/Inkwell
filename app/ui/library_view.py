from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QListWidget
from PySide6.QtWidgets import QPushButton
from app.ui.dialogs.add_book_dialog import AddBookDialog

from app.services.book_service import BookService


class LibraryView(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.add_book_button = QPushButton("Add Book")

        self.add_book_button.clicked.connect(
            self.open_add_book_dialog
        )

        self.layout.addWidget(self.add_book_button)

        self.book_list = QListWidget()

        self.layout.addWidget(self.book_list)

        self.setLayout(self.layout)

        self.load_books()

    def load_books(self):
        books = BookService.get_all_books()

        self.book_list.clear()

        for book in books:
            self.book_list.addItem(book.title)

    def open_add_book_dialog(self):
        dialog = AddBookDialog()

        if dialog.exec():
            self.load_books()