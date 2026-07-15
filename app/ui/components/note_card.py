from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
)


class NoteCard(QFrame):

    def __init__(self):

        super().__init__()

        self.setObjectName(
            "noteCard"
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
            "noteIndicator"
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

        self.title = QLabel()

        self.title.setObjectName(
            "noteCardTitle"
        )

        self.title.setWordWrap(
            False
        )

        self.book = QLabel()

        self.book.setObjectName(
            "noteCardBook"
        )

        self.book.setWordWrap(
            False
        )

        content_layout.addWidget(
            self.title
        )

        content_layout.addWidget(
            self.book
        )

        root_layout.addLayout(
            content_layout
        )

    def set_note(
        self,
        note,
    ):

        self.note = note

        self.title.setText(
            note.title
        )

        self.book.setText(
            note.book.title
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