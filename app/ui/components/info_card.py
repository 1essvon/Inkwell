from PySide6.QtWidgets import (
    QLabel
)

from app.ui.components.base_card import (
    BaseCard
)


class InfoCard(BaseCard):

    def __init__(self):
        super().__init__()

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

        self.content.setWordWrap(
            True
        )

        self.layout.addWidget(
            self.title
        )

        self.layout.addWidget(
            self.subtitle
        )

        self.layout.addSpacing(
            8
        )

        self.layout.addWidget(
            self.content
        )

    def set_data(
        self,
        title,
        subtitle,
        content
    ):

        self.title.setText(
            title
        )

        self.subtitle.setText(
            subtitle
        )

        self.content.setText(
            content
        )