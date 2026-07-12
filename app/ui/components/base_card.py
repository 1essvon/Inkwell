from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class BaseCard(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setObjectName("baseCard")

        self.setAttribute(
            Qt.WidgetAttribute.WA_StyledBackground,
            True,
        )

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum,
        )

        self.layout = QVBoxLayout(self)

        self.layout.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        self.layout.setSpacing(16)

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