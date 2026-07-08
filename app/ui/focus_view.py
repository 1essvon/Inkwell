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
from app.ui.dialogs.end_session_dialog import (
    EndSessionDialog
)
from app.ui.dialogs.session_complete_dialog import (
    SessionCompleteDialog
)
from app.ui.dialogs.add_note_dialog import (
    AddNoteDialog
)

from app.ui.dialogs.add_quote_dialog import (
    AddQuoteDialog
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

        self.current_page_label = QLabel()

        self.current_page_label.setAlignment(
            Qt.AlignCenter
        )

        self.current_page_label.setObjectName(
            "pageIndicator"
        )

        layout.addWidget(
            self.current_page_label
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

        self.timer_label.setObjectName(
            "timerLabel"
        )

        layout.addWidget(
            self.timer_label
        )

        self.session_start_page = 0

        self.book = None

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

        self.book = BookService.get_book(
            book_id
        )

        if not self.book:
            return

        current = self.book.current_page or 0

        total = self.book.page_count or 0

        self.current_page_label.setText(

            f"Page {current} / {total}"

        )  

    # =====================
    # Start / Stop
    # =====================

    def toggle_session(self):

        # ==========================
        # START SESSION
        # ==========================

        if not self.is_reading:

            self.started_at = datetime.now()

            self.is_reading = True

            self.session_start_page = (
                self.book.current_page or 0
            )

            self.timer_label.setText(
                "00:00:00"
            )

            self.timer.start(1000)

            self.book_combo.setEnabled(False)

            self.session_button.setText(
                "Stop Session"
            )

            return

        # ==========================
        # STOP SESSION
        # ==========================

        self.timer.stop()

        elapsed = (
            datetime.now()
            - self.started_at
        )

        duration = max(
            1,
            int(
                elapsed.total_seconds() / 60
            )
        )

        dialog = EndSessionDialog(

            self.session_start_page,

            self.book.page_count

        )

        if not dialog.exec():

            self.timer.start(1000)

            return

        end_page = dialog.value()

        pages_read = max(
            0,
            end_page - self.session_start_page
        )

        book_id = self.book_combo.currentData()

        ReadingSessionService.create_session(

            book_id=book_id,

            start_page=self.session_start_page,

            end_page=end_page,

            duration_minutes=duration

        )

        BookService.update_current_page(

            book_id,

            end_page

        )

        self.is_reading = False

        self.started_at = None

        self.book_combo.setEnabled(True)

        self.session_button.setText(
            "Start Session"
        )

        self.timer_label.setText(
            "00:00:00"
        )

        self.load_book(
            self.book_combo.currentIndex()
        )

        dialog = SessionCompleteDialog(

            self.book.title,

            pages_read,

            duration

        )

        dialog.exec()

        if dialog.result_action == SessionCompleteDialog.NOTE:

            self.open_note_dialog()

        elif dialog.result_action == SessionCompleteDialog.QUOTE:

            self.open_quote_dialog()


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

    def open_note_dialog(self):

        dialog = AddNoteDialog(

            self.book.id

        )

        dialog.exec()

        self.refresh()

    def open_quote_dialog(self):

        dialog = AddQuoteDialog(

            self.book.id

        )

        dialog.exec()

        self.refresh()