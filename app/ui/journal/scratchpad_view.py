from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QScrollArea,
    QSplitter,
    QComboBox,
    QPushButton,
)

from PySide6.QtGui import (
    QShortcut,
    QKeySequence,
)

from app.services.scratchpad_service import (
    ScratchpadService,
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

from app.ui.journal.scratchpad_list_widget import (
    ScratchpadListWidget,
)

from app.ui.journal.scratchpad_detail_view import (
    ScratchpadDetailView,
)

class ScratchpadView(QWidget):

    def __init__(self):

        super().__init__()

        self.selected_entry = None

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

        self.header = PageHeader(
            "Scratchpad"
        )

        self.content_layout.addWidget(
            self.header
        )

        self.toolbar = Toolbar()

        self.search = SearchBar(
            "Search scratchpads..."
        )

        self.sort_filter = QComboBox()

        self.sort_filter.addItems(

            [

                "Newest",

                "Oldest",

                "Title",

            ]

        )

        self.new_button = QPushButton(
            "New Scratchpad"
        )

        self.toolbar.add_widget(
            self.search
        )

        self.toolbar.add_widget(
            self.sort_filter
        )

        self.toolbar.add_stretch()

        self.toolbar.add_widget(
            self.new_button
        )

        self.content_layout.addWidget(
            self.toolbar
        )

        self.splitter = QSplitter()

        self.list_widget = ScratchpadListWidget()

        self.detail_view = ScratchpadDetailView()

        self.empty_state = EmptyState(

            icon="📝",

            title="No Scratchpads Yet",

            subtitle=(
                "Create a scratchpad\n"
                "for your thoughts and ideas."
            )

        )

        self.empty_state.hide()

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
            self.list_widget
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

        new_shortcut = QShortcut(
            QKeySequence("Ctrl+N"),
            self,
        )

        new_shortcut.activated.connect(
            self.create_entry
        )


    def connect_signals(self):

        self.new_button.clicked.connect(
            self.create_entry
        )

        self.list_widget.entry_selected.connect(
            self.show_entry
        )

        self.detail_view.entry_saved.connect(
            self.refresh
        )

        self.detail_view.entry_deleted.connect(
            self.refresh
        )

        # Sprint berikutnya
        # self.search.textChanged.connect(
        #     self.filter_entries
        # )

        # Sprint berikutnya
        # self.sort_filter.currentIndexChanged.connect(
        #     self.sort_entries
        # )

    def refresh(self):

        current_id = None

        if self.selected_entry:

            current_id = self.selected_entry.id

        self.load_entries()

        if current_id:

            self.select_entry(current_id)

    def load_entries(self):

        entries = ScratchpadService.get_all_entries()

        self.list_widget.set_entries(
            entries
        )

        if entries and self.selected_entry is None:

            self.list_widget.select_first()

        else:

            self.selected_entry = None

            self.detail_view.clear()

        self.update_empty_state()

    def show_entry(
        self,
        entry,
    ):

        self.selected_entry = entry

        self.detail_view.display_entry(
            entry
        )

        self.detail_view.entry_saved.connect(
            self.refresh
        )

    def create_entry(self):

        entry = ScratchpadService.create_entry()

        self.refresh()

        self.select_entry(
            entry.id
        )

        self.detail_view.title.setFocus()

        self.detail_view.title.selectAll()

    def select_entry(
        self,
        entry_id,
    ):

        for row in range(
            self.list_widget.count()
        ):

            item = self.list_widget.item(
                row
            )

            if item.entry.id == entry_id:

                self.list_widget.setCurrentRow(
                    row
                )

                break

    def update_empty_state(self):

        has_entries = self.list_widget.count() > 0

        self.list_widget.setVisible(
            has_entries
        )

        self.detail_view.setVisible(
            has_entries
        )

        self.empty_state.setVisible(
            not has_entries
        )