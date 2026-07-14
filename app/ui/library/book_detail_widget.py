from PySide6.QtCore import (
    Qt,
    Signal,
)
from PySide6.QtWidgets import (
    QLabel,
    QProgressBar,
    QVBoxLayout,
    QWidget,
    QGridLayout,
    QFrame,
    QPushButton
)

from app.constants.book_status import (
    BookStatus,
)

class BookDetailWidget(QWidget):

    editRequested = Signal()

    deleteRequested = Signal()

    continueRequested = Signal()

    notesRequested = Signal()

    quotesRequested = Signal()

    STATUS_OBJECT_NAMES = {

        BookStatus.READING:
            "badgeReading",

        BookStatus.COMPLETED:
            "badgeFinished",

        BookStatus.WANT_TO_READ:
            "badgeWaiting",

        BookStatus.PAUSED:
            "badgePaused",

        BookStatus.DROPPED:
            "badgeDanger",

    }

    def __init__(self):

        super().__init__()

        self.book = None

        self.setup_ui()

        self.setup_connections()

        self.clear()

    def setup_ui(self):

        self.main_layout = QVBoxLayout()

        self.main_layout.setContentsMargins(
            20,
            20,
            20,
            20,
        )

        self.cover = QLabel(
            "📘"
        )

        self.cover.setObjectName(
            "bookCover"
        )

        self.cover.setMinimumHeight(
            90
        )

        self.cover.setAlignment(
            Qt.AlignCenter
        )

        self.main_layout.addWidget(
            self.cover
        )

        self.title = QLabel()

        self.title.setObjectName(
            "bookTitle"
        )

        self.title.setAlignment(
            Qt.AlignCenter
        )

        self.main_layout.addWidget(
            self.title
        )

        self.author = QLabel()

        self.author.setObjectName(
            "secondaryText"
        )

        self.author.setAlignment(
            Qt.AlignCenter
        )

        self.main_layout.addWidget(
            self.author
        )

        self.status = QLabel()

        self.status.setObjectName(
            "badgeDefault"
        )

        self.main_layout.addWidget(
            self.status
        )

        self.progress = QProgressBar()

        self.progress.setFixedHeight(
            8
        )

        self.progress.setTextVisible(
            False
        )

        self.main_layout.addWidget(
            self.progress
        )

        self.progress_text = QLabel()

        self.progress_text.setObjectName(
            "captionText"
        )

        self.progress_text.setAlignment(
            Qt.AlignCenter
        )

        self.main_layout.addWidget(
            self.progress_text
        )

        divider = QFrame()

        divider.setObjectName(
            "divider"
        )

        self.main_layout.addWidget(
            divider
        )

        self.details_title = QLabel("Book Details")
        self.details_title.setObjectName("cardTitle")

        self.metadata_layout = QGridLayout()

        self.metadata_layout.setColumnStretch(
            0,
            1,
        )

        self.metadata_layout.setColumnStretch(
            1,
            1,
        )

        self.metadata_layout.setContentsMargins(
            0,
            8,
            0,
            0,
        )

        self.metadata_layout.setHorizontalSpacing(
            20
        )

        self.metadata_layout.setVerticalSpacing(
            12
        )   

        self.isbn = QLabel()

        self.publisher = QLabel()

        self.genre = QLabel()

        self.rating = QLabel()

        for label in (

            self.isbn,

            self.publisher,

            self.genre,

            self.rating,

        ):

            label.setObjectName(
                "secondaryText"
            )

        self.metadata_layout.addWidget(

            self.isbn,

            0,

            0,

        )

        self.metadata_layout.addWidget(

            self.publisher,

            0,

            1,

        )

        self.metadata_layout.addWidget(

            self.genre,

            1,

            0,

        )

        self.metadata_layout.addWidget(

            self.rating,

            1,

            1,

        )

        self.main_layout.addLayout(
            self.metadata_layout
        )

        self.main_layout.setSpacing(
            14
        )

        self.continue_button = QPushButton(
            "Continue Reading"
        )

        self.continue_button.setObjectName(
            "primaryButton"
        )

        self.notes_button = QPushButton(
            "Notes"
        )

        self.notes_button.setObjectName(
            "secondaryButton"
        )

        self.quotes_button = QPushButton(
            "Quotes"
        )

        self.quotes_button.setObjectName(
            "secondaryButton"
        )

        divider = QFrame()

        divider.setObjectName(
            "divider"
        )

        self.edit_button = QPushButton(
            "Edit Book"
        )

        self.edit_button.setObjectName(
            "secondaryButton"
        )

        self.delete_button = QPushButton(
            "Delete Book"
        )

        self.delete_button.setObjectName(
            "dangerButton"
        )

        self.main_layout.addStretch()

        self.setLayout(
            self.main_layout
        )

    def setup_connections(self):

        self.continue_button.clicked.connect(
            self.continueRequested.emit
        )

        self.notes_button.clicked.connect(
            self.notesRequested.emit
        )

        self.quotes_button.clicked.connect(
            self.quotesRequested.emit
        )

        self.edit_button.clicked.connect(
            self.editRequested.emit
        )

        self.delete_button.clicked.connect(
            self.deleteRequested.emit
        )

    def clear(self):

        self.book = None

        self.title.setText(
            "No Book Selected"
        )

        self.author.setText(
            "Choose a book from your library."
        )

        self.status.clear()

        self.progress.setValue(
            0
        )

        self.progress_text.clear()

        self.isbn.clear()

        self.publisher.clear()

        self.genre.clear()

        self.rating.clear()  

        for button in (

            self.continue_button,

            self.notes_button,

            self.quotes_button,

            self.edit_button,

            self.delete_button,

        ):

            button.setEnabled(False) 

    def set_book(
        self,
        book,
    ):

        self.book = book

        if book is None:

            self.clear()

            return

        self.populate_book()

    def populate_book(self):

        current = self.book.current_page or 0

        total = self.book.page_count or 0

        percent = self.calculate_progress(

            current,

            total,

        )

        self.title.setText(
            self.book.title
        )

        self.author.setText(
            self.book.author
        )

        self.progress.setValue(
            percent
        )

        self.progress_text.setText(
            f"{current} / {total} pages"
        )

        status = self.book.status

        self.status.setText(
            status
        )

        self.status.setObjectName(

            self.get_status_object_name(
                status
            )

        )

        self.status.style().unpolish(
            self.status
        )

        self.status.style().polish(
            self.status
        )

        self.isbn.setText(
            f"ISBN\n{self.book.isbn or '-'}"
        )

        self.publisher.setText(
            f"Publisher\n{self.book.publisher or '-'}"
        )

        self.genre.setText(
            f"Genre\n{self.book.genre or '-'}"
        )

        self.rating.setText(
            f"Rating\n{self.book.rating or '-'}"
        )

        for button in (

            self.continue_button,

            self.notes_button,

            self.quotes_button,

            self.edit_button,

            self.delete_button,

        ):

            button.setEnabled(True)

    def calculate_progress(
        self,
        current,
        total,
    ):

        if total <= 0:

            return 0

        return int(

            current / total * 100

        )
    
    def get_status_object_name(
        self,
        status,
    ):

        return self.STATUS_OBJECT_NAMES.get(

            status,

            "badgeDefault",

        )
    