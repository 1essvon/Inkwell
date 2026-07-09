from PySide6.QtCore import Qt

from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QLabel,
    QPushButton,
    QMessageBox,
    QSplitter,
    QComboBox
)

from app.services.book_service import BookService

from app.ui.library.book_list_widget import (
    BookListWidget
)

from app.ui.library.book_detail_widget import (
    BookDetailWidget
)

from app.ui.dialogs.add_book_dialog import (
    AddBookDialog
)

from app.ui.dialogs.edit_book_dialog import (
    EditBookDialog
)

from app.ui.components.search_bar import (
    SearchBar
)

from app.ui.components.page_header import (
    PageHeader
)

from app.ui.components.toolbar import (
    Toolbar
)


class LibraryView(QWidget):

    # ----------------------------------
    # Initialization
    # ----------------------------------

    def __init__(self):
        super().__init__()

        self.selected_book = None

        self.setup_ui()

        self.setup_connections()

        self.refresh()

    # ----------------------------------
    # UI
    # ----------------------------------

    def setup_ui(self):

        layout = QVBoxLayout()

        # ======================
        # Title
        # ======================

        layout.addWidget(

            PageHeader(

                "Library"

            )

        )

        # ======================
        # Toolbar
        # ======================

        self.search_bar = SearchBar()

        self.filter_box = QComboBox()

        self.filter_box.addItems([
            "All",
            "Reading",
            "Want To Read",
            "Completed",
            "Paused",
            "Dropped",
        ])

        self.sort_box = QComboBox()

        self.sort_box.addItems([
            "Title",
            "Author",
            "Recently Added",
            "Recently Updated",
        ])

        self.add_button = QPushButton(
            "Add Book"
        )

        self.edit_button = QPushButton(
            "Edit Book"
        )

        self.delete_button = QPushButton(
            "Delete Book"
        )

        toolbar = Toolbar()

        toolbar.add_widget(
            self.search_bar,
            1
        )

        toolbar.add_widget(
            self.filter_box
        )

        toolbar.add_widget(
            self.sort_box
        )

        toolbar.add_stretch()

        toolbar.add_widget(
            self.edit_button
        )

        toolbar.add_widget(
            self.delete_button
        )

        toolbar.add_widget(
            self.add_button
        )

        layout.addWidget(
            toolbar
        )

        layout.addSpacing(
            12
        )

        # ======================
        # Splitter
        # ======================

        self.book_list = BookListWidget()

        self.detail_view = BookDetailWidget()

        self.splitter = QSplitter(
            Qt.Horizontal
        )

        self.splitter.setChildrenCollapsible(
            False
        )

        self.splitter.addWidget(
            self.book_list
        )

        self.splitter.addWidget(
            self.detail_view
        )

        self.splitter.setStretchFactor(
            0,
            1
        )

        self.splitter.setStretchFactor(
            1,
            1
        )

        self.splitter.setSizes([
            450,
            650
        ])

        layout.addWidget(
            self.splitter,
            1
        )

        self.setLayout(
            layout
        )

    # ----------------------------------
    # Connections
    # ----------------------------------

    def setup_connections(self):

        self.add_button.clicked.connect(
            self.open_add_book_dialog
        )

        self.edit_button.clicked.connect(
            self.open_edit_dialog
        )

        self.delete_button.clicked.connect(
            self.delete_selected_book
        )

        self.book_list.bookSelected.connect(
            self.on_book_selected
        )

        self.search_bar.textChanged.connect(
            self.on_search_changed
        )

        self.filter_box.currentTextChanged.connect(
            self.refresh
        )

        self.sort_box.currentTextChanged.connect(
            self.refresh
        )

    # ----------------------------------
    # Events
    # ----------------------------------

    def on_book_selected(
        self,
        book
    ):
        """
        Dipanggil saat user
        memilih sebuah buku.
        """

        self.selected_book = book

        self.detail_view.set_book(
            book
        )
        

    def on_search_changed(
        self,
        text
    ):
        """
        Dipanggil saat isi SearchBar berubah.
        """

        self.book_list.refresh(
            text
        )

    # ----------------------------------
    # Data
    # ----------------------------------

    def refresh(self):

        keyword = self.search_bar.text()

        status = self.filter_box.currentText()

        sort_by = self.sort_box.currentText()

        selected_id = None

        if self.selected_book:

            selected_id = self.selected_book.id

        self.book_list.refresh(

            keyword=keyword,

            status=status,

            selected_id=selected_id,

            sort_by=sort_by

        )

    # ----------------------------------
    # Dialog
    # ----------------------------------

    def open_add_book_dialog(self):

        dialog = AddBookDialog()

        if dialog.exec():

            self.refresh()

    def open_edit_dialog(self):

        if self.selected_book is None:

            return

        dialog = EditBookDialog(
            self.selected_book
        )

        if dialog.exec():

            self.refresh()

    # ----------------------------------
    # Delete
    # ----------------------------------

    def delete_selected_book(self):

        if self.selected_book is None:

            return

        reply = QMessageBox.question(
            self,
            "Delete Book",
            f'Delete "{self.selected_book.title}"?',
            QMessageBox.Yes | QMessageBox.No
        )

        if reply != QMessageBox.Yes:

            return

        BookService.delete_book(
            self.selected_book.id
        )

        self.selected_book = None

        self.detail_view.clear()

        self.refresh()