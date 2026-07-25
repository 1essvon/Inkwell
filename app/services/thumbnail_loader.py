from urllib.request import urlopen

from PySide6.QtCore import (
    QObject,
    Signal,
)

from PySide6.QtGui import (
    QPixmap,
)


class ThumbnailLoader(QObject):

    loaded = Signal(QPixmap)

    failed = Signal()

    def load(self, url):

        if not url:

            self.failed.emit()
            return

        try:

            data = urlopen(url).read()

            pixmap = QPixmap()

            pixmap.loadFromData(data)

            self.loaded.emit(
                pixmap
            )

        except Exception:

            self.failed.emit()