from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout
)


class BaseCard(QWidget):

    def __init__(self):
        super().__init__()

        self.setObjectName(
            "baseCard"
        )

        self.layout = QVBoxLayout()

        self.layout.setContentsMargins(
            16,
            16,
            16,
            16
        )

        self.layout.setSpacing(8)

        self.setLayout(
            self.layout
        )