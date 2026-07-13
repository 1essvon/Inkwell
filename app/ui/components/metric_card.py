from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QLabel,
)

from app.ui.components.base_card import (
    BaseCard,
)

class MetricCard(BaseCard):

    def __init__(

        self,

        title: str,

        value: str,

        subtitle: str = "",

    ):

        super().__init__()

        self.setup_ui()

        self.set_data(

            title,

            value,

            subtitle,

        )

    def setup_ui(self):

        self.setMinimumHeight(
            130
        )

        self.title_label = QLabel()

        self.title_label.setObjectName(
            "metricTitle"
        )

        self.layout.addWidget(
            self.title_label
        )

        self.value_label = QLabel()

        self.value_label.setObjectName(
            "metricValue"
        )

        self.layout.addWidget(
            self.value_label
        )

        self.subtitle_label = QLabel()

        self.subtitle_label.setObjectName(
            "metricSubtitle"
        )

        self.layout.addWidget(
            self.subtitle_label
        )

        self.layout.addStretch()

    def set_data(

        self,

        title,

        value,

        subtitle="",

    ):

        self.title_label.setText(
            title
        )

        self.value_label.setText(
            value
        )

        self.subtitle_label.setText(
            subtitle
        )

    def update_value(

        self,

        value,

    ):

        self.value_label.setText(
            str(value)
        )

    def update_subtitle(

        self,

        subtitle,

    ):

        self.subtitle_label.setText(
            subtitle
        )

    def update_title(

        self,

        title,

    ):

        self.title_label.setText(
            title
        )