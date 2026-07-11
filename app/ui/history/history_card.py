from datetime import datetime

from PySide6.QtWidgets import (
    QLabel,
)

from app.models.book import Book
from app.models.reading_session import ReadingSession

from app.ui.components.base_card import BaseCard


class HistoryCard(BaseCard):

    def __init__(
        self,
        book: Book,
        session: ReadingSession,
    ):

        super().__init__()

        self.book = book
        self.session = session

        self.setup_ui()

    def format_datetime(self):

        dt = self.session.ended_at

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
            + dt.strftime("%d %b %Y • %H:%M")
        )
    
    def setup_ui(self):

        current = (
            self.session.end_page
            -
            self.session.start_page
        )

        title = QLabel(
            f"📖 {self.book.title}"
        )

        title.setObjectName(
            "bookTitle"
        )

        self.layout.addWidget(
            title
        )

        author = QLabel(
            self.book.author
        )

        author.setObjectName(
            "secondaryText"
        )

        self.layout.addWidget(
            author
        )

        self.layout.addSpacing(8)

        pages = QLabel(

            f"{self.session.start_page}"

            f" → "

            f"{self.session.end_page}"

        )

        pages.setObjectName(
            "bookProgress"
        )

        self.layout.addWidget(
            pages
        )

        info = QLabel(

            f"+{current} pages"

            f" • "

            f"⏱ {self.session.duration_minutes} min"

        )

        info.setObjectName(
            "secondaryText"
        )

        self.layout.addWidget(
            info
        )

        date = QLabel(
            self.format_datetime()
        )

        date.setObjectName(
            "summaryItem"
        )

        self.layout.addWidget(
            date
        )