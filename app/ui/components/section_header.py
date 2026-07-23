from PySide6.QtCore import Qt, Signal

from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QPushButton,
    QWidget,
)


class SectionHeader(QWidget):

    action_clicked = Signal()

    def __init__(
        self,
        title: str,
        action_text: str | None = None,
        parent=None,
    ):
        super().__init__(parent)

        self.setup_ui()

        self.set_title(title)

        if action_text:
            self.set_action(action_text)
        else:
            self.action.hide()

    # ==================================================
    # UI
    # ==================================================

    def setup_ui(self):

        layout = QHBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)

        self.title = QLabel()

        self.title.setObjectName("cardTitle")

        self.action = QPushButton()

        self.action.setFlat(True)

        self.action.clicked.connect(
            self.action_clicked.emit
        )

        layout.addWidget(self.title)

        layout.addStretch()

        layout.addWidget(self.action)

    # ==================================================
    # Public API
    # ==================================================

    def set_title(
        self,
        text: str,
    ):
        self.title.setText(text)

    def set_action(
        self,
        text: str,
    ):
        self.action.setText(text)
        self.action.show()