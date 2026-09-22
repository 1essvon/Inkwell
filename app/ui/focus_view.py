from datetime import datetime, timedelta

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
        self.timer_end_at = None
        self.paused_at = None
        self.paused_seconds = 0

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

        layout.addWidget(
            QLabel("Focus Duration")
        )

        self.duration_spin = QSpinBox()
        self.duration_spin.setRange(1, 120)
        self.duration_spin.setValue(25)
        self.duration_spin.setSuffix(" min")

        layout.addWidget(
            self.duration_spin
        )
                
        self.timer_label = QLabel(
            "25:00"
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

        self.pause_button = QPushButton(
            "Pause"
        )

        self.pause_button.setEnabled(False)
        self.pause_button.clicked.connect(
            self.toggle_pause
        )

        layout.addWidget(
            self.pause_button
        )

        self.reset_button = QPushButton(
            "Reset"
        )

        self.reset_button.setEnabled(False)
        self.reset_button.clicked.connect(
            self.reset_timer
        )

        layout.addWidget(
            self.reset_button
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

        books = BookService.get_reading_books()

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

            duration = self.duration_spin.value()

            self.timer_end_at = (
                datetime.now() + timedelta(minutes=duration)
            )

            self.paused_at = None
            self.paused_seconds = 0

            self.timer_label.setText(
                f"{duration:02}:00"
            )

            self.timer.start(1000)

            self.book_combo.setEnabled(False)

            self.session_button.setText(
                "Stop Session"
            )

            self.pause_button.setEnabled(True)
            self.pause_button.setText("Pause")

            self.reset_button.setEnabled(True)

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
            self.book.page_count or 999999
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

        self.pause_button.setEnabled(False)
        self.pause_button.setText("Pause")
        self.duration_spin.setEnabled(True)
        self.paused_at = None

        self.reset_button.setEnabled(False)

        self.timer_end_at = None

        self.timer_label.setText(
            "25:00"
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

    def reset_timer(self):

        if not self.is_reading:
            return

        self.timer.stop()

        duration = self.duration_spin.value()

        self.timer_end_at = (
            datetime.now() + timedelta(minutes=duration)
        )

        self.paused_at = None
        self.paused_seconds = 0

        self.pause_button.setText(
            "Pause"
        )

        self.timer_label.setText(
            f"{duration:02}:00"
        )

        self.timer.start(1000)

    def toggle_pause(self):

        if not self.is_reading:
            return

        if self.timer.isActive():

            self.timer.stop()
            self.paused_at = datetime.now()

            self.pause_button.setText(
                "Resume"
            )

            return

        if not self.paused_at:
            return

        paused_duration = (
            datetime.now() - self.paused_at
        )

        self.timer_end_at += paused_duration
        self.started_at += paused_duration

        self.paused_at = None

        self.pause_button.setText(
            "Pause"
        )

        self.timer.start(1000)


    # =====================
    # Timer
    # =====================

    def update_timer(self):

        if not self.timer_end_at:
            return

        remaining = (
            self.timer_end_at - datetime.now()
        )

        total = max(
            0,
            int(remaining.total_seconds())
        )

        minutes = total // 60
        seconds = total % 60

        self.timer_label.setText(
            f"{minutes:02}:{seconds:02}"
        )

        if total <= 0:
            self.timer.stop()
            self.timer_end_at = None

            if self.is_reading:
                self.window().statusBar().showMessage(
                    "Focus timer finished."
                )
                self.toggle_session()
                
    def refresh(self):

        pass

    def open_note_dialog(self):

        dialog = AddNoteDialog(
            self,
            self.book.id,
        )

        dialog.exec()

        self.refresh()

    def open_quote_dialog(self):

        dialog = AddQuoteDialog(
            self,
            self.book.id,
        )

        dialog.exec()

        self.refresh()