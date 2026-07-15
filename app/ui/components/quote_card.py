from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
)


class QuoteCard(QFrame):

    def __init__(self):

        super().__init__()

        self.setObjectName(
            "quoteCard"
        )

        self.setup_ui()

    def setup_ui(self):

        self.setFixedHeight(
            72
        )

        root_layout = QHBoxLayout(self)

        root_layout.setContentsMargins(
            14,
            10,
            14,
            10,
        )

        root_layout.setSpacing(
            12
        )

        # ======================
        # Selected Indicator
        # ======================

        self.indicator = QFrame()

        self.indicator.setObjectName(
            "quoteIndicator"
        )

        self.indicator.setFixedWidth(
            4
        )

        root_layout.addWidget(
            self.indicator
        )

        # ======================
        # Content
        # ======================

        content_layout = QVBoxLayout()

        content_layout.setSpacing(
            4
        )

        self.page = QLabel()

        self.page.setObjectName(
            "quoteCardPage"
        )

        self.book = QLabel()

        self.book.setObjectName(
            "quoteCardBook"
        )

        content_layout.addWidget(
            self.page
        )

        content_layout.addWidget(
            self.book
        )

        root_layout.addLayout(
            content_layout
        )

    def set_quote(
        self,
        quote,
    ):

        self.quote = quote

        if quote.page:

            self.page.setText(
                f"❝  Page {quote.page}"
            )

        else:

            self.page.setText(
                "❝  No Page"
            )

        self.book.setText(
            quote.book.title
        )

    def set_selected(
        self,
        selected,
    ):

        self.setProperty(
            "selected",
            selected,
        )

        self.style().unpolish(
            self
        )

        self.style().polish(
            self
        )

        self.update()

    