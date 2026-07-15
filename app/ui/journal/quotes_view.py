from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QSplitter,
    QComboBox,
    QPushButton,
)

from app.services.book_service import (
    BookService,
)

from app.services.quote_service import (
    QuoteService,
)

from app.ui.components.empty_state import (
    EmptyState,
)

from app.ui.components.page_header import (
    PageHeader,
)

from app.ui.components.search_bar import (
    SearchBar,
)

from app.ui.components.toolbar import (
    Toolbar,
)

from app.ui.dialogs.add_quote_dialog import (
    AddQuoteDialog,
)

from app.ui.journal.quote_list_widget import (
    QuoteListWidget,
)

from app.ui.journal.quote_detail_view import (
    QuoteDetailView,
)

class QuotesView(QWidget):

    def __init__(self):

        super().__init__()

        self.selected_quote = None

        self.setup_ui()

        self.connect_signals()

        self.refresh()

    def setup_ui(self):

        self.root_layout = QVBoxLayout(self)

        self.root_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(
            True
        )

        self.content = QWidget()

        self.content_layout = QVBoxLayout()

        self.content_layout.setSpacing(
            20
        )

        self.content.setLayout(
            self.content_layout
        )

        self.scroll.setWidget(
            self.content
        )

        self.root_layout.addWidget(
            self.scroll
        )

        self.header = PageHeader(
            "Quotes"
        )

        self.content_layout.addWidget(
            self.header
        )

        self.toolbar = Toolbar()

        self.search = SearchBar(
            "Search quotes..."
        )

        self.book_filter = QComboBox()

        self.sort_filter = QComboBox()

        self.sort_filter.addItems(

            [

                "Newest",

                "Oldest",

                "Page",

            ]

        )

        self.add_quote_button = QPushButton(
            "Add Quote"
        )

        self.toolbar.add_widget(
            self.search
        )

        self.toolbar.add_widget(
            self.book_filter
        )

        self.toolbar.add_widget(
            self.sort_filter
        )

        self.toolbar.add_stretch()

        self.toolbar.add_widget(
            self.add_quote_button
        )

        self.content_layout.addWidget(
            self.toolbar
        )

        self.splitter = QSplitter()

        self.quote_list = QuoteListWidget()

        self.detail_view = QuoteDetailView()

        self.empty_state = EmptyState(

            icon="❝",

            title="No Quotes Yet",

            subtitle=(
                "Save memorable passages\n"
                "from the books you read."
            )

        )

        self.empty_state.hide()

        self.left_panel = QWidget()

        self.left_layout = QVBoxLayout()

        self.left_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self.left_layout.addWidget(
            self.empty_state
        )

        self.left_layout.addWidget(
            self.quote_list
        )

        self.left_panel.setLayout(
            self.left_layout
        )

        self.splitter.addWidget(
            self.left_panel
        )

        self.splitter.addWidget(
            self.detail_view
        )

        self.splitter.setStretchFactor(
            0,
            2,
        )

        self.splitter.setStretchFactor(
            1,
            3,
        )

        self.content_layout.addWidget(
            self.splitter
        )

    def connect_signals(self):

        self.add_quote_button.clicked.connect(
            self.open_add_quote_dialog
        )

        self.book_filter.currentIndexChanged.connect(
            self.load_quotes
        )

        self.quote_list.quote_selected.connect(
            self.show_quote
        )

        self.detail_view.quote_saved.connect(
            self.refresh
        )

        self.detail_view.quote_deleted.connect(
            self.refresh
        )

        # Sprint berikutnya
        # self.search.textChanged.connect(
        #     self.filter_quotes
        # )

        # Sprint berikutnya
        # self.sort_filter.currentIndexChanged.connect(
        #     self.sort_quotes
        # )

    def refresh(self):

        self.load_books()

        self.load_quotes()

    def load_books(self):

        current_book = self.book_filter.currentData()

        self.book_filter.blockSignals(
            True
        )

        self.book_filter.clear()

        self.book_filter.addItem(
            "All Books",
            None,
        )

        books = BookService.get_all_books()

        for book in books:

            self.book_filter.addItem(
                book.title,
                book.id,
            )

        if current_book is not None:

            index = self.book_filter.findData(
                current_book
            )

            if index >= 0:

                self.book_filter.setCurrentIndex(
                    index
                )

        self.book_filter.blockSignals(
            False
        )

    def load_quotes(self):

        book_id = self.book_filter.currentData()

        if book_id is None:

            quotes = QuoteService.get_all_quotes()

        else:

            quotes = QuoteService.get_quotes_for_book(
                book_id
            )

        self.quote_list.set_quotes(
            quotes
        )

        if quotes:

            self.quote_list.select_first()

        else:

            self.selected_quote = None

            self.detail_view.clear()

        self.update_empty_state()

    def show_quote(
        self,
        quote,
    ):

        self.selected_quote = quote

        self.detail_view.display_quote(
            quote
        )

    def open_add_quote_dialog(self):

        dialog = AddQuoteDialog(
            self
        )

        if dialog.exec():

            self.refresh()

    def update_empty_state(self):

        has_quotes = self.quote_list.count() > 0

        self.quote_list.setVisible(
            has_quotes
        )

        self.detail_view.setVisible(
            has_quotes
        )

        self.empty_state.setVisible(
            not has_quotes
        )