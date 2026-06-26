from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel
)
from app.ui.components.base_card import (
    BaseCard
)


class InfoCard(BaseCard):

    def __init__(self):
        super().__init__()

        self.setObjectName(
            "infoCard"
        )

        layout = QVBoxLayout()

        self.title = QLabel()

        self.title.setObjectName(
            "cardSectionTitle"
        )

        self.subtitle = QLabel()

        self.subtitle.setObjectName(
            "cardSubtitle"
        )

        self.content = QLabel()

        self.content.setObjectName(
            "cardContent"
        )

        self.layout.addWidget(
            self.title
        )

        self.layout.addWidget(
            self.subtitle
        )

        self.layout.addWidget(
            self.content
        )

        self.layout.addStretch()

        self.setLayout(layout)

    def set_data(
        self,
        title,
        subtitle,
        content
    ):

        self.title.setText(title)

        self.subtitle.setText(subtitle)

        self.content.setText(content)