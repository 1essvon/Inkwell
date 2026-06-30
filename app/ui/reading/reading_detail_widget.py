from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QSpinBox
)
from PySide6.QtCore import Signal

from app.services.book_service import (
    BookService
)

class ReadingDetailWidget(QWidget):

    progressUpdated = Signal()

    def __init__(self):

        super().__init__()

        self.book = None

        self.setup_ui()

        self.setup_connections()

    def setup_ui(self):

        layout = QVBoxLayout()

        self.title = QLabel()

        self.title.setObjectName(
            "pageTitle"
        )

        self.progress = QLabel()

        buttons = QHBoxLayout()

        self.plus_one = QPushButton(
            "+1"
        )

        self.plus_five = QPushButton(
            "+5"
        )

        self.plus_ten = QPushButton(
            "+10"
        )

        buttons.addWidget(
            self.plus_one
        )

        buttons.addWidget(
            self.plus_five
        )

        buttons.addWidget(
            self.plus_ten
        )

        layout.addWidget(
            self.title
        )

        layout.addWidget(
            self.progress
        )

        layout.addLayout(
            buttons
        )

        layout.addSpacing(
            16
        )

        layout.addWidget(
            QLabel("Jump To Page")
        )

        self.page_input = QSpinBox()

        layout.addWidget(
            self.page_input
        )

        self.save_button = QPushButton(
            "Save"
        )

        layout.addWidget(
            self.save_button
        )

        layout.addStretch()

        self.setLayout(
            layout
        )

    def setup_connections(self):

        self.plus_one.clicked.connect(

            lambda: self.add_pages(1)

        )

        self.plus_five.clicked.connect(

            lambda: self.add_pages(5)

        )

        self.plus_ten.clicked.connect(

            lambda: self.add_pages(10)

        )

        self.save_button.clicked.connect(
            self.save_page
        )

    def set_book(
        self,
        book
    ):

        self.book = book

        self.refresh()

    def refresh(self):

        if not self.book:

            self.title.setText(
                "No Book Selected"
            )

            self.progress.clear()

            return

        current = self.book.current_page or 0

        total = self.book.page_count or 0

        self.page_input.setMaximum(
            total
        )

        self.page_input.setValue(
            current
        )

        self.title.setText(
            self.book.title
        )

        self.progress.setText(
            f"{current} / {total}"
        )

    def add_pages(
        self,
        amount
    ):

        if not self.book:

            return

        current = self.book.current_page or 0

        total = self.book.page_count or 0

        new_page = min(
            current + amount,
            total
        )

        BookService.update_current_page(

            self.book.id,

            new_page

        )

        self.book = BookService.get_book(
            self.book.id
        )

        self.refresh()

        self.progressUpdated.emit()

    def save_page(self):

        if not self.book:

            return

        BookService.update_current_page(

            self.book.id,

            self.page_input.value()

        )

        self.book = BookService.get_book(
            self.book.id
        )

        self.refresh()

        self.progressUpdated.emit()