from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


class BaseCard(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self._setup_ui()

    # ==================================================
    # UI
    # ==================================================

    def _setup_ui(self):

        self.setObjectName(
            "baseCard"
        )

        self.setAttribute(
            Qt.WidgetAttribute.WA_StyledBackground,
            True,
        )

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Minimum,
        )

        self.layout = QVBoxLayout(self)

        self.layout.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        self.layout.setSpacing(
            16
        )

    # ==================================================
    # Helpers
    # ==================================================

    def toggle_empty_state(
        self,
        has_data: bool,
    ):

        if hasattr(
            self,
            "content",
        ):

            self.content.setVisible(
                has_data
            )

        if hasattr(
            self,
            "empty",
        ):

            self.empty.setVisible(
                not has_data
            )