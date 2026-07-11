from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout
)
from PySide6.QtCore import Qt

from app.ui.components.base_card import (
    BaseCard
)


class StatCard(BaseCard):

    def __init__(
        self,
        title: str,
        value: str,
    ):

        super().__init__()

        self.title = QLabel(title)

        self.title.setAlignment(
            Qt.AlignCenter
        )

        self.title.setObjectName(
            "cardTitle"
        )

        self.value = QLabel(value)

        self.value.setAlignment(
            Qt.AlignCenter
        )

        self.value.setObjectName(
            "cardValue"
        )

        self.layout.setSpacing(8)

        self.layout.addWidget(
            self.title
        )

        self.layout.addWidget(
            self.value
        )

        self.setMinimumSize(
            140,
            100
        )

    def set_value(
        self,
        value,
    ):

        self.value.setText(
            str(value)
        )