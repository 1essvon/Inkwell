from PySide6.QtWidgets import (
    QVBoxLayout,
    QWidget,
)

from app.constants.book_status import (
    BookStatus,
)

from app.services.book_service import (
    BookService,
)

from app.ui.components.info_card import (
    InfoCard,
)


class LibrarySummaryCard(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.refresh()

    def setup_ui(self):

        layout = QVBoxLayout()

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(
            8,
        )

        self.card = InfoCard()

        layout.addWidget(
            self.card
        )

        self.setLayout(
            layout
        )

    def refresh(self):

        summary = BookService.get_status_summary()

        details = "\n".join(

            [

                f"📖 Reading : {summary[BookStatus.READING]}",

                f"📚 Want To Read : {summary[BookStatus.WANT_TO_READ]}",

                f"✅ Completed : {summary[BookStatus.COMPLETED]}",

                f"⏸ Paused : {summary[BookStatus.PAUSED]}",

                f"❌ Dropped : {summary[BookStatus.DROPPED]}",

            ]

        )

        self.card.set_data(

            "Library Summary",

            "",

            details,

        )