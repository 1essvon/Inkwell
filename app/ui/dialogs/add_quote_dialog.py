from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QLineEdit,
    QSpinBox,
    QPushButton
)

from app.services.quote_service import QuoteService


class AddQuoteDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add Quote")

        layout = QVBoxLayout()

        layout.addWidget(
            QLabel("Quote")
        )

        self.quote_input = QTextEdit()

        layout.addWidget(
            self.quote_input
        )

        layout.addWidget(
            QLabel("Source")
        )

        self.source_input = QLineEdit()

        layout.addWidget(
            self.source_input
        )

        layout.addWidget(
            QLabel("Page Number")
        )

        self.page_input = QSpinBox()

        self.page_input.setMaximum(
            100000
        )

        layout.addWidget(
            self.page_input
        )

        save_button = QPushButton(
            "Save"
        )

        save_button.clicked.connect(
            self.save_quote
        )

        layout.addWidget(
            save_button
        )

        self.setLayout(layout)

    def save_quote(self):

        quote_text = (
            self.quote_input
            .toPlainText()
            .strip()
        )

        if not quote_text:
            return

        QuoteService.create_quote(
            quote_text=quote_text,
            source=self.source_input.text(),
            page_number=self.page_input.value()
        )

        self.accept()