from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QPushButton,
    QComboBox,
    QSpinBox
)

from app.services.book_service import (
    BookService
)

from app.services.reading_session_service import (
    ReadingSessionService
)


class FocusView(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        layout.addWidget(
            QLabel("Book")
        )

        self.book_combo = QComboBox()

        self.books = (
            BookService.get_all_books()
        )

        for book in self.books:

            self.book_combo.addItem(
                book.title,
                book.id
            )

        layout.addWidget(
            self.book_combo
        )

        layout.addWidget(
            QLabel("Start Page")
        )

        self.start_page = QSpinBox()

        layout.addWidget(
            self.start_page
        )

        layout.addWidget(
            QLabel("End Page")
        )

        self.end_page = QSpinBox()

        layout.addWidget(
            self.end_page
        )

        layout.addWidget(
            QLabel("Duration (minutes)")
        )

        self.duration = QSpinBox()

        self.duration.setMaximum(
            10000
        )

        layout.addWidget(
            self.duration
        )

        save_button = QPushButton(
            "Save Session"
        )

        save_button.clicked.connect(
            self.save_session
        )

        layout.addWidget(
            save_button
        )

        layout.addStretch()

        self.setLayout(layout)

    def save_session(self):

        ReadingSessionService.create_session(
            book_id=self.book_combo.currentData(),
            start_page=self.start_page.value(),
            end_page=self.end_page.value(),
            duration_minutes=self.duration.value()
        )