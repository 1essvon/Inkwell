from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
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


class DashboardView(QWidget):

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

        root_layout = QVBoxLayout()

        # ======================
        # Scroll Area
        # ======================

        scroll = QScrollArea()

        scroll.setWidgetResizable(
            True
        )

        content = QWidget()

        layout = QVBoxLayout()

        layout.setSpacing(
            18
        )

        # ======================
        # Widgets
        # ======================

        self.greeting = GreetingWidget()

        self.continue_reading = ContinueReadingWidget()

        self.library_summary = LibrarySummaryCard()

        self.recent_books = RecentBooksCard()

        self.statistics = StatisticsGrid()

        self.reading_goal = ReadingGoalCard()

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
            self.continue_reading
        )

        layout.addWidget(
            self.library_summary
        )

        layout.addWidget(
            self.statistics
        )

        layout.addWidget(
            self.reading_goal
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

        self.setLayout(
            root_layout
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