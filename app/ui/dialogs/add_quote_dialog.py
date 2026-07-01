from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QTextEdit,
    QPushButton,
    QSpinBox,
    QVBoxLayout
)

from app.services.quote_service import (
    QuoteService
)


class AddQuoteDialog(QDialog):

    def __init__(
        self,
        book_id
    ):

        super().__init__()

        self.book_id = book_id

        self.setWindowTitle(
            "Add Quote"
        )

        layout = QVBoxLayout()

        layout.addWidget(
            QLabel("Quote")
        )

        self.quote_input = QTextEdit()

        self.quote_input.setPlaceholderText(
            "Enter quote..."
        )

        layout.addWidget(
            self.quote_input
        )

        layout.addWidget(
            QLabel("Page")
        )

        self.page_input = QSpinBox()

        self.page_input.setMinimum(1)

        layout.addWidget(
            self.page_input
        )

        self.save_button = QPushButton(
            "Save"
        )

        self.save_button.clicked.connect(
            self.save_quote
        )

        layout.addWidget(
            self.save_button
        )

        self.setLayout(
            layout
        )

    def save_quote(self):

        content = (
            self.quote_input
            .toPlainText()
            .strip()
        )

        if not content:

            return

        QuoteService.create_quote(

            book_id=self.book_id,

            content=content,

            page=self.page_input.value()

        )

        self.accept()