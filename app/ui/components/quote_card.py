from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
)

from app.ui.components.icon_provider import (
    SIZE_INLINE,
    pixmap,
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
            78
        )

        root_layout = QHBoxLayout(self)

        root_layout.setContentsMargins(
            16,
            12,
            16,
            12,
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
            8
        )

        self.page = QLabel()

        self.page.setObjectName(
            "quoteCardPage"
        )

        self.quote_icon = QLabel()

        self.quote_icon.setObjectName(
            "quoteIcon"
        )

        self.quote_icon.setProperty(
            "inkwell_icon_name",
            "quote",
        )

        self.quote_icon.setProperty(
            "inkwell_icon_size",
            SIZE_INLINE,
        )

        self.quote_icon.setPixmap(
            pixmap(
                "quote",
                size=SIZE_INLINE,
            )
        )

        page_layout = QHBoxLayout()
        page_layout.setContentsMargins(0, 0, 0, 0)
        page_layout.setSpacing(8)
        page_layout.addWidget(self.quote_icon)
        page_layout.addWidget(self.page)
        page_layout.addStretch()

        self.book = QLabel()

        self.book.setObjectName(
            "quoteCardBook"
        )

        content_layout.addLayout(page_layout)

        content_layout.addWidget(
            self.book
        )

        root_layout.addLayout(
            content_layout,
            1,
        )

    def set_quote(
        self,
        quote,
    ):

        self.quote = quote

        if quote.page:

            self.page.setText(
                f"Page {quote.page}"
            )

        else:

            self.page.setText(
                "No Page"
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

    