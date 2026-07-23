from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QWidget,
)


class SummaryRow(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.setup_ui()

    # ==================================================
    # UI
    # ==================================================

    def setup_ui(self):

        layout = QHBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        #
        # Icon
        #

        self.icon_label = QLabel()

        self.icon_label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.icon_label.setFixedWidth(20)

        #
        # Label
        #

        self.label = QLabel()

        #
        # Progress
        #

        self.progress = QProgressBar()

        self.progress.setRange(0, 100)

        self.progress.setTextVisible(False)

        self.progress.setFixedHeight(8)

        #
        # Value
        #

        self.value = QLabel()

        self.value.setAlignment(
            Qt.AlignmentFlag.AlignRight
        )

        self.value.setMinimumWidth(30)

        #
        # Layout
        #

        layout.addWidget(self.icon_label)

        layout.addWidget(self.label)

        layout.addWidget(
            self.progress,
            1,
        )

        layout.addWidget(self.value)

    # ==================================================
    # Public API
    # ==================================================

    def set_data(
        self,
        icon: str,
        label: str,
        value: int,
        percentage: int,
    ):

        self.icon_label.setText(icon)

        self.label.setText(label)

        self.value.setText(str(value))

        self.progress.setValue(percentage)