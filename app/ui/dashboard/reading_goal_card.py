from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
)

from app.ui.components.base_card import BaseCard
from app.ui.components.empty_state import EmptyState
from app.ui.components.progress_bar import ProgressBar
from app.ui.components.section_header import SectionHeader


class ReadingGoalCard(BaseCard):

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
            "Reading Goal"
        )

        self.layout.addWidget(
            self.header
        )

        #
        # Empty State
        #

        self.empty = EmptyState(

            icon="🎯",

            title="No reading goal",

            subtitle=(
                "Set a yearly reading goal "
                "to track your progress."
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
            8
        )

        #
        # Progress
        #

        self.progress = ProgressBar()

        content_layout.addWidget(
            self.progress
        )

        #
        # Progress Text
        #

        self.progress_text = QLabel()

        self.progress_text.setObjectName(
            "secondaryText"
        )

        content_layout.addWidget(
            self.progress_text
        )

        #
        # Status
        #

        self.status = QLabel()

        self.status.setObjectName(
            "captionText"
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

        has_goal = (
            data is not None
            and data["goal"] > 0
        )

        self.toggle_empty_state(
            has_goal
        )

        if not has_goal:
            return

        completed = data["completed"]

        goal = data["goal"]

        self.progress.set_progress(
            completed,
            goal,
        )

        self.progress_text.setText(
            f"{completed} of {goal} books"
        )

        self.status.setText(
            data["status"]
        )