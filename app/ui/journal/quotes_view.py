from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QListWidget
)
from PySide6.QtWidgets import QListWidgetItem
from PySide6.QtWidgets import QHBoxLayout
from PySide6.QtWidgets import QMessageBox

from app.ui.dialogs.add_quote_dialog import (
    AddQuoteDialog
)

from app.services.quote_service import (
    QuoteService
)

from app.ui.journal.quote_detail_view import (
    QuoteDetailView
)


class QuotesView(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.add_quote_button = QPushButton(
            "Add Quote"
        )

        self.delete_quote_button = QPushButton(
            "Delete Quote"
        )

        self.delete_quote_button.clicked.connect(
            self.delete_selected_quote
        )

        self.add_quote_button.clicked.connect(
            self.open_add_quote_dialog
        )

        self.quote_list = QListWidget()

        self.selected_quote = None

        self.detail_view = QuoteDetailView()

        self.quote_list.itemClicked.connect(
            self.show_quote_details
        )

        button_layout = QHBoxLayout()

        button_layout.addWidget(
            self.add_quote_button
        )

        button_layout.addWidget(
            self.delete_quote_button
        )

        layout.addLayout(
            button_layout
        )

        content_layout = QHBoxLayout()

        content_layout.addWidget(
            self.quote_list,
            2
        )

        content_layout.addWidget(
            self.detail_view,
            3
        )

        layout.addLayout(
            content_layout
        )

        self.load_quotes()

        self.setLayout(layout)

    def load_quotes(self):

        self.quote_list.clear()

        quotes = QuoteService.get_all_quotes()

        for quote in quotes:

            preview = quote.quote_text.split("\n")[0][:80]

            item = QListWidgetItem(
                preview
            )

            item.setData(
                1,
                quote.id
            )

            self.quote_list.addItem(
                item
            )

        if quotes:

            self.selected_quote = quotes[0]

            self.detail_view.display_quote(
                quotes[0]
            )

        else:

            self.selected_quote = None

            self.detail_view.clear()

    def open_add_quote_dialog(self):

        dialog = AddQuoteDialog()

        if dialog.exec():
            self.load_quotes()

    def show_quote_details(self, item):

        quote_id = item.data(1)

        quote = QuoteService.get_quote(
            quote_id
        )

        if quote:

            self.selected_quote = quote

            self.detail_view.display_quote(
                quote
            )

    def delete_selected_quote(self):

        if not self.selected_quote:
            return

        reply = QMessageBox.question(
            self,
            "Delete Quote",
            "Delete selected quote?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:

            QuoteService.delete_quote(
                self.selected_quote.id
            )

            self.selected_quote = None

            self.load_quotes()

            self.detail_view.clear()