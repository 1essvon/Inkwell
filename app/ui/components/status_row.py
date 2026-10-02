from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QSizePolicy,
    QWidget,
)

from app.ui.components.icon_provider import (
    SIZE_INLINE,
    has_icon,
    pixmap,
)


class StatusRow(QWidget):

    def __init__(
        self,
        icon: str,
        label: str,
        parent=None,
    ):

        super().__init__(parent)

        self.setup_ui(
            icon,
            label,
        )

    # ==================================================
    # UI
    # ==================================================

    def setup_ui(
        self,
        icon: str,
        label: str,
    ):

        layout = QHBoxLayout(self)

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(
            8
        )

        #
        # Icon
        #

        self.icon = QLabel()

        self.icon.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        self.icon.setFixedWidth(
            22
        )

        if has_icon(icon):
            self.icon.setProperty("inkwell_icon_name", icon)
            self.icon.setProperty("inkwell_icon_size", SIZE_INLINE)
            self.icon.setPixmap(pixmap(icon, size=SIZE_INLINE))
        else:
            self.icon.setText(icon)

        layout.addWidget(
            self.icon
        )

        #
        # Label
        #

        self.label = QLabel(
            label
        )

        self.label.setObjectName(
            "secondaryText"
        )

        layout.addWidget(
            self.label
        )

        layout.addStretch()

        #
        # Count
        #

        self.count = QLabel(
            "0"
        )

        self.count.setObjectName(
            "bookTitle"
        )

        self.count.setAlignment(
            Qt.AlignmentFlag.AlignRight
            | Qt.AlignmentFlag.AlignVCenter
        )

        self.count.setMinimumWidth(
            32
        )

        self.count.setSizePolicy(
            QSizePolicy.Policy.Minimum,
            QSizePolicy.Policy.Preferred,
        )

        layout.addWidget(
            self.count
        )

    # ==================================================
    # Public API
    # ==================================================

    def set_count(
        self,
        count: int,
    ):

        self.count.setText(
            str(count)
        )