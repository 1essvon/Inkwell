from PySide6.QtCore import (
    Qt,
    QTimer,
)

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QHBoxLayout,
)


class Toast(QWidget):

    def __init__(
        self,
        parent,
        message: str,
        duration: int = 2000,
    ):
        super().__init__(parent)

        self.setObjectName(
            "toast"
        )

        self.setWindowFlags(
            Qt.SubWindow
        )

        layout = QHBoxLayout()

        layout.setContentsMargins(
            16,
            12,
            16,
            12,
        )

        self.label = QLabel(
            message
        )

        self.label.setObjectName(
            "toastLabel"
        )

        layout.addWidget(
            self.label
        )

        self.setLayout(
            layout
        )

        self.adjustSize()

        # ----------------------------
        # Position
        # ----------------------------

        margin = 20

        x = (
            parent.width()
            - self.width()
            - margin
        )

        y = (
            parent.height()
            - self.height()
            - margin
        )

        self.move(
            x,
            y
        )

        # ----------------------------
        # Auto Hide
        # ----------------------------

        QTimer.singleShot(
            duration,
            self.close
        )

    @classmethod
    def show_message(
        cls,
        parent,
        message: str,
        duration: int = 2000,
    ):

        toast = cls(
            parent,
            message,
            duration,
        )

        toast.show()

        return toast