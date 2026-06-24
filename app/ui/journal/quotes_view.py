from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout
)


class QuotesView(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(
            QLabel("Quotes Module")
        )

        self.setLayout(layout)