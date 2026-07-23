from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
)


class BookListItem(QWidget):

    def __init__(self):
        super().__init__()

        self.setup_ui()

    # ==================================================
    # UI
    # ==================================================

    def setup_ui(self):

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(2)

        self.title = QLabel()

        self.title.setObjectName(
            "bookTitle"
        )

        layout.addWidget(
            self.title
        )

        self.subtitle = QLabel()

        self.subtitle.setObjectName(
            "secondaryText"
        )

        layout.addWidget(
            self.subtitle
        )

    # ==================================================
    # Public API
    # ==================================================

    def set_data(
        self,
        title,
        subtitle,
    ):

        self.title.setText(
            title
        )

        self.subtitle.setText(
            subtitle
        )