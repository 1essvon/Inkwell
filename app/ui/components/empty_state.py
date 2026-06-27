from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget
)


class EmptyState(QWidget):

    def __init__(
        self,
        icon: str,
        title: str,
        subtitle: str
    ):
        super().__init__()

        layout = QVBoxLayout()

        layout.setAlignment(
            Qt.AlignCenter
        )

        layout.setSpacing(8)

        self.icon = QLabel(icon)
        self.icon.setObjectName(
            "emptyIcon"
        )
        self.icon.setAlignment(
            Qt.AlignCenter
        )

        self.title = QLabel(title)
        self.title.setObjectName(
            "emptyTitle"
        )
        self.title.setAlignment(
            Qt.AlignCenter
        )

        self.subtitle = QLabel(subtitle)
        self.subtitle.setObjectName(
            "emptySubtitle"
        )
        self.subtitle.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(self.icon)
        layout.addWidget(self.title)
        layout.addWidget(self.subtitle)

        self.setLayout(layout)