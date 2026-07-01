import sys

from PySide6.QtWidgets import QApplication

from app.database.init_db import init_database
from app.ui.main_window import MainWindow
from app.styles.load_styles import load_styles
from app.database.seed import (
    seed_database,
    seed_notes,
    seed_quotes
)

def main():

    init_database()
    seed_database()

    app = QApplication(sys.argv)

    app.setStyleSheet(
        load_styles()
    )

    window = MainWindow()

    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()