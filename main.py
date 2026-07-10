import sys

from PySide6.QtWidgets import QApplication

from app.database.init_db import init_database
from app.ui.main_window import MainWindow
from app.styles.load_styles import load_styles
from app.services.theme_service import (
    ThemeService
)

def main():

    init_database()

    app = QApplication(sys.argv)

    ThemeService.apply_theme(app)

    window = MainWindow()

    window.show()

    print("min :", window.minimumSize())
    print("max :", window.maximumSize())
    print("size:", window.size())
    print("hint:", window.minimumSizeHint())

    sys.exit(app.exec())


if __name__ == "__main__":
    main()