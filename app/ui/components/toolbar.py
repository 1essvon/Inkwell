from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout
)


class Toolbar(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QHBoxLayout()

        self.layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        self.layout.setSpacing(
            8
        )

        self.layout.addStretch()

        self.setLayout(
            self.layout
        )

    def add_widget(
        self,
        widget
    ):

        self.layout.insertWidget(
            self.layout.count() - 1,
            widget
        )