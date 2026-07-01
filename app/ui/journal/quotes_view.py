from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QPushButton,
    QListWidget,
    QLabel,
    QComboBox,
    QListWidgetItem,
    QHBoxLayout,
    QMessageBox,
    QScrollArea
)

from app.services.book_service import (
    BookService
)

from app.services.quote_service import (
    QuoteService
)

from app.ui.dialogs.add_quote_dialog import (
    AddQuoteDialog
)

from app.ui.journal.quote_detail_view import (
    QuoteDetailView
)


class QuotesView(QWidget):

    def __init__(self):

        super().__init__()

        self.selected_quote = None

        root_layout = QVBoxLayout()

        scroll = QScrollArea()

        scroll.setWidgetResizable(True)

        content = QWidget()

        layout = QVBoxLayout()

        content.setLayout(
            layout
        )

        scroll.setWidget(
            content
        )

        root_layout.addWidget(
            scroll
        )

        layout.addWidget(
            QLabel("Book")
        )

        self.book_filter = QComboBox()

        layout.addWidget(
            self.book_filter
        )

        self.add_quote_button = QPushButton(
            "Add Quote"
        )

        self.delete_quote_button = QPushButton(
            "Delete Quote"
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

        self.quote_list = QListWidget()

        self.detail_view = QuoteDetailView()

        content_layout = QHBoxLayout()

        content_layout.addWidget(
            self.quote_list,
            1
        )

        content_layout.addWidget(
            self.detail_view,
            3
        )

        layout.addLayout(
            content_layout
        )

        self.setLayout(
            root_layout
        )

        self.add_quote_button.clicked.connect(
            self.open_add_quote_dialog
        )

        self.delete_quote_button.clicked.connect(
            self.delete_selected_quote
        )

        self.quote_list.itemClicked.connect(
            self.show_quote_details
        )

        self.book_filter.currentIndexChanged.connect(
            self.load_quotes
        )

        self.load_books()

        self.load_quotes()

    def load_books(self):

        self.book_filter.clear()

        self.book_filter.addItem(
            "All Books",
            None
        )

        books = BookService.get_all_books()

        for book in books:

            self.book_filter.addItem(

                book.title,

                book.id

            )

    def load_quotes(self):

        self.quote_list.clear()

        book_id = self.book_filter.currentData()

        if book_id is None:

            quotes = QuoteService.get_all_quotes()

        else:

            quotes = QuoteService.get_quotes_for_book(
                book_id
            )

        for quote in quotes:

            text = (
                f"Page {quote.page}"
            )

            item = QListWidgetItem(
                text
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

        book_id = self.book_filter.currentData()

        if book_id is None:

            return

        dialog = AddQuoteDialog(
            book_id
        )

        if dialog.exec():

            self.load_quotes()

    def show_quote_details(
        self,
        item
    ):

        quote = QuoteService.get_quote(

            item.data(1)

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