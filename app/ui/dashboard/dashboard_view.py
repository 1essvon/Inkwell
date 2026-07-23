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

from app.services.dashboard_service import (
    DashboardService,
)

class DashboardView(QWidget):

    add_book_requested = Signal()

    start_session_requested = Signal()

    new_note_requested = Signal()

    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.connect_signals()

        self.refresh()

    def setup_ui(self):

        self._create_widgets()

        self._create_layout()
    
    def _create_widgets(self):

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

    def connect_signals(self):

        self.quick_actions.add_book_requested.connect(
            self.add_book_requested.emit
        )

        self.quick_actions.start_session_requested.connect(
            self.start_session_requested.emit
        )

        self.quick_actions.new_note_requested.connect(
            self.new_note_requested.emit
        )

    def _create_layout(self):

        self.root_layout = QVBoxLayout(
            self
        )

        self.root_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(
            True
        )

        self.content = QWidget()

        self.layout = QVBoxLayout(
            self.content
        )

        self.layout.setSpacing(
            20
        )

        self.scroll.setWidget(
            self.content
        )

        self.root_layout.addWidget(
            self.scroll
        )

        self.layout.addWidget(
            self.header
        )

        self.layout.addWidget(
            self.greeting
        )

        self.layout.addWidget(
            self.quick_actions
        )

        self.layout.addLayout(
            self._create_hero_row()
        )

        self.layout.addLayout(
            self._create_info_row()
        )

        self.layout.addWidget(
            self.recent_books
        )

        self.layout.addStretch()

    def _create_hero_row(self):

        layout = QHBoxLayout()

        layout.setSpacing(
            16
        )

        layout.addWidget(
            self.continue_reading,
            2,
        )

        layout.addWidget(
            self.reading_goal,
            1,
        )

        layout.addWidget(
            self.reading_streak,
            1,
        )

        return layout
    
    def _create_info_row(self):

        layout = QHBoxLayout()

        layout.setSpacing(
            16
        )

        layout.addWidget(
            self.statistics,
            3,
        )

        layout.addWidget(
            self.library_summary,
            2,
        )

        return layout

    def refresh(self):

        dashboard = DashboardService.get_dashboard_data()

        summary = dashboard["summary"]

        continue_reading = dashboard["continue_reading"]

        reading_goal = dashboard["reading_goal"]

        reading_streak = dashboard["reading_streak"]

        library_summary = dashboard["library_summary"]

        recent_books = dashboard["recent_books"]

        self.greeting.refresh()

        self.statistics.set_data(
            summary
        )

        self.continue_reading.set_data(
            continue_reading
        )

        self.reading_goal.set_data(
            reading_goal
        )

        self.reading_streak.set_data(
            reading_streak
        )

        self.library_summary.set_data(
            library_summary
        )

        self.recent_books.set_data(
            recent_books
        )