"""
File:
    dashboard_view.py

Purpose:
    Halaman Dashboard.

Responsibilities:
    - Menyusun layout
    - Menghubungkan widget Dashboard
    - Refresh seluruh widget

Does NOT:
    - Mengambil data database
    - Menghitung greeting
    - Menampilkan statistik
"""

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel
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

        layout = QVBoxLayout()

        layout.setSpacing(
            18
        )

        self.title = QLabel(
            "Dashboard"
        )

        self.title.setObjectName(
            "pageTitle"
        )

        self.greeting = GreetingWidget()

        self.continue_reading = ContinueReadingWidget()

        self.statistics = StatisticsGrid()

        layout.addWidget(
            self.title
        )

        layout.addWidget(
            self.greeting
        )

        layout.addWidget(
            self.continue_reading
        )

        layout.addWidget(
            self.statistics
        )

        layout.addStretch()

        self.setLayout(
            layout
        )

    # ----------------------------------
    # Data
    # ----------------------------------

    def refresh(self):

        self.greeting.refresh()

        self.continue_reading.refresh()

        self.statistics.refresh()