from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QVBoxLayout

from app.models.book import Book

from app.ui.widgets.book_detail_card import (
    BookDetailCard
)


class BookDetailView(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.card = BookDetailCard()

        layout.addWidget(self.card)

        self.setLayout(layout)

    def display_book(self, book: Book):
        self.card.set_book(book)

    def clear(self):
        self.card.clear()