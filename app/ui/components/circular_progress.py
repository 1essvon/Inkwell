from PySide6.QtCore import (
    QRectF,
    Qt,
)

from PySide6.QtGui import (
    QColor,
    QFont,
    QPainter,
    QPen,
)

from PySide6.QtWidgets import (
    QWidget,
)


class CircularProgress(QWidget):

    def __init__(self, parent=None):

        super().__init__(parent)

        self._percentage = 0

        self._thickness = 10

        self._track_color = QColor("#343434")

        self._progress_color = QColor("#4F8EF7")

        self._text_color = QColor("#FFFFFF")

        self.setMinimumSize(
            120,
            120,
        )

    # ==================================================
    # Public API
    # ==================================================

    def set_percentage(
        self,
        percentage: int,
    ):

        percentage = max(
            0,
            min(
                percentage,
                100,
            ),
        )

        self._percentage = percentage

        self.update()

    def set_progress(

        self,

        current: int,

        total: int,

    ):

        if total <= 0:

            self.set_percentage(
                0,
            )

            return

        percentage = int(

            current / total * 100

        )

        self.set_percentage(
            percentage
        )

    # ==================================================
    # Paint
    # ==================================================

    def paintEvent(
        self,
        event,
    ):

        painter = QPainter(
            self
        )

        painter.setRenderHint(
            QPainter.RenderHint.Antialiasing
        )

        margin = self._thickness

        rect = QRectF(

            margin,

            margin,

            self.width() - margin * 2,

            self.height() - margin * 2,

        )

        #
        # Track
        #

        track_pen = QPen(

            self._track_color,

            self._thickness,

        )

        painter.setPen(
            track_pen
        )

        painter.drawArc(

            rect,

            0,

            360 * 16,

        )

        #
        # Progress
        #

        progress_pen = QPen(

            self._progress_color,

            self._thickness,

        )

        progress_pen.setCapStyle(

            Qt.PenCapStyle.RoundCap

        )

        painter.setPen(
            progress_pen
        )

        span = int(

            -360

            * 16

            * self._percentage

            / 100

        )

        painter.drawArc(

            rect,

            90 * 16,

            span,

        )

        #
        # Percentage
        #

        painter.setPen(

            self._text_color

        )

        font = QFont()

        font.setPointSize(
            18,
        )

        font.setBold(
            True,
        )

        painter.setFont(
            font
        )

        painter.drawText(

            self.rect(),

            Qt.AlignmentFlag.AlignCenter,

            f"{self._percentage}%",

        )