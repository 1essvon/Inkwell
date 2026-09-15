from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSplitter
)

from app.constants.book_status import (
    BookStatus
)

from app.ui.reading.reading_book_list_widget import (
    ReadingBookListWidget
)

from app.ui.reading.reading_detail_widget import (
    ReadingDetailWidget
)

class ReadingSessionView(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.setup_connections()

        self.refresh()
        

    def setup_ui(self):

        layout = QVBoxLayout()

        self.book_list = ReadingBookListWidget()

        self.detail = ReadingDetailWidget()

        self.splitter = QSplitter(
            Qt.Horizontal
        )

        self.splitter.setChildrenCollapsible(False)

        self.splitter.addWidget(
            self.book_list
        )

        self.splitter.addWidget(
            self.detail
        )

        self.splitter.setStretchFactor(
            0,
            1
        )

        self.splitter.setStretchFactor(
            1,
            2
        )

        self.splitter.setSizes([
            280,
            700
        ])

        layout.addWidget(
            self.splitter
        )

        self.setLayout(
            layout
        )

    def refresh(self):

        self.book_list.refresh()

    def setup_connections(self):

        self.book_list.bookSelected.connect(
            self.on_book_selected
        )

        self.detail.progressUpdated.connect(
            self.on_progress_updated
        )

    def on_progress_updated(self):

        book = self.detail.book

        self.refresh_list()

        if not book:
            return

        if book.status == BookStatus.COMPLETED:

            self.detail.clear()

            self.window().statusBar().showMessage(
                "Book completed!"
            )

            return

        self.window().statusBar().showMessage(
            f"Progress updated to page "
            f"{book.current_page}."
        )

    def on_book_selected(
        self,
        book
    ):

        self.detail.set_book(
            book
        )

    def open_start_session(self):

        self.show_reading()

    def refresh_list(self):

        if self.detail.book:

            selected_id = self.detail.book.id

        else:

            selected_id = None

        self.book_list.refresh(

            selected_id=selected_id

        )