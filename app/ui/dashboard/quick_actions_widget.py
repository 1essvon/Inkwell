"""
File:
    quick_actions_widget.py

Purpose:
    Dashboard quick actions.
"""

from PySide6.QtCore import Signal, Qt

from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QHBoxLayout,
)

from app.ui.components.base_card import BaseCard


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
            "📚",
            "Add Book"
        )

        self.session_button = self.create_button(
            "📖",
            "Start Session"
        )

        self.note_button = self.create_button(
            "📝",
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
        icon,
        text,
    ):

        button = QPushButton(
            f"{icon}\n\n{text}"
        )

        button.setMinimumHeight(
            self.CARD_HEIGHT
        )

        button.setCursor(
            Qt.PointingHandCursor
        )

        return button