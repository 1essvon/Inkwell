from datetime import datetime

from PySide6.QtCore import Qt
from PySide6.QtCore import QTimer

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QSpinBox,
    QMessageBox
)

from app.services.book_service import BookService
from app.services.reading_session_service import (
    ReadingSessionService
)


class FocusView(QWidget):

    def __init__(self):
        super().__init__()

        self.is_reading = False
        self.started_at = None

        self.timer = QTimer()
        self.timer.timeout.connect(
            self.update_timer
        )

        layout = QVBoxLayout()

        # =====================
        # Book
        # =====================

        layout.addWidget(
            QLabel("Book")
        )

        self.book_combo = QComboBox()

        self.refresh_books()

        self.book_combo.currentIndexChanged.connect(
            self.load_book
        )

        layout.addWidget(
            self.book_combo
        )

        # =====================
        # Start Page
        # =====================

        layout.addWidget(
            QLabel("Start Page")
        )

        self.start_page = QSpinBox()

        layout.addWidget(
            self.start_page
        )

        # =====================
        # End Page
        # =====================

        layout.addWidget(
            QLabel("End Page")
        )

        self.end_page = QSpinBox()

        layout.addWidget(
            self.end_page
        )

        # =====================
        # Timer
        # =====================

        self.timer_label = QLabel(
            "00:00:00"
        )

        self.timer_label.setAlignment(
            Qt.AlignCenter
        )

        self.timer_label.setStyleSheet("""
            font-size:32px;
            font-weight:bold;
            padding:20px;
        """)

        layout.addWidget(
            self.timer_label
        )

        # =====================
        # Button
        # =====================

        self.session_button = QPushButton(
            "Start Session"
        )

        self.session_button.clicked.connect(
            self.toggle_session
        )

        layout.addWidget(
            self.session_button
        )

        layout.addStretch()

        self.setLayout(layout)

        if self.book_combo.count() > 0:
            self.load_book(0)

    # =====================
    # Refresh Books
    # =====================

    def refresh_books(self):

        current = self.book_combo.currentData()

        self.book_combo.blockSignals(True)

        self.book_combo.clear()

        books = BookService.get_all_books()

        for book in books:

            self.book_combo.addItem(
                book.title,
                book.id
            )

        self.book_combo.blockSignals(False)

        if current is not None:

            index = self.book_combo.findData(
                current
            )

            if index >= 0:
                self.book_combo.setCurrentIndex(
                    index
                )

    # =====================
    # Load Book
    # =====================

    def load_book(self, index):

        if index < 0:
            return

        book_id = self.book_combo.currentData()

        book = BookService.get_book(
            book_id
        )

        if not book:
            return

        current_page = book.current_page or 0

        max_page = book.page_count or 9999

        self.start_page.setMaximum(
            max_page
        )

        self.end_page.setMaximum(
            max_page
        )

        self.start_page.setValue(
            current_page
        )

        self.end_page.setValue(
            current_page
        )

    # =====================
    # Start / Stop
    # =====================

    def toggle_session(self):

        if not self.is_reading:

            self.started_at = datetime.now()

            self.is_reading = True

            self.timer.start(1000)

            self.book_combo.setEnabled(False)

            self.start_page.setEnabled(False)

            self.session_button.setText(
                "Stop Session"
            )

            return

        if self.end_page.value() < self.start_page.value():

            QMessageBox.warning(
                self,
                "Invalid Page",
                "End page must be greater than or equal to start page."
            )

            return

        self.timer.stop()

        elapsed = (
            datetime.now()
            - self.started_at
        )

        duration = max(
            1,
            int(elapsed.total_seconds() / 60)
        )

        book_id = self.book_combo.currentData()

        ReadingSessionService.create_session(
            book_id=book_id,
            start_page=self.start_page.value(),
            end_page=self.end_page.value(),
            duration_minutes=duration
        )

        BookService.update_current_page(
            book_id,
            self.end_page.value()
        )

        self.is_reading = False

        self.started_at = None

        self.book_combo.setEnabled(True)

        self.start_page.setEnabled(True)

        self.session_button.setText(
            "Start Session"
        )

        self.timer_label.setText(
            "00:00:00"
        )

        self.load_book(
            self.book_combo.currentIndex()
        )

        QMessageBox.information(
            self,
            "Reading Session",
            "Reading session saved!"
        )

    # =====================
    # Timer
    # =====================

    def update_timer(self):

        if not self.started_at:
            return

        elapsed = (
            datetime.now()
            - self.started_at
        )

        total = int(
            elapsed.total_seconds()
        )

        hours = total // 3600

        minutes = (
            total % 3600
        ) // 60

        seconds = total % 60

        self.timer_label.setText(
            f"{hours:02}:{minutes:02}:{seconds:02}"
        )

    def refresh(self):

        pass