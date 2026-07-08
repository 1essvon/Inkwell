from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QPushButton,
    QVBoxLayout
)
from PySide6.QtCore import Qt

class SessionCompleteDialog(QDialog):

    DONE = 0
    NOTE = 1
    QUOTE = 2

    def __init__(

        self,

        title,

        pages,

        duration

    ):

        super().__init__()

        self.result_action = self.DONE

        self.setWindowTitle(
            "Reading Complete"
        )

        self.resize(
            420,
            320
        )

        self.setMinimumWidth(
            420
        )

        layout = QVBoxLayout()

        layout.setSpacing(16)

        layout.setContentsMargins(
            24,
            24,
            24,
            24
        )

        title_label = QLabel(
            "🎉 Great Reading Session!"
        )

        title_label.setAlignment(
            Qt.AlignCenter
        )

        title_label.setObjectName(
            "dialogTitle"
        )

        layout.addWidget(
            title_label
        )

        book_label = QLabel(title)

        book_label.setAlignment(
            Qt.AlignCenter
        )

        book_label.setObjectName(
            "dialogBook"
        )

        layout.addWidget(book_label)

        pages_label = QLabel(
            f"📖 {pages} Pages Read"
        )

        pages_label.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            pages_label
        )

        duration_label = QLabel(
            f"⏱ {duration} Minute{'s' if duration > 1 else ''}"
        )

        duration_label.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            duration_label
        )

        layout.addSpacing(10)

        note_button = QPushButton(
            "📝 Add Note"
        )

        note_button.setToolTip(
            "Save your thoughts about this reading session."
        )

        note_button.setMinimumHeight(40)


        quote_button = QPushButton(
            "💬 Add Quote"
        )

        quote_button.setToolTip(
            "Save a memorable quote from this session."
        )

        quote_button.setMinimumHeight(40)


        done_button = QPushButton(
            "Done"
        )

        done_button.setMinimumHeight(40)

        note_button.clicked.connect(
            self.note_clicked
        )

        quote_button.clicked.connect(
            self.quote_clicked
        )

        done_button.clicked.connect(
            self.accept
        )

        layout.addWidget(
            note_button
        )

        layout.addWidget(
            quote_button
        )

        layout.addWidget(
            done_button
        )

        self.setLayout(layout)

    def note_clicked(self):

        self.result_action = self.NOTE

        self.accept()

    def quote_clicked(self):

        self.result_action = self.QUOTE

        self.accept()