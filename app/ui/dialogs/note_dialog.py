from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QPushButton
)

from app.services.note_service import NoteService


class AddNoteDialog(QDialog):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Add Note")

        layout = QVBoxLayout()

        layout.addWidget(
            QLabel("Title")
        )

        self.title_input = QLineEdit()

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

        if not title:
            return

        NoteService.create_note(
            title
        )

        self.accept()