from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QHBoxLayout,
)

from app.constants.book_status import BookStatus


class StatusBadge(QFrame):

    STATUS_MAP = {

        BookStatus.READING: (
            "Reading",
            "badgeReading",
        ),

        BookStatus.COMPLETED: (
            "Completed",
            "badgeCompleted",
        ),

        BookStatus.WANT_TO_READ: (
            "Want to Read",
            "badgeWaiting",
        ),

        BookStatus.PAUSED: (
            "Paused",
            "badgePaused",
        ),

        BookStatus.DROPPED: (
            "Dropped",
            "badgeDropped",
        ),

    }

    def __init__(self, parent=None):

        super().__init__(parent)

        self._status = None

        self.setup_ui()

        self.clear()

    # ==================================================
    # UI
    # ==================================================

    def setup_ui(self):

        self.label = QLabel()

        self.label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            8,
            0,
            8,
            0,
        )

        layout.setSpacing(0)

        self.setMaximumHeight(24)
        self.setMinimumHeight(24)

        layout.addWidget(
            self.label
        )

    # ==================================================
    # Public API
    # ==================================================

    def set_status(self, status):

        self._status = status

        text, object_name = self.STATUS_MAP.get(

            status,

            (
                "Unknown",
                "badgeDefault",
            ),

        )

        self.label.setText(
            text
        )

        self.setObjectName(
            object_name
        )

        # Force Qt to refresh stylesheet
        self.style().unpolish(self)
        self.style().polish(self)

    def status(self):

        return self._status

    def clear(self):

        self._status = None

        self.label.setText("")

        self.setObjectName(
            "badgeDefault"
        )

        self.style().unpolish(self)
        self.style().polish(self)