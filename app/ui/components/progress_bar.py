from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QProgressBar,
    QSizePolicy,
    QWidget,
)

class ProgressBar(QWidget):

    def __init__(
        self,
        parent=None,
    ):

        super().__init__(parent)

        self.setup_ui()

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

    def setup_ui(self):

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(12)

        self.progress = QProgressBar()

        self.progress.setFixedHeight(12)

        self.progress.setStyleSheet("""
        QProgressBar {
            background: #2F2F2F;
            border: none;
            border-radius: 6px;
        }

        QProgressBar::chunk {
            background: white;
            border-radius: 6px;
        }
        """)

        self.progress.setTextVisible(
            False
        )

        self.progress.setRange(
            0,
            100
        )

        self.progress.setValue(
            0
        )

        self.progress.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        self.percent_label = QLabel(
            "0%"
        )

        self.percent_label.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.percent_label.setMinimumWidth(
            42
        )

        layout.addWidget(
            self.progress
        )

        layout.addWidget(
            self.percent_label
        )

        layout.setStretch(0, 1)
        layout.setStretch(1, 0)

    def set_value(
        self,
        value: int,
    ):

        value = max(
            0,
            min(
                100,
                value,
            ),
        )

        self.progress.setValue(
            value
        )

        self.percent_label.setText(
            f"{value}%"
        )

    def set_range(
        self,
        minimum: int,
        maximum: int,
    ):

        self.progress.setRange(
            minimum,
            maximum,
        )

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

        percent = round(
            current / total * 100
        )

        self.set_value(
            percent
        )