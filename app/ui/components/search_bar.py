"""
File:
    search_bar.py

Purpose:
    Search bar reusable untuk seluruh aplikasi.

Responsibilities:
    - Menampilkan input pencarian
    - Mengirim signal saat teks berubah

Does NOT:
    - Melakukan pencarian data
"""

from PySide6.QtCore import Signal

from PySide6.QtWidgets import (
    QWidget,
    QHBoxLayout,
    QLineEdit
)


class SearchBar(QWidget):

    textChanged = Signal(str)

    # ----------------------------------
    # Initialization
    # ----------------------------------

    def __init__(
        self,
        placeholder="Search...",
    ):
        super().__init__()

        self.setup_ui()

        self.setup_connections()

        self.input.setPlaceholderText(
            placeholder
        )

    # ----------------------------------
    # UI
    # ----------------------------------

    def setup_ui(self):

        layout = QHBoxLayout()

        layout.setContentsMargins(
            0, 0, 0, 0
        )

        self.input = QLineEdit()

        self.input.setPlaceholderText(
            "Search books..."
        )

        layout.addWidget(
            self.input
        )

        self.setLayout(
            layout
        )

    # ----------------------------------
    # Connections
    # ----------------------------------

    def setup_connections(self):

        self.input.textChanged.connect(
            self.textChanged.emit
        )

    # ----------------------------------
    # Public API
    # ----------------------------------

    def text(self):

        return self.input.text()

    def clear(self):

        self.input.clear()

    def focus(self):

        self.input.setFocus()

    def set_text(
        self,
        text: str,
    ):

        self.input.setText(
            text
        )