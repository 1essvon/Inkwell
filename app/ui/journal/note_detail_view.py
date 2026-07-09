from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout
)
from PySide6.QtWidgets import QTextEdit
from PySide6.QtWidgets import QPushButton

class NoteDetailView(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.title_label = QLabel(
            "No Note Selected"
        )
        self.title_label.setObjectName(
            "detailTitle"
        )

        self.content_label = QLabel(
            ""
        )

        layout.addWidget(
            self.title_label
        )

        layout.addWidget(
            self.content_label
        )

        self.setLayout(layout)

        self.content_editor = QTextEdit()

        self.content_editor.setPlaceholderText(
            "Write your thoughts here..."
        )

        self.content_editor.setMinimumHeight(
            400
        )

        self.save_button = QPushButton(
            "Save Note"
        )

        layout.addWidget(
            self.content_editor
        )

        layout.addWidget(
            self.save_button
        )

        self.current_note = None

        self.save_button.clicked.connect(
            self.save_note
        )

    def display_note(self, note):

        self.title_label.setText(
            note.title
        )

        self.content_label.setText(
            note.content
        )

        self.current_note = note

        self.save_button.setText(
            "Save Note"
        )

        self.title_label.setText(
            note.title
        )

        self.content_editor.setPlainText(
            note.content
        )

    def clear(self):

        self.title_label.setText(
            "No Note Selected"
        )

        self.content_label.setText(
            ""
        )

        self.content_editor.clear()

        self.current_note = None

    def save_note(self):

        if not self.current_note:
            return

        from app.services.note_service import (
            NoteService
        )

        NoteService.update_note(
            self.current_note.id,
            self.content_editor.toPlainText()
        )

        self.save_button.setText(
            "Saved!"
        )