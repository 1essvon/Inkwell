from PySide6.QtCore import (
    Qt,
    Signal
)

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QListWidget,
    QListWidgetItem,
    QLabel,
    QSizePolicy
)

from app.services.book_service import BookService
from app.ui.components.book_card import BookCard
from app.ui.components.empty_state import (
    EmptyState
)

class BookListWidget(QWidget):

    bookSelected = Signal(object)

    # ----------------------------------
    # Initialization
    # ----------------------------------

    def __init__(self):
        super().__init__()

        self.setup_ui()

    # ----------------------------------
    # UI
    # ----------------------------------

    def setup_ui(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(
            0, 0, 0, 0
        )

        layout.setSpacing(0)

        self.list_widget = QListWidget()

        self.empty_state = EmptyState(

            icon="📚",

            title="Your Library is Empty",

            subtitle=(
                "Add your first book to start reading."
            )

        )

        self.empty_state.hide()

        self.list_widget.setSpacing(10)

        self.list_widget.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

        self.list_widget.itemClicked.connect(
            self.on_item_clicked
        )

        layout.addWidget(
            self.list_widget
        )

        layout.addWidget(
            self.empty_state
        )

        self.setLayout(
            layout
        )

        self.setSizePolicy(
            QSizePolicy.Expanding,
            QSizePolicy.Expanding
        )

    # ----------------------------------
    # Data
    # ----------------------------------

    def refresh(
        self,
        keyword="",
        status="All",
        selected_id=None,
        sort_by="Title"
    ):

        self.list_widget.clear()

        books = BookService.get_all_books()

        if sort_by == "Title":

            books.sort(
                key=lambda b: (b.title or "").lower()
            )

        elif sort_by == "Author":

            books.sort(
                key=lambda b: (b.author or "").lower()
            )

        elif sort_by == "Recently Added":

            books.sort(
                key=lambda b: b.id,
                reverse=True
            )

        elif sort_by == "Recently Updated":

            books.sort(
                key=lambda b: b.updated_at,
                reverse=True
            )

        keyword = keyword.lower().strip()

        for book in books:

            # ----------------------------
            # Search Filter
            # ----------------------------

            if keyword:

                if (

                    keyword not in book.title.lower()

                    and

                    keyword not in book.author.lower()

                ):

                    continue

            # ----------------------------
            # Status Filter
            # ----------------------------

            if status != "All":

                if book.status != status:

                    continue

            # ----------------------------
            # Add Book
            # ----------------------------

            self.add_book(book)

            if selected_id == book.id:

                item = self.list_widget.item(
                    self.list_widget.count() - 1
                )

                self.list_widget.setCurrentItem(
                    item
                )

                self.on_item_clicked(
                    item
                )

        self.update_empty_state()

    def add_book(
        self,
        book
    ):

        card = BookCard(book)

        item = QListWidgetItem()

        item.setSizeHint(
            card.sizeHint()
        )

        item.setData(
            1,
            book.id
        )

        self.list_widget.addItem(
            item
        )

        self.list_widget.setItemWidget(
            item,
            card
        )

    def update_empty_state(self):

        has_books = (
            self.list_widget.count() > 0
        )

        self.list_widget.setVisible(
            has_books
        )

        self.empty_state.setVisible(
            not has_books
        )

    def current_book(self):

        item = self.list_widget.currentItem()

        if item is None:

            return None

        return BookService.get_book(
            item.data(1)
        )

    # ----------------------------------
    # Events
    # ----------------------------------

    def on_item_clicked(
        self,
        item
    ):

        book = BookService.get_book(
            item.data(1)
        )

        self.bookSelected.emit(
            book
        )