"""
File:
    quick_actions_widget.py

Purpose:
    Dashboard quick actions.
"""

from PySide6.QtCore import Signal, Qt, QSize

from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QHBoxLayout,
)

from app.ui.components.base_card import BaseCard
from app.ui.components.icon_provider import set_button_icon, SIZE_ACTION


class QuickActionsWidget(BaseCard):

    add_book_requested = Signal()
    start_session_requested = Signal()
    new_note_requested = Signal()

    CARD_HEIGHT = 90

    def __init__(self):

        super().__init__()

        self.setup_ui()

    def setup_ui(self):

        title = QLabel("Quick Actions")
        title.setObjectName("cardTitle")

        self.layout.addWidget(title)

        row = QHBoxLayout()
        row.setSpacing(16)

        self.add_button = self.create_button(
            "add_book",
            "Add Book"
        )

        self.session_button = self.create_button(
            "play",
            "Start Session"
        )

        self.note_button = self.create_button(
            "note",
            "New Note"
        )

        self.add_button.clicked.connect(
            self.add_book_requested.emit
        )

        self.session_button.clicked.connect(
            self.start_session_requested.emit
        )

        self.note_button.clicked.connect(
            self.new_note_requested.emit
        )

        row.addWidget(self.add_button)
        row.addWidget(self.session_button)
        row.addWidget(self.note_button)

        self.layout.addLayout(row)

    def create_button(
        self,
        icon_name,
        text,
    ):

        button = QPushButton(text)
        button.setObjectName("quickAction")
        set_button_icon(button, icon_name, size=SIZE_ACTION)

        button.setMinimumHeight(
            self.CARD_HEIGHT
        )

        button.setCursor(
            Qt.PointingHandCursor
        )

        return button
