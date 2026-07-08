from datetime import datetime

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem
)

from app.services.reading_session_service import (
    ReadingSessionService
)

from app.services.book_service import (
    BookService
)


class ReadingHistoryView(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.refresh()

    def format_datetime(self, dt):

        now = datetime.now()

        if dt.date() == now.date():

            return (
                "🕒 Today • "
                + dt.strftime("%H:%M")
            )

        if (

            now.date() - dt.date()

        ).days == 1:

            return (
                "🕒 Yesterday • "
                + dt.strftime("%H:%M")
            )

        return (
            "🕒 "
            + dt.strftime(
                "%d %b %Y • %H:%M"
            )
        )

    # ==================================
    # UI
    # ==================================

    def setup_ui(self):

        layout = QVBoxLayout()

        title = QLabel("Reading History")

        title.setObjectName(
            "pageTitle"
        )

        layout.addWidget(
            title
        )

        self.history_list = QListWidget()

        layout.addWidget(
            self.history_list
        )

        self.setLayout(layout)

    # ==================================
    # Refresh
    # ==================================

    def refresh(self):

        self.history_list.clear()

        sessions = (
            ReadingSessionService
            .get_recent_sessions()
        )

        if not sessions:

            self.history_list.addItem(

                QListWidgetItem(

                    "No reading sessions yet.\n\n"
                    "Start a Focus Session to begin."

                )

            )

            return

        for session in sessions:

            book = BookService.get_book(
                session.book_id
            )

            if not book:
                continue

            pages = (
                session.end_page
                - session.start_page
            )

            page_text = (
                "Page"
                if pages == 1
                else "Pages"
            )

            minute_text = (
                "Minute"
                if session.duration_minutes == 1
                else "Minutes"
            )

            date_text = self.format_datetime(
                session.ended_at
            )

            text = (

                f"📖 {book.title}\n\n"

                f"{session.start_page}"

                f" → "

                f"{session.end_page}\n\n"

                f"+{pages} {page_text}"

                f" • "

                f"⏱ "

                f"{session.duration_minutes} {minute_text}\n\n"

                f"{date_text}"

            )

            item = QListWidgetItem(
                text
            )

            size = item.sizeHint()

            size.setHeight(110)

            item.setSizeHint(
                size
            )

            self.history_list.addItem(
                item
            )

            self.history_list.scrollToTop()