from PySide6.QtWidgets import (
    QLabel,
    QFrame,
    QWidget,
    QVBoxLayout,
)

from app.ui.components.base_card import BaseCard
from app.ui.components.empty_state import EmptyState
from app.ui.components.section_header import SectionHeader


class ReadingStreakCard(BaseCard):

    def __init__(self):
        super().__init__()

        self.setup_ui()

        self.set_data(None)

    # ==================================================
    # UI
    # ==================================================

    def setup_ui(self):

        #
        # Header
        #

        self.header = SectionHeader(
            "Reading Streak"
        )

        self.layout.addWidget(
            self.header
        )

        #
        # Empty State
        #

        self.empty = EmptyState(

            icon="🔥",

            title="No reading streak",

            subtitle=(
                "Read today to begin\n"
                "your first streak."
            ),

        )

        self.layout.addWidget(
            self.empty
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
            12
        )

        def add_section(title):

            title_label = QLabel(title)
            title_label.setObjectName(
                "secondaryText"
            )

            value_label = QLabel()
            value_label.setObjectName(
                "bookTitle"
            )

            content_layout.addWidget(
                title_label
            )

            content_layout.addWidget(
                value_label
            )

            divider = QFrame()

            divider.setFrameShape(
                QFrame.Shape.HLine
            )

            content_layout.addWidget(
                divider
            )

            return value_label

        self.current_value = add_section(
            "🔥 Current"
        )

        self.best_value = add_section(
            "🏆 Best"
        )

        self.last_value = add_section(
            "📅 Last Reading"
        )

        self.status = QLabel()

        self.status.setObjectName(
            "secondaryText"
        )

        self.status.setWordWrap(
            True
        )

        content_layout.addWidget(
            self.status
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

        has_data = data is not None

        self.toggle_empty_state(
            has_data
        )

        if not has_data:
            return

        self.current_value.setText(
            data["current"]
        )

        self.best_value.setText(
            data["best"]
        )

        self.last_value.setText(
            data["last_read"]
        )

        self.status.setText(
            data["status"]
        )