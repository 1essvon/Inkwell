from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton,
)

from app.services.book_service import BookService


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
            author=author
        )

        self.accept()