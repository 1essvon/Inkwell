from PySide6.QtWidgets import (
    QVBoxLayout,
    QWidget,
)

from app.ui.components.base_card import BaseCard
from app.ui.components.section_header import SectionHeader
from app.ui.components.status_row import StatusRow


class LibrarySummaryCard(BaseCard):

    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.set_data(
            {
                "reading": 0,
                "want_to_read": 0,
                "completed": 0,
                "paused": 0,
                "dropped": 0,
            }
        )

    # ==================================================
    # UI
    # ==================================================

    def setup_ui(self):

        #
        # Header
        #

        self.header = SectionHeader(
            "Library Summary"
        )

        self.layout.addWidget(
            self.header
        )

        #
        # Content
        #

        self.content = QWidget()

        content_layout = QVBoxLayout(
            self.content
        )

        content_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        content_layout.setSpacing(
            8
        )

        #
        # Status Rows
        #

        self.reading = StatusRow(
            "📖",
            "Reading",
        )

        self.want_to_read = StatusRow(
            "📚",
            "Want To Read",
        )

        self.completed = StatusRow(
            "✅",
            "Completed",
        )

        self.paused = StatusRow(
            "⏸",
            "Paused",
        )

        self.dropped = StatusRow(
            "❌",
            "Dropped",
        )

        rows = [

            self.reading,

            self.want_to_read,

            self.completed,

            self.paused,

            self.dropped,

        ]

        for row in rows:

            content_layout.addWidget(
                row
            )

        self.layout.addWidget(
            self.content
        )

        self.layout.addStretch()

    # ==================================================
    # Public API
    # ==================================================

    def set_data(
        self,
        data,
    ):

        self.reading.set_count(
            data["reading"]
        )

        self.want_to_read.set_count(
            data["want_to_read"]
        )

        self.completed.set_count(
            data["completed"]
        )

        self.paused.set_count(
            data["paused"]
        )

        self.dropped.set_count(
            data["dropped"]
        )