from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QTextEdit,
    QPushButton
)

from app.services.scratchpad_service import (
    ScratchpadService
)


class ScratchpadView(QWidget):

    def __init__(self):
        super().__init__()

        layout = QVBoxLayout()

        self.editor = QTextEdit()

        self.save_button = QPushButton(
            "Save Scratchpad"
        )

        self.save_button.clicked.connect(
            self.save_content
        )

        layout.addWidget(
            self.editor
        )

        layout.addWidget(
            self.save_button
        )

        self.setLayout(layout)

        self.load_content()

    def load_content(self):

        entry = (
            ScratchpadService.get_entry()
        )

        if entry:

            self.editor.setPlainText(
                entry.content
            )

    def save_content(self):

        ScratchpadService.save_content(
            self.editor.toPlainText()
        )