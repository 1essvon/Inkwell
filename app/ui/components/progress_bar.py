from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QWidget,
)


class ProgressBar(QWidget):

    def __init__(
        self,
        parent=None,
    ):

        super().__init__(parent)

        self._percentage = 0

        self.setup_ui()

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

    # ==================================================
    # UI
    # ==================================================

    def setup_ui(self):

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(
            12
        )

        #
        # Track
        #

        self.track = QFrame()

        self.track.setFixedHeight(
            10
        )

        self.track.setObjectName(
            "progressTrack"
        )

        self.track.setStyleSheet("""
            QFrame#progressTrack {

                background: #2F2F2F;

                border-radius: 5px;

            }
        """)

        track_layout = QHBoxLayout(
            self.track
        )

        track_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        track_layout.setSpacing(
            0
        )

        #
        # Fill
        #

        self.fill = QFrame()

        self.fill.setFixedWidth(
            0
        )

        self.fill.setObjectName(
            "progressFill"
        )

        self.fill.setStyleSheet("""
            QFrame#progressFill {

                background: white;

                border-radius: 5px;

            }
        """)

        track_layout.addWidget(
            self.fill,
            alignment=Qt.AlignmentFlag.AlignLeft,
        )

        #
        # Percentage
        #

        self.percent_label = QLabel(
            "0%"
        )

        self.percent_label.setMinimumWidth(
            42
        )

        self.percent_label.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignVCenter
        )

        layout.addWidget(
            self.track,
            1,
        )

        layout.addWidget(
            self.percent_label
        )

    # ==================================================
    # Resize
    # ==================================================

    def resizeEvent(
        self,
        event,
    ):

        super().resizeEvent(
            event
        )

        self._update_fill()

    # ==================================================
    # Helpers
    # ==================================================

    def _update_fill(self):

        width = round(

            self.track.width()

            * self._percentage

            / 100

        )

        self.fill.setFixedWidth(
            width
        )

    # ==================================================
    # Public API
    # ==================================================

    def set_value(
        self,
        value: int,
    ):

        self._percentage = max(
            0,
            min(
                100,
                value,
            ),
        )

        self.percent_label.setText(
            f"{self._percentage}%"
        )

        self._update_fill()

    def set_progress(
        self,
        current: int,
        total: int,
    ):

        if total <= 0:

            self.set_value(
                0
            )

            return

        percentage = round(
            current
            / total
            * 100
        )

        self.set_value(
            percentage
        )