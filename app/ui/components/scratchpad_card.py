from PySide6.QtWidgets import (
    QFrame,
    QLabel,
    QHBoxLayout,
    QVBoxLayout,
)

class ScratchpadCard(QFrame):

    def __init__(self):

        super().__init__()

        self.setObjectName(
            "scratchpadCard"
        )

        self.setup_ui()

    def setup_ui(self):

        self.setFixedHeight(
            82
        )

        root_layout = QHBoxLayout(self)

        root_layout.setContentsMargins(
            16,
            12,
            16,
            12,
        )

        root_layout.setSpacing(
            12
        )

        self.indicator = QFrame()

        self.indicator.setObjectName(
            "scratchpadIndicator"
        )

        self.indicator.setFixedWidth(
            4
        )

        root_layout.addWidget(
            self.indicator
        )

        content_layout = QVBoxLayout()

        content_layout.setSpacing(
            6
        )

        self.title = QLabel()

        self.title.setObjectName(
            "scratchpadCardTitle"
        )

        content_layout.addWidget(
            self.title
        )

        self.updated = QLabel()

        self.updated.setObjectName(
            "scratchpadCardUpdated"
        )

        content_layout.addWidget(
            self.updated
        )

        root_layout.addLayout(
            content_layout,
            1,
        )

    def set_entry(
        self,
        entry,
    ):

        self.entry = entry

        self.title.setText(
            entry.title
        )

        if entry.updated_at:

            self.updated.setText(

                entry.updated_at.strftime(
                    "%d %b %Y • %H:%M"
                )

            )

        else:

            self.updated.setText(
                "-"
            )

    def set_selected(
        self,
        selected,
    ):

        self.setProperty(
            "selected",
            selected,
        )

        self.style().unpolish(
            self
        )

        self.style().polish(
            self
        )

        self.update()

    