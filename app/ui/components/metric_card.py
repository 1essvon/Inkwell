from PySide6.QtWidgets import QLabel

from app.ui.components.base_card import BaseCard


class MetricCard(BaseCard):

    def __init__(
        self,
        title: str,
        value: str = "0",
        subtitle: str = "",
    ):

        super().__init__()

        self.setup_ui()

        self.set_data(
            title=title,
            value=value,
            subtitle=subtitle,
        )

    # ==================================================
    # UI
    # ==================================================

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

    # ==================================================
    # Public API
    # ==================================================

    def set_data(
        self,
        title: str,
        value,
        subtitle: str = "",
    ):

        self.set_title(title)
        self.set_value(value)
        self.set_subtitle(subtitle)

    def set_title(
        self,
        title: str,
    ):

        self.title_label.setText(
            title
        )

    def set_value(
        self,
        value,
    ):

        self.value_label.setText(
            str(value)
        )

    def set_subtitle(
        self,
        subtitle: str,
    ):

        self.subtitle_label.setText(
            subtitle
        )