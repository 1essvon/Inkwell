from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QPushButton,
    QComboBox,
    QScrollArea,
    QSplitter,
)

from app.services.book_service import (
    BookService,
)

from app.services.note_service import (
    NoteService,
)

from app.ui.components.empty_state import (
    EmptyState,
)

from app.ui.components.page_header import (
    PageHeader,
)

from app.ui.components.search_bar import (
    SearchBar,
)

from app.ui.components.toolbar import (
    Toolbar,
)

from app.ui.dialogs.add_note_dialog import (
    AddNoteDialog,
)

from app.ui.journal.note_detail_view import (
    NoteDetailView,
)

from app.ui.journal.note_list_widget import (
    NoteListWidget,
)


class NotesView(QWidget):

    def __init__(self):

        super().__init__()

        self.selected_note = None

        self.setup_ui()

        self.connect_signals()

        self.refresh()

    def setup_ui(self):

        self.root_layout = QVBoxLayout(self)

        self.root_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        # ======================
        # Scroll Area
        # ======================

        self.scroll = QScrollArea()

        self.scroll.setWidgetResizable(
            True
        )

        self.content = QWidget()

        self.content_layout = QVBoxLayout()

        self.content_layout.setSpacing(
            20
        )

        self.content.setLayout(
            self.content_layout
        )

        self.scroll.setWidget(
            self.content
        )

        self.root_layout.addWidget(
            self.scroll
        )

        # ======================
        # Header
        # ======================

        self.header = PageHeader(
            "Notes"
        )

        self.content_layout.addWidget(
            self.header
        )

        # ======================
        # Toolbar
        # ======================

        self.toolbar = Toolbar()

        self.search = SearchBar(
            "Search notes..."
        )

        self.book_filter = QComboBox()

        self.sort_filter = QComboBox()

        self.sort_filter.addItems(

            [

                "Newest",

                "Oldest",

                "Title",

            ]

        )

        self.add_note_button = QPushButton(
            "Add Note"
        )

        self.toolbar.add_widget(
            self.search
        )

        self.toolbar.add_widget(
            self.book_filter
        )

        self.toolbar.add_widget(
            self.sort_filter
        )

        self.toolbar.add_stretch()

        self.toolbar.add_widget(
            self.add_note_button
        )

        self.content_layout.addWidget(
            self.toolbar
        )

        # ======================
        # Main Content
        # ======================

        self.splitter = QSplitter()

        self.note_list = NoteListWidget()

        self.detail_view = NoteDetailView()

        self.empty_state = EmptyState(

            icon="📝",

            title="No Notes Yet",

            subtitle=(
                "Create your first note\n"
                "to keep track of your ideas."
            )

        )

        self.empty_state.hide()

        # Left Panel

        self.left_panel = QWidget()

        self.left_layout = QVBoxLayout()

        self.left_layout.setContentsMargins(
            0,
            0,
            0,
            0,
        )

        self.left_layout.addWidget(
            self.empty_state
        )

        self.left_layout.addWidget(
            self.note_list
        )

        self.left_panel.setLayout(
            self.left_layout
        )

        self.splitter.addWidget(
            self.left_panel
        )

        self.splitter.addWidget(
            self.detail_view
        )

        self.splitter.setStretchFactor(
            0,
            2,
        )

        self.splitter.setStretchFactor(
            1,
            3,
        )

        self.content_layout.addWidget(
            self.splitter
        )

    def connect_signals(self):

        self.add_note_button.clicked.connect(
            self.open_add_note_dialog
        )

        self.book_filter.currentIndexChanged.connect(
            self.load_notes
        )

        self.note_list.note_selected.connect(
            self.show_note
        )

        self.detail_view.note_saved.connect(
            self.refresh
        )

        self.detail_view.note_deleted.connect(
            self.refresh
        )

        # Sprint berikutnya
        # self.search.textChanged.connect(
        #     self.filter_notes
        # )

        # Sprint berikutnya
        # self.sort_filter.currentIndexChanged.connect(
        #     self.sort_notes
        # )

    def refresh(self):

        self.load_books()

        self.load_notes()

    def load_books(self):

        current_book = self.book_filter.currentData()

        self.book_filter.blockSignals(
            True
        )

        self.book_filter.clear()

        self.book_filter.addItem(
            "All Books",
            None,
        )

        books = BookService.get_all_books()

        for book in books:

            self.book_filter.addItem(
                book.title,
                book.id,
            )

        if current_book is not None:

            index = self.book_filter.findData(
                current_book
            )

            if index >= 0:

                self.book_filter.setCurrentIndex(
                    index
                )

        self.book_filter.blockSignals(
            False
        )

    def load_notes(self):

        book_id = self.book_filter.currentData()

        if book_id is None:

            notes = NoteService.get_all_notes()

        else:

            notes = NoteService.get_notes_for_book(
                book_id
            )

        self.note_list.set_notes(
            notes
        )

        if notes:

            self.note_list.select_first()

        else:

            self.selected_note = None

            self.detail_view.clear()

        self.update_empty_state()

    def show_note(
        self,
        note,
    ):

        self.selected_note = note

        self.detail_view.display_note(
            note
        )

    def open_add_note_dialog(self):

        dialog = AddNoteDialog(
            self
        )

        if dialog.exec():

            self.refresh()

    def update_empty_state(self):

        has_notes = self.note_list.count() > 0

        self.note_list.setVisible(
            has_notes
        )

        self.detail_view.setVisible(
            has_notes
        )

        self.empty_state.setVisible(
            not has_notes
        )