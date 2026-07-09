from datetime import datetime

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
)

from app.services.book_service import (
    BookService,
)

from app.services.reading_session_service import (
    ReadingSessionService,
)

from app.ui.components.empty_state import (
    EmptyState,
)

from app.ui.components.page_header import (
    PageHeader
)

from app.ui.components.toolbar import (
    Toolbar
)

class ReadingHistoryView(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.refresh()

    # ==================================
    # Helpers
    # ==================================

    def format_datetime(self, dt):

        now = datetime.now()

        if dt.date() == now.date():

            return (
                "🕒 Today • "
                + dt.strftime("%H:%M")
            )

        if (

            now.date()
            - dt.date()

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

    def update_empty_state(self):

        has_history = (
            self.history_list.count() > 0
        )

        self.history_list.setVisible(
            has_history
        )

        self.empty_state.setVisible(
            not has_history
        )

    # ==================================
    # UI
    # ==================================

    def setup_ui(self):

        layout = QVBoxLayout()

        layout.addWidget(

            PageHeader(

                "Reading History"

            )

        )

        self.history_list = QListWidget()

        self.empty_state = EmptyState(

            icon="📖",

            title="No Reading History",

            subtitle=(
                "Complete your first reading "
                "session to see it here."
            )

        )

        self.empty_state.hide()

        layout.addWidget(
            self.history_list
        )

        layout.addWidget(
            self.empty_state
        )

        self.setLayout(
            layout
        )

    # ==================================
    # Refresh
    # ==================================

    def refresh(self):

        self.history_list.clear()

        sessions = (

            ReadingSessionService
            .get_recent_sessions()

        )

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

            size.setHeight(
                110
            )

            item.setSizeHint(
                size
            )

            self.history_list.addItem(
                item
            )

        self.history_list.scrollToTop()

        self.update_empty_state()