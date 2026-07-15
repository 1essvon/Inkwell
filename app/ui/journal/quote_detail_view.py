from PySide6.QtCore import Signal

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QLineEdit
)

from app.services.quote_service import (
    QuoteService,
)

class QuoteDetailView(QWidget):

    quote_saved = Signal()

    quote_deleted = Signal()

    def __init__(self):

        super().__init__()

        self.current_quote = None

        self.setup_ui()

    def setup_ui(self):

        self.main_layout = QVBoxLayout(self)

        self.main_layout.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        self.main_layout.setSpacing(
            14
        )

        self.page = QLabel()

        self.page.setObjectName(
            "pageTitle"
        )

        self.main_layout.addWidget(
            self.page
        )

        self.book = QLabel()

        self.book.setObjectName(
            "secondaryText"
        )

        self.main_layout.addWidget(
            self.book
        )

        self.author = QLabel()

        self.author.setObjectName(
            "captionText"
        )

        self.main_layout.addWidget(
            self.author
        )

        divider = QFrame()

        divider.setObjectName(
            "divider"
        )

        self.main_layout.addWidget(
            divider
        )

        meta_row = QHBoxLayout()

        meta_row.setSpacing(
            40
        )

        self.created = QLabel()

        self.created.setObjectName(
            "captionText"
        )

        self.updated = QLabel()

        self.updated.setObjectName(
            "captionText"
        )

        meta_row.addWidget(
            self.created
        )

        meta_row.addWidget(
            self.updated
        )

        meta_row.addStretch()

        self.main_layout.addLayout(
            meta_row
        )

        self.tags = QLineEdit()

        self.tags.setPlaceholderText(
            "Tags (comma separated)"
        )

        self.main_layout.addWidget(
            self.tags
        )

        divider2 = QFrame()

        divider2.setObjectName(
            "divider"
        )

        self.main_layout.addWidget(
            divider2
        )

        quote_title = QLabel(
            "Quote"
        )

        quote_title.setObjectName(
            "sectionTitle"
        )

        self.main_layout.addWidget(
            quote_title
        )

        self.quote_content = QTextEdit()

        self.quote_content.setReadOnly(
            True
        )

        self.main_layout.addWidget(
            self.quote_content
        )

        notes_title = QLabel(
            "Personal Notes"
        )

        notes_title.setObjectName(
            "sectionTitle"
        )

        self.main_layout.addWidget(
            notes_title
        )

        self.notes_editor = QTextEdit()

        self.notes_editor.setPlaceholderText(
            "Add your thoughts..."
        )

        self.main_layout.addWidget(
            self.notes_editor,
            1,
        )

        button_row = QHBoxLayout()

        button_row.addStretch()


        self.save_button = QPushButton(
            "Save"
        )

        button_row.addWidget(
            self.save_button
        )

        self.delete_button = QPushButton(
            "Delete"
        )

        self.delete_button.setObjectName(
            "dangerButton"
        )

        button_row.addWidget(
            self.delete_button
        )

        self.main_layout.addLayout(
            button_row
        )

        self.save_button.clicked.connect(
            self.save_quote
        )

        self.delete_button.clicked.connect(
            self.delete_quote
        )

    def display_quote(
        self,
        quote,
    ):

        self.current_quote = quote

        # ======================
        # Header
        # ======================

        if quote.page:

            self.page.setText(
                f"Page {quote.page}"
            )

        else:

            self.page.setText(
                "No Page"
            )

        self.book.setText(
            quote.book.title
        )

        if quote.book.author:

            self.author.setText(
                quote.book.author
            )

        else:

            self.author.clear()

        # ======================
        # Metadata
        # ======================

        if quote.created_at:

            self.created.setText(

                "Created • "

                + quote.created_at.strftime(
                    "%d %b %Y"
                )

            )

        else:

            self.created.clear()

        if quote.updated_at:

            self.updated.setText(

                "Updated • "

                + quote.updated_at.strftime(
                    "%d %b %Y"
                )

            )

        else:

            self.updated.clear()

        # ======================
        # Tags
        # ======================

        self.tags.setText(
            quote.tags or ""
        )
        # ======================
        # Content
        # ======================

        self.quote_content.setPlainText(
            quote.content or ""
        )

        self.notes_editor.setPlainText(
            quote.note or ""
        )

    def clear(self):

        self.current_quote = None

        self.page.setText(
            "No Quote Selected"
        )

        self.book.clear()

        self.author.clear()

        self.created.clear()

        self.updated.clear()

        self.tags.clear()

        self.quote_content.clear()

        self.notes_editor.clear()

    def save_quote(self):

        if self.current_quote is None:

            return

        QuoteService.update_quote(

            self.current_quote.id,

            self.notes_editor.toPlainText(),

            self.tags.text(),

        )

        self.note_saved.emit()

    def delete_quote(self):

        if self.current_quote is None:

            return

        QuoteService.delete_quote(
            self.current_quote.id
        )

        self.current_quote = None

        self.quote_deleted.emit()

        self.clear()