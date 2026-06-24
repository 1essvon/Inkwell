from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QMainWindow,
    QStackedWidget
)

from app.ui.library_view import LibraryView
from app.ui.journal_view import JournalView
from app.ui.statistics_view import (
    StatisticsView
)
from app.ui.focus_view import FocusView


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("The Inkwell")
        self.resize(1280, 720)

        root = QWidget()

        self.setCentralWidget(root)

        main_layout = QHBoxLayout()

        main_layout.setContentsMargins(
            12,
            12,
            12,
            12
        )

        main_layout.setSpacing(12)

        root.setLayout(main_layout)

        # ======================
        # Sidebar
        # ======================

        sidebar = QVBoxLayout()

        title = QLabel("THE INKWELL")

        title.setStyleSheet("""
        font-size: 20px;
        font-weight: bold;
        padding: 12px;
        """)

        sidebar.addWidget(title)

        self.library_button = QPushButton(
            "Library"
        )

        self.journal_button = QPushButton(
            "Journal"
        )

        self.statistics_button = QPushButton(
            "Statistics"
        )

        self.focus_button = QPushButton(
            "Focus Mode"
        )

        self.settings_button = QPushButton(
            "Settings"
        )

        sidebar.addWidget(
            self.library_button
        )

        sidebar.addWidget(
            self.journal_button
        )

        sidebar.addWidget(
            self.statistics_button
        )

        sidebar.addWidget(
            self.focus_button
        )

        sidebar.addWidget(
            self.settings_button
        )

        sidebar.addStretch()

        sidebar_widget = QWidget()
        sidebar_widget.setLayout(sidebar)
        sidebar_widget.setFixedWidth(220)

        # ======================
        # Pages
        # ======================

        self.pages = QStackedWidget()

        self.library_page = LibraryView()

        self.journal_page = JournalView()

        self.statistics_page = StatisticsView()

        self.focus_page = FocusView()

        self.settings_page = QLabel(
            "Settings Module"
        )

        self.pages.addWidget(
            self.library_page
        )

        self.pages.addWidget(
            self.journal_page
        )

        self.pages.addWidget(
            self.statistics_page
        )

        self.pages.addWidget(
            self.focus_page
        )

        self.pages.addWidget(
            self.settings_page
        )

        # ======================
        # Navigation
        # ======================

        self.library_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(0)
        )

        self.journal_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(1)
        )

        self.statistics_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(2)
        )

        self.focus_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(3)
        )

        self.settings_button.clicked.connect(
            lambda: self.pages.setCurrentIndex(4)
        )

        main_layout.addWidget(sidebar_widget)

        main_layout.addWidget(
            self.pages,
            4
        )