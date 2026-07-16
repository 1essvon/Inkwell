from PySide6.QtCore import (
    Qt,
    QSize,
    Signal,
)

from PySide6.QtWidgets import (
    QListWidget,
    QListWidgetItem,
    QAbstractItemView,
)

from app.ui.components.scratchpad_card import (
    ScratchpadCard,
)

class ScratchpadListWidget(QListWidget):

    entry_selected = Signal(object)

    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.currentItemChanged.connect(
            self.on_current_changed
        )

    def setup_ui(self):

        self.setObjectName(
            "scratchpadList"
        )

        self.setSpacing(
            12
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

    def set_entries(
        self,
        entries,
    ):

        self.clear()

        for entry in entries:

            item = QListWidgetItem()

            card = ScratchpadCard()

            card.set_entry(
                entry
            )

            item.setSizeHint(
                QSize(
                    0,
                    82,
                )
            )

            self.addItem(
                item
            )

            self.setItemWidget(
                item,
                card,
            )

            item.entry = entry

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

            self.entry_selected.emit(
                current.entry
            )

    