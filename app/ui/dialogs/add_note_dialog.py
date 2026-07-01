from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton
)

from app.services.note_service import NoteService


class AddNoteDialog(QDialog):

    def __init__(
        self,
        book_id
    ):
        super().__init__()

        self.book_id = book_id

        self.setWindowTitle("Add Note")

        layout = QVBoxLayout()

        layout.addWidget(
            QLabel("Title")
        )

        self.title_input = QLineEdit()

        layout.addWidget(
            QLabel("Content")
        )

        self.content_input = QTextEdit()

        layout.addWidget(
            self.content_input
        )

        layout.addWidget(
            self.title_input
        )

        save_button = QPushButton(
            "Save"
        )

        save_button.clicked.connect(
            self.save_note
        )

        layout.addWidget(
            save_button
        )

        self.setLayout(layout)

    def save_note(self):

        title = self.title_input.text().strip()

        content = self.content_input.toPlainText().strip()

        if not title:
            return

        NoteService.create_note(
            book_id=self.book_id,
            title=title,
            content=content
        )

        self.accept()