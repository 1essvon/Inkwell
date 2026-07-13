from PySide6.QtCore import Signal

from PySide6.QtWidgets import (
    QHBoxLayout,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from app.ui.components.page_header import (
    PageHeader,
)

from app.ui.dashboard.continue_reading_widget import (
    ContinueReadingWidget,
)

from app.ui.dashboard.greeting_widget import (
    GreetingWidget,
)

from app.ui.dashboard.library_summary_card import (
    LibrarySummaryCard,
)

from app.ui.dashboard.quick_actions_widget import (
    QuickActionsWidget,
)

from app.ui.dashboard.reading_goal_card import (
    ReadingGoalCard,
)

from app.ui.dashboard.reading_streak_card import (
    ReadingStreakCard,
)

from app.ui.dashboard.recent_books_card import (
    RecentBooksCard,
)

from app.ui.dashboard.statistics_grid import (
    StatisticsGrid,
)

class DashboardView(QWidget):

    add_book_requested = Signal()

    start_session_requested = Signal()

    new_note_requested = Signal()

    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.refresh()

    def setup_ui(self):

        root_layout = QVBoxLayout(self)

        root_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        scroll = QScrollArea()

        scroll.setWidgetResizable(
            True
        )

        content = QWidget()

        layout = QVBoxLayout()

        layout.setSpacing(
            20
        )

        content.setLayout(
            layout
        )

        scroll.setWidget(
            content
        )

        root_layout.addWidget(
            scroll
        )

        self.header = PageHeader(
            "Dashboard"
        )

        self.greeting = GreetingWidget()

        self.quick_actions = QuickActionsWidget()

        self.continue_reading = ContinueReadingWidget()

        self.reading_goal = ReadingGoalCard()

        self.reading_streak = ReadingStreakCard()

        self.statistics = StatisticsGrid()

        self.library_summary = LibrarySummaryCard()

        self.recent_books = RecentBooksCard()

        self.quick_actions.add_book_requested.connect(
            self.add_book_requested.emit
        )

        self.quick_actions.start_session_requested.connect(
            self.start_session_requested.emit
        )

        self.quick_actions.new_note_requested.connect(
            self.new_note_requested.emit
        )

        # ======================
        # Hero Row
        # ======================

        hero_row = QHBoxLayout()

        hero_row.setSpacing(
            16
        )

        hero_row.addWidget(
            self.continue_reading,
            2,
        )

        hero_row.addWidget(
            self.reading_goal,
            1,
        )

        hero_row.addWidget(
            self.reading_streak,
            1,
        )

        # ======================
        # Info Row
        # ======================

        info_row = QHBoxLayout()

        info_row.setSpacing(
            16
        )

        info_row.addWidget(
            self.statistics,
            3,
        )

        info_row.addWidget(
            self.library_summary,
            2,
        )

        # ======================
        # Main Layout
        # ======================

        layout.addWidget(
            self.header
        )

        layout.addWidget(
            self.greeting
        )

        layout.addWidget(
            self.quick_actions
        )

        layout.addLayout(
            hero_row
        )

        layout.addLayout(
            info_row
        )

        layout.addWidget(
            self.recent_books
        )

        layout.addStretch()

    def refresh(self):

        self.greeting.refresh()

        self.continue_reading.refresh()

        self.reading_goal.refresh()

        self.reading_streak.refresh()

        self.statistics.refresh()

        self.library_summary.refresh()

        self.recent_books.refresh()