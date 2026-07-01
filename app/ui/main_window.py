from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QMainWindow,
    QStackedWidget
)
from app.ui.dashboard.dashboard_view import DashboardView
from app.ui.library.library_view import LibraryView
from app.ui.journal_view import JournalView
from app.ui.statistics_view import (
    StatisticsView
)
from app.ui.focus_view import FocusView
from app.ui.reading.reading_session_view import (
    ReadingSessionView
)


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

        self.dashboard_button = QPushButton(
            "Dashboard"
        )

        self.library_button = QPushButton(
            "Library"
        )

        self.reading_button = QPushButton(
            "Reading Session"
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
            self.dashboard_button
        )

        sidebar.addWidget(
            self.library_button
        )

        sidebar.addWidget(
            self.reading_button
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

        self.dashboard_page = DashboardView()

        self.library_page = LibraryView()

        self.reading_page = ReadingSessionView()

        self.journal_page = JournalView()

        self.statistics_page = StatisticsView()

        self.focus_page = FocusView()

        self.settings_page = QLabel(
            "Settings Module"
        )

        self.pages.addWidget(
            self.dashboard_page
        )

        self.pages.addWidget(
            self.library_page
        )

        self.pages.addWidget(
            self.reading_page
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

        self.dashboard_button.clicked.connect(
            self.show_dashboard
        )

        self.library_button.clicked.connect(
            self.show_library
        )

        self.reading_button.clicked.connect(
            self.show_reading
        )

        self.journal_button.clicked.connect(
            self.show_journal
        )

        self.statistics_button.clicked.connect(
            self.show_statistics
        )

        self.focus_button.clicked.connect(
            self.show_focus
        )

        self.settings_button.clicked.connect(
            self.show_settings
        )

        main_layout.addWidget(sidebar_widget)

        main_layout.addWidget(
            self.pages,
            4
        )

        self.pages.setCurrentIndex(0)

    def refresh_views(self):

        self.library_page.refresh()

        self.statistics_page.refresh()

    def show_dashboard(self):

        self.dashboard_page.refresh()

        self.pages.setCurrentIndex(
            0
        )


    def show_library(self):

        self.library_page.refresh()

        self.pages.setCurrentIndex(
            1
        )

    def show_reading(self):

        self.reading_page.refresh()

        self.pages.setCurrentIndex(
            2
        )


    def show_journal(self):

        self.journal_page.refresh()

        self.pages.setCurrentIndex(
            3
        )


    def show_statistics(self):

        self.statistics_page.refresh()

        self.pages.setCurrentIndex(
            4
        )


    def show_focus(self):

        self.pages.setCurrentIndex(
            5
        )


    def show_settings(self):

        self.pages.setCurrentIndex(
            6
        )