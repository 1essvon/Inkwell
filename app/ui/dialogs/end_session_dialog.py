from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QVBoxLayout,
    QPushButton,
    QSpinBox
)


class EndSessionDialog(QDialog):

    def __init__(

        self,

        start_page,

        max_page

    ):

        super().__init__()

        self.setWindowTitle(
            "End Reading Session"
        )

        layout = QVBoxLayout()

        layout.addWidget(
            QLabel(
                f"Started on page {start_page}"
            )
        )

        layout.addWidget(
            QLabel(
                "Where did you stop?"
            )
        )

        self.end_page = QSpinBox()

        self.end_page.setMinimum(
            start_page
        )

        self.end_page.setMaximum(
            max_page
        )

        self.end_page.setValue(
            start_page
        )

        layout.addWidget(
            self.end_page
        )

        self.save_button = QPushButton(
            "Save Session"
        )

        self.save_button.clicked.connect(
            self.accept
        )

        layout.addWidget(
            self.save_button
        )

        self.setLayout(
            layout
        )

    def value(self):

        return self.end_page.value()