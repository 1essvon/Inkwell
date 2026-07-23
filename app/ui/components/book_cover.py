from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import (
    QLabel,
    QFrame,
    QVBoxLayout,
)


class BookCover(QFrame):

    SIZES = {

        "small": (60, 90),

        "medium": (72, 108),

        "large": (120, 180),

    }

    def __init__(
        self,
        size="medium",
        parent=None,
    ):
        super().__init__(parent)

        self._cover_path = None

        self.width, self.height = self.SIZES.get(
            size,
            self.SIZES["medium"],
        )

        self.setup_ui()

        self.clear()

    # ==================================================
    # UI
    # ==================================================

    def setup_ui(self):

        self.setObjectName(
            "bookCover"
        )

        self.setFixedSize(
            self.width,
            self.height,
        )

        self.label = QLabel()

        self.label.setAlignment(
            Qt.AlignmentFlag.AlignCenter
        )

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.addWidget(
            self.label
        )

    # ==================================================
    # Public API
    # ==================================================

    def set_cover(
        self,
        cover_path,
    ):

        self._cover_path = cover_path

        if (
            cover_path
            and
            Path(cover_path).exists()
        ):

            pixmap = QPixmap(
                cover_path
            )

            self.label.setPixmap(

                pixmap.scaled(

                    self.width,

                    self.height,

                    Qt.KeepAspectRatio,

                    Qt.TransformationMode.SmoothTransformation,

                )

            )

            return

        self.clear()

    def clear(self):

        self._cover_path = None

        self.label.setPixmap(
            QPixmap()
        )

        self.label.setText("📘")

    def cover_path(self):

        return self._cover_path