from PySide6.QtCore import Signal

from PySide6.QtWidgets import (
    QWidget,
    QLabel,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QFrame,
    QMessageBox,
)

from PySide6.QtGui import (
    QShortcut,
    QKeySequence,
)

from app.services.scratchpad_service import (
    ScratchpadService,
)

class ScratchpadDetailView(QWidget):

    entry_saved = Signal()

    entry_deleted = Signal()

    def __init__(self):

        super().__init__()

        self.current_entry = None

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

        self.title = QLineEdit()

        self.title.setPlaceholderText(
            "Untitled"
        )

        self.title.setObjectName(
            "pageTitleEditor"
        )

        self.main_layout.addWidget(
            self.title
        )

        self.updated = QLabel()

        self.updated.setObjectName(
            "captionText"
        )

        self.main_layout.addWidget(
            self.updated
        )

        divider = QFrame()

        divider.setObjectName(
            "divider"
        )

        self.main_layout.addWidget(
            divider
        )

        self.editor = QTextEdit()

        self.editor.setPlaceholderText(
            "Start writing..."
        )

        self.main_layout.addWidget(
            self.editor,
            1,
        )

        button_row = QHBoxLayout()

        self.save_button = QPushButton(
            "Save"
        )

        button_row.addWidget(
            self.save_button
        )

        self.delete_button = QPushButton(
            "Delete"
        )

        button_row.addWidget(
            self.delete_button
        )

        self.main_layout.addLayout(
            button_row
        )

        # baru setelah tombol dibuat
        self.save_button.clicked.connect(
            self.save_entry
        )

        self.delete_button.clicked.connect(
            self.delete_entry
        )

        save_shortcut = QShortcut(
            QKeySequence("Ctrl+S"),
            self,
        )

        save_shortcut.activated.connect(
            self.save_entry
        )

        self.title.returnPressed.connect(
            self.focus_editor
        )


    def display_entry(
        self,
        entry,
    ):

        self.current_entry = entry

        self.title.selectAll()

        self.title.setText(
            entry.title
        )

        if entry.updated_at:

            self.updated.setText(

                "Updated • "

                + entry.updated_at.strftime(
                    "%d %b %Y • %H:%M"
                )

            )

        else:

            self.updated.clear()

        self.editor.setPlainText(
            entry.content or ""
        )

    def clear(self):

        self.current_entry = None

        self.title.clear()

        self.title.setPlaceholderText(
            "Untitled"
        )

        self.updated.clear()

        self.editor.clear()

    def save_entry(self):

        title = self.title.text().strip()

        if not title:

            title = "Untitled"

            self.title.setText(
                title
            )

        content = self.editor.toPlainText()

        ScratchpadService.update_entry(

            self.current_entry.id,

            title,

            content,

        )

        self.entry_saved.emit()

    def delete_entry(self):

        if self.current_entry is None:

            return

        reply = QMessageBox.question(

            self,

            "Delete Scratchpad",

            (
                f'Delete "{self.current_entry.title}"?\n\n'
                "This action cannot be undone."
            ),

            QMessageBox.Yes | QMessageBox.No,

            QMessageBox.No,

        )

        if reply != QMessageBox.Yes:

            return

        ScratchpadService.delete_entry(
            self.current_entry.id
        )

        self.current_entry = None

        self.entry_deleted.emit()

        self.clear()

    def focus_editor(self):

        self.editor.setFocus()

        self.title.returnPressed.connect(
            self.focus_editor
        )

