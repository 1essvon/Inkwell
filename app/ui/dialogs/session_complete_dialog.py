from PySide6.QtWidgets import (
    QDialog,
    QLabel,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout
)
from PySide6.QtCore import Qt
from app.ui.components.icon_provider import SIZE_INLINE, set_button_icon, pixmap

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
            "Great Reading Session!"
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
            "bookTitle"
        )

        layout.addWidget(book_label)

        pages_row = QHBoxLayout()
        pages_row.setSpacing(8)
        pages_row.addStretch()

        pages_icon = QLabel()
        pages_icon.setProperty("inkwell_icon_name", "reading")
        pages_icon.setProperty("inkwell_icon_size", SIZE_INLINE)
        pages_icon.setPixmap(pixmap("reading", size=SIZE_INLINE))
        pages_row.addWidget(pages_icon)

        pages_label = QLabel(
            f"{pages} Pages Read"
        )

        pages_label.setAlignment(
            Qt.AlignCenter
        )

        pages_row.addWidget(pages_label)
        pages_row.addStretch()
        layout.addLayout(pages_row)

        duration_label = QLabel(
            f"{duration} Minute{'s' if duration > 1 else ''}"
        )

        duration_label.setAlignment(
            Qt.AlignCenter
        )

        layout.addWidget(
            duration_label
        )

        layout.addSpacing(10)

        note_button = QPushButton(
            "Add Note"
        )
        set_button_icon(note_button, "note", size=SIZE_INLINE)

        note_button.setToolTip(
            "Save your thoughts about this reading session."
        )

        note_button.setMinimumHeight(40)


        quote_button = QPushButton(
            "Add Quote"
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