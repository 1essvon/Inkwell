from PySide6.QtCore import (
    Qt,
    Signal,
)

from PySide6.QtWidgets import (
    QListWidget,
    QListWidgetItem,
    QAbstractItemView,
)

from app.ui.components.quote_card import (
    QuoteCard,
)

class QuoteListWidget(QListWidget):

    quote_selected = Signal(object)

    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.currentItemChanged.connect(
            self.on_current_changed
        )

    def setup_ui(self):

        self.setObjectName(
            "quoteList"
        )

        self.setSpacing(
            10
        )

        self.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self.setViewportMargins(
            0,
            0,
            0,
            0,
        )

        self.setUniformItemSizes(
            False
        )

        self.setSelectionMode(
            QAbstractItemView.SingleSelection
        )

        self.setVerticalScrollMode(
            QAbstractItemView.ScrollPerPixel
        )

        self.setHorizontalScrollBarPolicy(
            Qt.ScrollBarAlwaysOff
        )

    def set_quotes(
        self,
        quotes,
    ):

        self.clear()

        for quote in quotes:

            item = QListWidgetItem()

            card = QuoteCard()

            card.set_quote(
                quote
            )

            item.setSizeHint(
                card.sizeHint()
            )

            self.addItem(
                item
            )

            self.setItemWidget(
                item,
                card,
            )

            item.quote = quote

    def select_first(self):

        if self.count():

            self.setCurrentRow(
                0
            )

    def on_current_changed(
        self,
        current,
        previous,
    ):

        if previous:

            previous_card = self.itemWidget(
                previous
            )

            if previous_card:

                previous_card.set_selected(
                    False
                )

        if current:

            current_card = self.itemWidget(
                current
            )

            if current_card:

                current_card.set_selected(
                    True
                )

            self.quote_selected.emit(
                current.quote
            )

    