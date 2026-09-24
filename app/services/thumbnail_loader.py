import logging
from urllib.request import urlopen

from PySide6.QtCore import (
    QObject,
    Signal,
)

from PySide6.QtGui import (
    QPixmap,
)


logger = logging.getLogger(__name__)


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

        except Exception as error:
            logger.warning("Thumbnail loading failed (%s)", type(error).__name__)

            self.failed.emit()
