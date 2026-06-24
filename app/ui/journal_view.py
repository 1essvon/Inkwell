from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QLabel,
    QStackedWidget
)

from app.ui.journal.notes_view import NotesView
from app.ui.journal.quotes_view import QuotesView

class JournalView(QWidget):

    def __init__(self):
        super().__init__()

        main_layout = QVBoxLayout()

        title = QLabel("Journal")
        title.setStyleSheet("""
            font-size: 20px;
            font-weight: bold;
        """)

        main_layout.addWidget(title)

        # ======================
        # Navigation
        # ======================

        nav_layout = QHBoxLayout()

        self.notes_button = QPushButton(
            "Notes"
        )

        self.quotes_button = QPushButton(
            "Quotes"
        )

        nav_layout.addWidget(
            self.notes_button
        )

        nav_layout.addWidget(
            self.quotes_button
        )

        main_layout.addLayout(
            nav_layout
        )

        # ======================
        # Pages
        # ======================

        self.pages = QStackedWidget()

        self.notes_page = NotesView()
        self.quotes_page = QuotesView()

        self.pages.addWidget(
            self.notes_page
        )

        self.pages.addWidget(
            self.quotes_page
        )

        main_layout.addWidget(
            self.pages
        )

        # ======================
        # Navigation Events
        # ======================

        self.notes_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(0)
        )

        self.quotes_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(1)
        )

        self.setLayout(main_layout)