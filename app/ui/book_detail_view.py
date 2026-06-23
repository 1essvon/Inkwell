from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QVBoxLayout

from app.models.book import Book


class BookDetailView(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.title_label = QLabel("Title:")
        self.author_label = QLabel("Author:")
        self.status_label = QLabel("Status:")
        self.page_label = QLabel("Current Page:")

        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.author_label)
        self.layout.addWidget(self.status_label)
        self.layout.addWidget(self.page_label)

        self.setLayout(self.layout)

    def display_book(self, book: Book):
        self.title_label.setText(f"Title: {book.title}")
        self.author_label.setText(f"Author: {book.author}")
        self.status_label.setText(f"Status: {book.status}")
        self.page_label.setText(
            f"Current Page: {book.current_page}"
        )