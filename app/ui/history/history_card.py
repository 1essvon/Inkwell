from datetime import datetime, timezone

from PySide6.QtWidgets import (
    QLabel,
    QHBoxLayout,
)

from app.models.book import Book
from app.models.reading_session import ReadingSession

from app.ui.components.base_card import BaseCard
from app.ui.components.icon_provider import SIZE_INLINE, pixmap


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

        dt = self.session.ended_at.replace(
            tzinfo=timezone.utc
        ).astimezone()

        now = datetime.now().astimezone()

        if dt.date() == now.date():

            return (
                "Today • "
                + dt.strftime("%H:%M")
            )

        if (
            now.date()
            - dt.date()
        ).days == 1:

            return (
                "Yesterday • "
                + dt.strftime("%H:%M")
            )

        return dt.strftime("%d %b %Y • %H:%M")
    
    def setup_ui(self):

        current = (
            self.session.end_page
            -
            self.session.start_page
        )

        title_layout = QHBoxLayout()
        title_layout.setSpacing(8)

        book_icon = QLabel()
        book_icon.setProperty("inkwell_icon_name", "book")
        book_icon.setProperty("inkwell_icon_size", SIZE_INLINE)
        book_icon.setPixmap(pixmap("book", size=SIZE_INLINE))
        title_layout.addWidget(book_icon)

        title = QLabel(self.book.title)

        title.setObjectName(
            "bookTitle"
        )

        title_layout.addWidget(title)
        self.layout.addLayout(title_layout)

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

            f"{self.session.duration_minutes} min"

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
            "captionText"
        )

        self.layout.addWidget(
            date
        )
