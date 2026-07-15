from PySide6.QtCore import (
    Signal,
)

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QTextEdit,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
    QFrame,
)

from app.services.note_service import (
    NoteService,
)

class NoteDetailView(QWidget):

    note_deleted = Signal()

    note_saved = Signal()

    def __init__(self):

        super().__init__()

        self.current_note = None

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

        self.title = QLabel()

        self.title.setObjectName(
            "pageTitle"
        )

        self.main_layout.addWidget(
            self.title
        )

        self.book = QLabel()

        self.book.setObjectName(
            "secondaryText"
        )

        self.main_layout.addWidget(
            self.book
        )

        divider = QFrame()

        divider.setObjectName(
            "divider"
        )

        self.main_layout.addWidget(
            divider
        )

        self.created = QLabel()

        self.created.setObjectName(
            "captionText"
        )

        self.updated = QLabel()

        self.updated.setObjectName(
            "captionText"
        )

        self.main_layout.addWidget(
            self.created
        )

        self.main_layout.addWidget(
            self.updated
        )

        divider2 = QFrame()

        divider2.setObjectName(
            "divider"
        )

        self.main_layout.addWidget(
            divider2
        )

        self.editor = QTextEdit()

        self.editor.setPlaceholderText(
            "Write your thoughts..."
        )

        self.main_layout.addWidget(
            self.editor,
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
            self.save_note
        )

        self.delete_button.clicked.connect(
            self.delete_note
        )

    def display_note(
        self,
        note,
    ):

        self.current_note = note

        self.title.setText(
            note.title
        )

        self.book.setText(
            note.book.title
        )

        self.editor.setPlainText(
            note.content or ""
        )

        self.created.setText(

            "Created • "

            + note.created_at.strftime(
                "%d %b %Y"
            )

        )

        self.updated.setText(

            "Updated • "

            + note.updated_at.strftime(
                "%d %b %Y"
            )

        )

    def clear(self):

        self.current_note = None

        self.title.setText(
            "No Note Selected"
        )

        self.book.clear()

        self.created.clear()

        self.updated.clear()

        self.editor.clear()

    def save_note(self):

        if self.current_note is None:

            return

        NoteService.update_note(

            self.current_note.id,

            self.editor.toPlainText(),

        )

        self.note_saved.emit()

    def delete_note(self):

        if self.current_note is None:

            return

        NoteService.delete_note(

            self.current_note.id

        )

        self.current_note = None

        self.note_deleted.emit()

        self.clear()