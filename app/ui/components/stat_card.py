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
        icon: str = "",
    ):

        super().__init__()

        self.layout.setSpacing(10)

        if icon:

            self.icon = QLabel(icon)

            self.icon.setAlignment(
                Qt.AlignmentFlag.AlignCenter
            )

            self.icon.setObjectName(
                "cardIcon"
            )

            self.layout.addWidget(
                self.icon
            )

        self.title = QLabel(title)

        self.title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.title.setObjectName(
            "cardTitle"
        )

        self.layout.addWidget(
            self.title
        )

        self.value = QLabel(value)

        self.value.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.value.setObjectName(
            "cardValue"
        )

        self.layout.addWidget(
            self.value
        )

        self.layout.addStretch()

        self.setMinimumSize(
            150,
            130,
        )

    def set_value(
        self,
        value,
    ):

        self.value.setText(
            str(value)
        )