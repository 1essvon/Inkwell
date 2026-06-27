from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QWidget
)


class SearchBar(QWidget):

    def __init__(
        self,
        placeholder="Search..."
    ):
        super().__init__()

        layout = QHBoxLayout()

        layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        layout.setSpacing(8)

        icon = QLabel("🔍")

        icon.setObjectName(
            "searchIcon"
        )

        self.input = QLineEdit()

        self.input.setPlaceholderText(
            placeholder
        )

        self.input.setObjectName(
            "searchInput"
        )

        layout.addWidget(icon)

        layout.addWidget(self.input)

        self.setLayout(layout)

    def text(self):

        return self.input.text()

    def clear(self):

        self.input.clear()

    def line_edit(self):

        return self.input