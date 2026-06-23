import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from app.ui.library_view import LibraryView

from app.database.init_db import init_database


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("The Inkwell")
        self.resize(1280, 720)

        self.library_view = LibraryView()

        self.setCentralWidget(self.library_view)

def main():
    init_database()

    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
