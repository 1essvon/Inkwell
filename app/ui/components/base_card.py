from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QSizePolicy
)
from PySide6.QtCore import Qt

class BaseCard(QWidget):

    def __init__(self):
        super().__init__()

        self.setObjectName(
            "baseCard"
        )

        self.layout = QVBoxLayout()

        self.layout.setContentsMargins(
            20,
            20,
            20,
            20
        )

        self.layout.setSpacing(12)

        self.setLayout(
            self.layout
        )

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_StyledBackground,
            True
        )