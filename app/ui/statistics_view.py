from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QGroupBox,
    QFormLayout,
    QScrollArea,
    QHBoxLayout
)

from app.services.statistics_service import (
    StatisticsService
)

from app.ui.components.page_header import (
    PageHeader
)

from app.ui.components.stat_card import (
    StatCard
)


class StatisticsView(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.refresh()

    # ==================================
    # UI
    # ==================================

    def setup_ui(self):

        root_layout = QVBoxLayout()

        root_layout.setContentsMargins(
            0,
            0,
            0,
            0
        )

        root_layout.setSpacing(12)

        root_layout.addWidget(

            PageHeader(
                "Statistics"
            )

        )

        scroll = QScrollArea()

        scroll.setWidgetResizable(True)

        content = QWidget()

        layout = QVBoxLayout()

        layout.setSpacing(16)

        content.setLayout(layout)

        scroll.setWidget(content)

        root_layout.addWidget(scroll)

        self.setLayout(root_layout)

        overview = QHBoxLayout()

        overview.setSpacing(12)

        self.total_books = StatCard(
            "Books",
            "0"
        )

        self.pages_read = StatCard(
            "Pages",
            "0"
        )

        self.notes = StatCard(
            "Notes",
            "0"
        )

        self.quotes = StatCard(
            "Quotes",
            "0"
        )

        overview.addWidget(
            self.total_books
        )

        overview.addWidget(
            self.pages_read
        )

        overview.addWidget(
            self.notes
        )

        overview.addWidget(
            self.quotes
        )

        layout.addLayout(
            overview
        )

        # ==================================
        # Library Statistics
        # ==================================

        library_group = QGroupBox(
            "Library Overview"
        )

        library_layout = QFormLayout()

        self.reading = QLabel()

        self.completed = QLabel()

        self.want_to_read = QLabel()

        self.paused = QLabel()

        self.dropped = QLabel()

        library_layout.addRow(
            "Reading",
            self.reading
        )

        library_layout.addRow(
            "Completed",
            self.completed
        )

        library_layout.addRow(
            "Want To Read",
            self.want_to_read
        )

        library_layout.addRow(
            "Paused",
            self.paused
        )

        library_layout.addRow(
            "Dropped",
            self.dropped
        )

        library_group.setLayout(
            library_layout
        )

        layout.addWidget(
            library_group
        )

        # ==================================
        # Reading Statistics
        # ==================================

        reading_group = QGroupBox(
            "Reading Overview"
        )

        reading_layout = QFormLayout()

        self.average_progress = QLabel()

        self.active_books = QLabel()

        self.longest_book = QLabel()

        self.shortest_book = QLabel()

        reading_layout.addRow(
            "Currently Reading",
            self.active_books
        )

        reading_layout.addRow(
            "Average Progress",
            self.average_progress
        )

        reading_layout.addRow(
            "Longest Book",
            self.longest_book
        )

        reading_layout.addRow(
            "Shortest Book",
            self.shortest_book
        )

        reading_group.setLayout(
            reading_layout
        )

        layout.addWidget(
            reading_group
        )

        layout.addStretch()

    # ==================================
    # Refresh
    # ==================================

    def refresh(self):

        library = (
            StatisticsService
            .get_library_statistics()
        )

        reading = (
            StatisticsService
            .get_reading_statistics()
        )

        journal = (
            StatisticsService
            .get_journal_statistics()
        )

        # ----------------------------------
        # Overview Cards
        # ----------------------------------

        self.total_books.set_value(
            library["total_books"]
        )

        self.pages_read.set_value(
            reading["pages_read"]
        )

        self.notes.set_value(
            journal["notes"]
        )

        self.quotes.set_value(
            journal["quotes"]
        )

        # ----------------------------------
        # Library
        # ----------------------------------

        self.reading.setText(
            str(library["reading"])
        )

        self.completed.setText(
            str(library["completed"])
        )

        self.want_to_read.setText(
            str(library["want_to_read"])
        )

        self.paused.setText(
            str(library["paused"])
        )

        self.dropped.setText(
            str(library["dropped"])
        )

        # ----------------------------------
        # Reading
        # ----------------------------------

        self.average_progress.setText(
            f'{reading["average_progress"]}%'
        )

        self.active_books.setText(
            str(reading["active_books"])
        )

        self.longest_book.setText(
            reading["longest_book"]
        )

        self.shortest_book.setText(
            reading["shortest_book"]
        )