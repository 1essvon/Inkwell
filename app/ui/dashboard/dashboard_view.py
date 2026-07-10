from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea
)

from app.ui.dashboard.greeting_widget import (
    GreetingWidget
)

from app.ui.dashboard.continue_reading_widget import (
    ContinueReadingWidget
)

from app.ui.dashboard.statistics_grid import (
    StatisticsGrid
)

from app.ui.dashboard.library_summary_card import (
    LibrarySummaryCard
)

from app.ui.dashboard.recent_books_card import (
    RecentBooksCard
)

from app.ui.dashboard.reading_goal_card import (
    ReadingGoalCard
)

from app.ui.components.page_header import (
    PageHeader
)

from app.ui.dashboard.reading_streak_card import (
    ReadingStreakCard,
)

from app.ui.dashboard.quick_actions_widget import (
    QuickActionsWidget,
)

from PySide6.QtCore import Signal


class DashboardView(QWidget):

    add_book_requested = Signal()

    start_session_requested = Signal()

    new_note_requested = Signal()

    # ----------------------------------
    # Initialization
    # ----------------------------------

    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.refresh()

    # ----------------------------------
    # UI
    # ----------------------------------

    def setup_ui(self):

        root_layout = QVBoxLayout(self)

        # ======================
        # Scroll Area
        # ======================

        scroll = QScrollArea()

        scroll.setWidgetResizable(True)

        content = QWidget()

        layout = QVBoxLayout()

        layout.setSpacing(18)

        # ======================
        # Widgets
        # ======================

        self.greeting = GreetingWidget()

        self.quick_actions = QuickActionsWidget()

        self.continue_reading = ContinueReadingWidget()

        self.library_summary = LibrarySummaryCard()

        self.reading_goal = ReadingGoalCard()

        self.reading_streak = ReadingStreakCard()

        self.statistics = StatisticsGrid()

        self.recent_books = RecentBooksCard()

        # ======================
        # Signals
        # ======================

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
        # Goal Row
        # ======================

        goal_row = QHBoxLayout()

        goal_row.setSpacing(16)

        goal_row.addWidget(
            self.reading_goal,
            1,
        )

        goal_row.addWidget(
            self.reading_streak,
            1,
        )

        # ======================
        # Layout
        # ======================

        layout.addWidget(
            PageHeader(
                "Dashboard"
            )
        )

        layout.addWidget(
            self.greeting
        )

        layout.addWidget(
            self.quick_actions
        )

        layout.addWidget(
            self.continue_reading
        )

        layout.addWidget(
            self.library_summary
        )

        layout.addLayout(
            goal_row
        )

        layout.addWidget(
            self.statistics
        )

        layout.addWidget(
            self.recent_books
        )

        layout.addStretch()

        content.setLayout(
            layout
        )

        scroll.setWidget(
            content
        )

        root_layout.addWidget(
            scroll
        )

    # ----------------------------------
    # Data
    # ----------------------------------

    def refresh(self):

        self.greeting.refresh()

        self.continue_reading.refresh()

        self.library_summary.refresh()

        self.statistics.refresh()

        self.recent_books.refresh()

        self.reading_goal.refresh()

        self.reading_streak.refresh()