from PySide6.QtCore import Signal

from PySide6.QtWidgets import (
    QLabel,
    QPushButton,
    QTextEdit,
    QSpinBox,
    QHBoxLayout,
    QProgressBar,
    QVBoxLayout
)

from app.services.book_service import BookService
from app.services.note_service import NoteService
from app.services.quote_service import QuoteService

from app.ui.components.base_card import BaseCard


class ReadingDetailWidget(BaseCard):

    progressUpdated = Signal()

    def __init__(self):

        super().__init__()

        self.book = None

        self.setup_ui()

        self.setup_connections()

    def setup_ui(self):

        layout = self.layout

        # ==================================================
        # Header
        # ==================================================

        self.title = QLabel()
        self.title.setObjectName("pageTitle")

        self.author = QLabel()
        self.author.setObjectName("secondaryText")

        layout.addWidget(self.title)
        layout.addWidget(self.author)

        layout.addSpacing(12)

        # ==================================================
        # Reading Progress
        # ==================================================

        progress_title = QLabel("Reading Progress")
        progress_title.setObjectName("cardTitle")

        layout.addWidget(progress_title)

        self.progress = QLabel()

        layout.addWidget(self.progress)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setTextVisible(False)

        layout.addWidget(self.progress_bar)

        self.progress_percent = QLabel()
        self.progress_percent.setObjectName("secondaryText")

        layout.addWidget(self.progress_percent)

        # ==================================================
        # Quick Progress Buttons
        # ==================================================

        buttons = QHBoxLayout()
        buttons.setSpacing(8)

        self.plus_one = QPushButton("+1")
        self.plus_five = QPushButton("+5")
        self.plus_ten = QPushButton("+10")

        for button in (
            self.plus_one,
            self.plus_five,
            self.plus_ten,
        ):

            button.setMinimumHeight(38)

            buttons.addWidget(
                button,
                1
            )

        layout.addLayout(buttons)

        layout.addSpacing(16)

        # ==================================================
        # Jump To Page
        # ==================================================

        jump_title = QLabel("Jump To Page")
        jump_title.setObjectName("cardTitle")

        layout.addWidget(jump_title)

        jump_layout = QHBoxLayout()

        self.page_input = QSpinBox()

        self.save_button = QPushButton("Save")
        self.save_button.setMinimumHeight(38)

        jump_layout.addWidget(
            self.page_input,
            1
        )

        jump_layout.addWidget(
            self.save_button
        )

        layout.addLayout(jump_layout)

        layout.addSpacing(20)

        # ==================================================
        # Quote & Note
        # ==================================================

        bottom = QHBoxLayout()
        bottom.setSpacing(16)

        #
        # Quote
        #

        quote_layout = QVBoxLayout()

        quote_title = QLabel("Today's Quote")
        quote_title.setObjectName("cardTitle")

        self.quote_input = QTextEdit()

        self.quote_input.setPlaceholderText(
            "Save a memorable quote..."
        )

        self.quote_input.setMaximumHeight(120)

        self.save_quote_button = QPushButton(
            "Save Quote"
        )

        self.save_quote_button.setMinimumHeight(38)

        quote_layout.addWidget(quote_title)
        quote_layout.addWidget(self.quote_input)
        quote_layout.addWidget(self.save_quote_button)

        #
        # Note
        #

        note_layout = QVBoxLayout()

        note_title = QLabel("Today's Note")
        note_title.setObjectName("cardTitle")

        self.note_input = QTextEdit()

        self.note_input.setPlaceholderText(
            "Write something about today's reading..."
        )

        self.note_input.setMaximumHeight(120)

        self.save_note_button = QPushButton(
            "Save Note"
        )

        self.save_note_button.setMinimumHeight(38)

        note_layout.addWidget(note_title)
        note_layout.addWidget(self.note_input)
        note_layout.addWidget(self.save_note_button)

        bottom.addLayout(
            quote_layout,
            1
        )

        bottom.addLayout(
            note_layout,
            1
        )

        layout.addLayout(bottom)

        layout.addStretch()

    def refresh(self):

        # =====================================
        # No Book Selected
        # =====================================

        if not self.book:

            self.title.setText(
                "No Book Selected"
            )

            self.author.clear()

            self.progress.clear()

            self.progress_bar.setValue(0)

            self.progress_percent.clear()

            self.page_input.setEnabled(False)

            self.plus_one.setEnabled(False)

            self.plus_five.setEnabled(False)

            self.plus_ten.setEnabled(False)

            self.save_button.setEnabled(False)

            self.note_input.clear()

            self.note_input.setEnabled(False)

            self.save_note_button.setEnabled(False)

            self.quote_input.clear()

            self.quote_input.setEnabled(False)

            self.save_quote_button.setEnabled(False)

            return

        # =====================================
        # Enable Controls
        # =====================================

        self.page_input.setEnabled(True)

        self.plus_one.setEnabled(True)

        self.plus_five.setEnabled(True)

        self.plus_ten.setEnabled(True)

        self.save_button.setEnabled(True)

        self.note_input.setEnabled(True)

        self.save_note_button.setEnabled(True)

        self.quote_input.setEnabled(True)

        self.save_quote_button.setEnabled(True)

        # =====================================
        # Book Information
        # =====================================

        current = self.book.current_page or 0

        total = self.book.page_count or 0

        if total > 0:

            percent = int(
                (current / total) * 100
            )

        else:

            percent = 0

        self.title.setText(
            self.book.title
        )

        self.author.setText(
            self.book.author
        )

        self.progress.setText(
            f"{current} / {total} pages"
        )

        self.progress_bar.setValue(
            percent
        )

        self.progress_percent.setText(
            f"{percent}% completed"
        )

        # =====================================
        # Page Input
        # =====================================

        self.page_input.setMaximum(
            max(total, 1)
        )

        self.page_input.setValue(
            current
        )

    def setup_connections(self):

        self.plus_one.clicked.connect(
            lambda: self.add_pages(1)
        )

        self.plus_five.clicked.connect(
            lambda: self.add_pages(5)
        )

        self.plus_ten.clicked.connect(
            lambda: self.add_pages(10)
        )

        self.save_button.clicked.connect(
            self.save_page
        )

        self.save_note_button.clicked.connect(
            self.save_note
        )

        self.save_quote_button.clicked.connect(
            self.save_quote
        )

    def set_book(
        self,
        book,
    ):

        self.book = book

        self.refresh()

    def add_pages(
        self,
        amount,
    ):

        if not self.book:
            return

        current = self.book.current_page or 0

        total = self.book.page_count or 0

        new_page = min(
            current + amount,
            total,
        )

        BookService.update_current_page(
            self.book.id,
            new_page,
        )

        self.book = BookService.get_book(
            self.book.id
        )

        self.refresh()

        self.progressUpdated.emit()

    def save_page(self):

        if not self.book:
            return

        BookService.update_current_page(
            self.book.id,
            self.page_input.value(),
        )

        self.book = BookService.get_book(
            self.book.id
        )

        self.refresh()

        self.progressUpdated.emit()

    def save_note(self):

        if not self.book:
            return

        content = self.note_input.toPlainText().strip()

        if not content:
            return

        self.save_note_button.setEnabled(False)

        NoteService.create_quick_note(
            book_id=self.book.id,
            content=content,
            current_page=self.book.current_page,
        )

        self.note_input.clear()

        self.save_note_button.setEnabled(True)

        self.note_input.setFocus()

    def save_quote(self):

        if not self.book:
            return

        content = (
            self.quote_input
            .toPlainText()
            .strip()
        )

        if not content:
            return

        self.save_quote_button.setEnabled(False)

        QuoteService.create_quick_quote(
            book_id=self.book.id,
            content=content,
            page=self.book.current_page,
        )

        self.quote_input.clear()

        self.save_quote_button.setEnabled(True)

        self.quote_input.setFocus()

    def clear(self):

        self.set_book(None)