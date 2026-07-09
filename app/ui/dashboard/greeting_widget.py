"""
File:
    greeting_widget.py

Purpose:
    Menampilkan salam sesuai waktu.

Responsibilities:
    - Menentukan greeting
    - Menampilkan subtitle

Does NOT:
    - Mengakses database
    - Menampilkan buku
    - Menampilkan statistik
"""

from datetime import datetime

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel
)


class GreetingWidget(QWidget):

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

        layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        layout.setSpacing(
            4
        )

        self.title = QLabel()

        self.title.setObjectName(
            "dashboardGreeting"
        )

        self.subtitle = QLabel(
            "Continue where you left off."
        )

        self.subtitle.setObjectName(
            "dashboardSubtitle"
        )

        layout.addWidget(
            self.title
        )

        layout.addWidget(
            self.subtitle
        )

        self.setLayout(
            layout
        )

    # ----------------------------------
    # Data
    # ----------------------------------

    def refresh(self):

        hour = datetime.now().hour

        if hour < 12:

            greeting = "Good Morning"

        elif hour < 18:

            greeting = "Good Afternoon"

        else:

            greeting = "Good Evening"

        self.title.setText(
            greeting
        )