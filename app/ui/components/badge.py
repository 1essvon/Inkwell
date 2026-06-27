from PySide6.QtWidgets import QLabel


class Badge(QLabel):

    def __init__(
        self,
        text: str,
        badge_type: str = "default"
    ):
        super().__init__(text)

        self.setAlignment(
            __import__("PySide6.QtCore").QtCore.Qt.AlignCenter
        )

        mapping = {
            "reading": "badgeReading",
            "finished": "badgeFinished",
            "waiting": "badgeWaiting",
            "danger": "badgeDanger",
            "default": "badgeDefault"
        }

        self.setObjectName(
            mapping.get(
                badge_type,
                "badgeDefault"
            )
        )