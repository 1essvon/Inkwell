from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QProgressBar,
    QVBoxLayout,
    QSizePolicy,
)


class BookProgress(QWidget):

    def __init__(self, parent=None):
        super().__init__(parent)

        self._current = 0
        self._total = 0

        self.setup_ui()

        self.clear()

    def setup_ui(self):

        self.setSizePolicy(
            QSizePolicy.Policy.Expanding,
            QSizePolicy.Policy.Fixed,
        )

        self.progress_bar = QProgressBar()

        self.progress_bar.setRange(0, 100)

        self.progress_bar.setTextVisible(False)

        self.progress_bar.setFixedHeight(8)

        self.progress_text = QLabel()

        self.progress_text.setObjectName(
            "captionText"
        )

        layout = QVBoxLayout(self)

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(6)

        layout.addWidget(
            self.progress_bar
        )

        layout.addWidget(
            self.progress_text
        )

    def set_progress(self, current, total):

        self._current = current or 0

        self._total = total or 0

        percent = self.percent()

        self.progress_bar.setValue(percent)

        self.progress_text.setText(
            f"{self._current} / {self._total} pages"
        )

    def clear(self):

        self.set_progress(
            0,
            0,
        )

    def current(self):

        return self._current

    def total(self):

        return self._total

    def percent(self):

        if self._total <= 0:

            return 0

        return int(
            self._current / self._total * 100
        )