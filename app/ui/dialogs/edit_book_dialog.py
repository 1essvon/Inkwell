from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout
)

from app.services.book_service import BookService


class EditBookDialog(QDialog):

    def __init__(self, book):
        super().__init__()

        self.book = book

        self.setWindowTitle("Edit Book")

        layout = QVBoxLayout()

        layout.addWidget(QLabel("Title"))

        self.title_input = QLineEdit(book.title)
        layout.addWidget(self.title_input)

        layout.addWidget(QLabel("Author"))

        self.author_input = QLineEdit(book.author)
        layout.addWidget(self.author_input)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_book)

        layout.addWidget(save_button)

        self.setLayout(layout)

    def save_book(self):
        BookService.update_book(
            self.book.id,
            self.title_input.text(),
            self.author_input.text()
        )

        self.accept()