from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QTextEdit,
    QVBoxLayout
)


class QuoteDetailView(QWidget):

    def __init__(self):

        super().__init__()

        layout = QVBoxLayout()

        self.page_label = QLabel()

        self.content = QTextEdit()

        self.content.setReadOnly(True)

        layout.addWidget(
            self.page_label
        )

        layout.addWidget(
            self.content
        )

        self.setLayout(
            layout
        )

        self.clear()

    def display_quote(
        self,
        quote
    ):

        self.page_label.setText(
            f"Page {quote.page}"
        )

        self.content.setPlainText(
            quote.content
        )

        self.current_quote = quote

    def clear(self):

        self.page_label.setText(
            "No Quote Selected"
        )

        self.content.clear()

        self.current_quote = None