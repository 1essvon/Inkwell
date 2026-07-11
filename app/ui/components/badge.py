from PySide6.QtWidgets import QLabel
from PySide6.QtCore import Qt


class Badge(QLabel):

    def __init__(
        self,
        text: str,
        badge_type: str = "default"
    ):
        super().__init__(text)

        self.setAlignment(
            Qt.AlignCenter
        )

        BADGE_TYPES = {
            "reading": "badgeReading",
            "finished": "badgeFinished",
            "waiting": "badgeWaiting",
            "danger": "badgeDanger",
            "default": "badgeDefault",
        }

        self.setObjectName(
            self.BADGE_TYPES.get(
                badge_type,
                "badgeDefault"
            )
        )