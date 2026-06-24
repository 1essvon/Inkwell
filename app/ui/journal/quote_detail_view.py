from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout
)


class QuoteDetailView(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.quote_label = QLabel(
            "No Quote Selected"
        )

        self.quote_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
        """)

        self.source_label = QLabel("")

        self.page_label = QLabel("")

        self.quote_label.setWordWrap(
            True
        )

        layout.addWidget(
            self.quote_label
        )

        layout.addWidget(
            self.source_label
        )

        layout.addWidget(
            self.page_label
        )

        self.setLayout(layout)

    def display_quote(self, quote):

        self.quote_label.setText(
            quote.quote_text
        )

        self.source_label.setText(
            f"Source: {quote.source or '-'}"
        )

        self.page_label.setText(
            f"Page: {quote.page_number or '-'}"
        )

    def clear(self):

        self.quote_label.setText(
            "No Quote Selected"
        )

        self.source_label.setText("")
        self.page_label.setText("")