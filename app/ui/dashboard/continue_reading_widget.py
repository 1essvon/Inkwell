from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QProgressBar
)

from app.ui.components.info_card import (
    InfoCard
)

from app.services.book_service import (
    BookService
)


class ContinueReadingWidget(QWidget):

    # ----------------------------------
    # Initialization
    # ----------------------------------

    def __init__(self):
        super().__init__()

        self.setup_ui()

        self.refresh()

    # ----------------------------------
    # UI
    # ----------------------------------

    def setup_ui(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(
            8
        )

        self.info_card = InfoCard()

        self.progress = QProgressBar()

        layout.addWidget(
            self.info_card
        )

        layout.addWidget(
            self.progress
        )

        self.setLayout(
            layout
        )

    # ----------------------------------
    # Data
    # ----------------------------------

    def refresh(self):

        book = BookService.get_current_reading()

        if book is None:

            self.info_card.set_data(
                "Continue Reading",
                "",
                "No active reading."
            )

            self.progress.setValue(0)

            return

        if book.page_count > 0:

            percent = int(
                (book.current_page / book.page_count) * 100
            )

        else:

            percent = 0

        percent = max(
            0,
            min(
                percent,
                100,
            ),
        )

        self.info_card.set_data(
            "Continue Reading",
            book.author,
            f"{book.title}\n\nPage {book.current_page} / {book.page_count}"
        )

        self.progress.setValue(
            percent
        )