from PySide6.QtWidgets import QWidget
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QVBoxLayout

from app.models.book import Book


class BookDetailCard(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.title_label = QLabel("No Book Selected")
        self.author_label = QLabel("")
        self.status_label = QLabel("")
        self.page_label = QLabel("")
        self.isbn_label = QLabel("")
        self.publisher_label = QLabel("")
        self.genre_label = QLabel("")
        self.rating_label = QLabel("")

        self.title_label.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
        """)

        layout.addWidget(self.title_label)
        layout.addWidget(self.author_label)

        layout.addSpacing(10)

        layout.addWidget(self.isbn_label)
        layout.addWidget(self.publisher_label)
        layout.addWidget(self.genre_label)

        layout.addWidget(self.status_label)
        layout.addWidget(self.page_label)

        layout.addWidget(self.rating_label)

        self.setLayout(layout)

    def set_book(self, book: Book):

        self.title_label.setText(book.title)

        self.author_label.setText(book.author)

        self.isbn_label.setText(
            f"ISBN: {book.isbn or '-'}"
        )

        self.publisher_label.setText(
            f"Publisher: {book.publisher or '-'}"
        )

        self.genre_label.setText(
            f"Genre: {book.genre or '-'}"
        )

        self.status_label.setText(
            f"Status: {book.status}"
        )

        self.page_label.setText(
            f"Current Page: {book.current_page}"
        )

        self.rating_label.setText(
            f"Rating: {book.rating or '-'}"
        )

    def clear(self):

        self.title_label.setText(
            "No Book Selected"
        )

        self.author_label.setText("")
        self.status_label.setText("")
        self.page_label.setText("")

        self.isbn_label.setText("")
        self.publisher_label.setText("")
        self.genre_label.setText("")
        self.rating_label.setText("")