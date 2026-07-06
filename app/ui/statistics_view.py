from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QGroupBox,
    QFormLayout,
    QScrollArea
)

from app.services.statistics_service import (
    StatisticsService
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

        scroll = QScrollArea()

        scroll.setWidgetResizable(True)

        content = QWidget()

        layout = QVBoxLayout()

        content.setLayout(layout)

        scroll.setWidget(content)

        root_layout.addWidget(scroll)

        self.setLayout(root_layout)

        # ==================================
        # Library Statistics
        # ==================================

        library_group = QGroupBox(
            "Library"
        )

        library_layout = QFormLayout()

        self.total_books = QLabel()

        self.reading = QLabel()

        self.completed = QLabel()

        self.want_to_read = QLabel()

        self.paused = QLabel()

        self.dropped = QLabel()

        library_layout.addRow(
            "Total Books",
            self.total_books
        )

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
            "Reading"
        )

        reading_layout = QFormLayout()

        self.pages_read = QLabel()

        self.average_progress = QLabel()

        self.active_books = QLabel()

        self.longest_book = QLabel()

        self.shortest_book = QLabel()

        reading_layout.addRow(

            "Longest Book",

            self.longest_book

        )

        reading_layout.addRow(

            "Shortest Book",

            self.shortest_book

        )

        reading_layout.addRow(
            "Pages Read",
            self.pages_read
        )

        reading_layout.addRow(
            "Average Progress",
            self.average_progress
        )

        reading_layout.addRow(
            "Currently Reading",
            self.active_books
        )

        reading_group.setLayout(
            reading_layout
        )

        layout.addWidget(
            reading_group
        )

        # ==================================
        # Journal Statistics
        # ==================================

        journal_group = QGroupBox(
            "Journal"
        )

        journal_layout = QFormLayout()

        self.notes = QLabel()

        self.quotes = QLabel()

        journal_layout.addRow(
            "Notes",
            self.notes
        )

        journal_layout.addRow(
            "Quotes",
            self.quotes
        )

        journal_group.setLayout(
            journal_layout
        )

        layout.addWidget(
            journal_group
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

        self.longest_book.setText(

            reading["longest_book"]

        )

        self.shortest_book.setText(

            reading["shortest_book"]

        )

        # ------------------------------
        # Library
        # ------------------------------

        self.total_books.setText(
            str(
                library["total_books"]
            )
        )

        self.reading.setText(
            str(
                library["reading"]
            )
        )

        self.completed.setText(
            str(
                library["completed"]
            )
        )

        self.want_to_read.setText(
            str(
                library["want_to_read"]
            )
        )

        self.paused.setText(
            str(
                library["paused"]
            )
        )

        self.dropped.setText(
            str(
                library["dropped"]
            )
        )

        # ------------------------------
        # Reading
        # ------------------------------

        self.pages_read.setText(
            str(
                reading["pages_read"]
            )
        )

        self.average_progress.setText(
            f'{reading["average_progress"]}%'
        )

        self.active_books.setText(
            str(
                reading["active_books"]
            )
        )

        # ------------------------------
        # Journal
        # ------------------------------

        self.notes.setText(
            str(
                journal["notes"]
            )
        )

        self.quotes.setText(
            str(
                journal["quotes"]
            )
        )