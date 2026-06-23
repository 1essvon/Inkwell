import sys

from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QMainWindow
from app.database.base import Base
from app.database.engine import engine

from app.models.book import Book

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("The Inkwell")
        self.resize(1280, 720)


def main():
    Base.metadata.create_all(bind=engine)
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
