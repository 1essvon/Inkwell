from PySide6.QtWidgets import (
    QListWidget,
    QListWidgetItem,
    QAbstractItemView,
)

from PySide6.QtCore import (
    Qt,
    Signal,
)

from app.ui.components.note_card import (
    NoteCard,
)

class NoteListWidget(QListWidget):

    note_selected = Signal(object)

    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.itemSelectionChanged.connect(
            self.on_selection_changed
        )

        self.currentRowChanged.connect(
            lambda _: self.refresh_selection()
        )

    def setup_ui(self):

        self.setObjectName(
            "noteList"
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

    def clear_notes(self):

        self.clear()

    def set_notes(
        self,
        notes,
    ):

        self.clear()

        for note in notes:

            item = QListWidgetItem()

            card = NoteCard()

            card.set_note(
                note
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

            item.note = note

    def on_selection_changed(self):

        items = self.selectedItems()

        if not items:

            return

        note = items[0].note

        self.note_selected.emit(
            note
        )

    def selected_note(self):

        items = self.selectedItems()

        if not items:

            return None

        return items[0].note
    
    def select_first(self):

        if self.count():

            self.setCurrentRow(
                0
            )

    def refresh_selection(self):

        for row in range(
            self.count()
        ):

            item = self.item(
                row
            )

            card = self.itemWidget(
                item
            )

            card.set_selected(
                row == self.currentRow()
            )

    