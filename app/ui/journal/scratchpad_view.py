from PySide6.QtGui import (
    QKeySequence,
    QShortcut
)

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QTextEdit,
    QPushButton,
    QMessageBox
)

from app.services.scratchpad_service import (
    ScratchpadService
)


class ScratchpadView(QWidget):

    def __init__(self):

        super().__init__()

        self.setup_ui()

        self.load()

    # ==========================
    # UI
    # ==========================

    def setup_ui(self):

        layout = QVBoxLayout()

        title = QLabel("Scratchpad")

        title.setObjectName(
            "pageTitle"
        )

        layout.addWidget(
            title
        )

        self.editor = QTextEdit()

        self.editor.setPlaceholderText(

            "Write anything..."

        )

        layout.addWidget(
            self.editor
        )

        self.save_button = QPushButton(
            "Save"
        )

        self.save_button.clicked.connect(
            self.save
        )

        layout.addWidget(
            self.save_button
        )

        shortcut = QShortcut(

            QKeySequence(
                "Ctrl+S"
            ),

            self

        )

        shortcut.activated.connect(
            self.save
        )

        self.setLayout(
            layout
        )

    # ==========================
    # Load
    # ==========================

    def load(self):

        scratchpad = (

            ScratchpadService.get()

        )

        self.editor.setPlainText(

            scratchpad.content

        )

    # ==========================
    # Save
    # ==========================

    def save(self):

        ScratchpadService.save(

            self.editor.toPlainText()

        )

        QMessageBox.information(

            self,

            "Scratchpad",

            "Scratchpad saved."

        )

    # ==========================
    # Refresh
    # ==========================

    def refresh(self):

        self.load()