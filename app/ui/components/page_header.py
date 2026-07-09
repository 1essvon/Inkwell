from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QLabel,
    QVBoxLayout,
    QWidget,
)


class PageHeader(QWidget):

    def __init__(
        self,
        title: str,
        subtitle: str | None = None,
    ):
        super().__init__()

        layout = QVBoxLayout()

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(4)

        self.title_label = QLabel(
            title
        )

        self.title_label.setObjectName(
            "pageTitle"
        )

        layout.addWidget(
            self.title_label
        )

        self.subtitle_label = QLabel()

        self.subtitle_label.setObjectName(
            "pageSubtitle"
        )

        self.subtitle_label.setWordWrap(
            True
        )

        self.subtitle_label.setAlignment(
            Qt.AlignmentFlag.AlignLeft
        )

        if subtitle:

            self.subtitle_label.setText(
                subtitle
            )

            layout.addWidget(
                self.subtitle_label
            )

        else:

            self.subtitle_label.hide()

        self.setLayout(
            layout
        )

    def set_title(
        self,
        title: str,
    ):

        self.title_label.setText(
            title
        )

    def set_subtitle(
        self,
        subtitle: str | None,
    ):

        if subtitle:

            self.subtitle_label.setText(
                subtitle
            )

            self.subtitle_label.show()

        else:

            self.subtitle_label.hide()