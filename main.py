import sys
import logging
from PySide6.QtWidgets import QApplication

from app.logging_config import configure_logging
from app.database.init_db import init_database
from app.ui.main_window import MainWindow
from app.styles.load_styles import load_styles
from app.services.theme_service import (
    ThemeService
)

logger = logging.getLogger("app.startup")

def main():

    configure_logging()

    try:
        init_database()
    except Exception:
        logger.exception("Application database initialization failed")
        raise

    app = QApplication(sys.argv)

    ThemeService.apply_theme(app)

    window = MainWindow()

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
