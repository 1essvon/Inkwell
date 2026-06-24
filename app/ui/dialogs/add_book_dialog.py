from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)

from app.services.book_service import BookService
from PySide6.QtWidgets import QSpinBox


class AddBookDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add Book")

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Title"))

        self.title_input = QLineEdit()
        layout.addWidget(self.title_input)

        layout.addWidget(QLabel("Author"))

        self.author_input = QLineEdit()
        layout.addWidget(self.author_input)

        layout.addWidget(QLabel("ISBN"))

        self.isbn_input = QLineEdit()
        layout.addWidget(self.isbn_input)

        layout.addWidget(QLabel("Publisher"))

        self.publisher_input = QLineEdit()
        layout.addWidget(self.publisher_input)

        layout.addWidget(QLabel("Genre"))

        self.genre_input = QLineEdit()
        layout.addWidget(self.genre_input)

        layout.addWidget(QLabel("Page Count"))

        self.page_count_input = QSpinBox()
        self.page_count_input.setMaximum(100000)

        layout.addWidget(self.page_count_input)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_book)

        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_book(self):

        title = self.title_input.text().strip()
        author = self.author_input.text().strip()

        if not title:
            return

        BookService.create_book(
            title=title,
            author=author,
            isbn=self.isbn_input.text().strip(),
            publisher=self.publisher_input.text().strip(),
            genre=self.genre_input.text().strip(),
            page_count=self.page_count_input.value()
        )

        self.accept()