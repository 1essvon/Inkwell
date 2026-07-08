from typing import Callable

from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class EmptyState(QWidget):

    def __init__(
        self,
        icon: str,
        title: str,
        subtitle: str,
        button_text: str | None = None,
        button_callback: Callable | None = None,
    ):
        super().__init__()

        layout = QVBoxLayout()

        layout.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout.setSpacing(12)

        self.icon = QLabel(icon)

        self.icon.setObjectName(
            "emptyIcon"
        )

        self.icon.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.title = QLabel(title)

        self.title.setObjectName(
            "emptyTitle"
        )

        self.title.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.subtitle = QLabel(subtitle)

        self.subtitle.setObjectName(
            "emptySubtitle"
        )

        self.subtitle.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.subtitle.setWordWrap(
            True
        )

        layout.addWidget(
            self.icon
        )

        layout.addWidget(
            self.title
        )

        layout.addWidget(
            self.subtitle
        )

        self.button = None

        if button_text:

            self.button = QPushButton(
                button_text
            )

            self.button.setObjectName(
                "emptyButton"
            )

            if button_callback:

                self.button.clicked.connect(
                    button_callback
                )

            layout.addWidget(
                self.button,
                alignment=Qt.AlignmentFlag.AlignCenter
            )

        layout.addStretch()

        self.setLayout(
            layout
        )