from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QGroupBox,
    QComboBox,
    QCheckBox,
    QPushButton,
    QMessageBox,
    QSpinBox,
)

from app.services.settings_service import (
    SettingsService,
)

from app.ui.components.page_header import (
    PageHeader,
)


class SettingsView(QWidget):

    def __init__(self):

        super().__init__()

        self.settings = None

        self.setup_ui()

        self.load()

    # ==========================
    # UI
    # ==========================

    def setup_ui(self):

        layout = QVBoxLayout(self)

        layout.setSpacing(
            16,
        )

        layout.addWidget(

            PageHeader(
                "Settings"
            )

        )

        # --------------------------
        # Appearance
        # --------------------------

        appearance_group = QGroupBox(
            "Appearance"
        )

        appearance_layout = QVBoxLayout()

        appearance_layout.addWidget(
            QLabel("Theme")
        )

        self.theme_combo = QComboBox()

        self.theme_combo.addItems(

            [
                "Dark",
            ]

        )

        appearance_layout.addWidget(
            self.theme_combo
        )

        appearance_group.setLayout(
            appearance_layout
        )

        layout.addWidget(
            appearance_group
        )

        # --------------------------
        # Scratchpad
        # --------------------------

        scratchpad_group = QGroupBox(
            "Scratchpad"
        )

        scratchpad_layout = QVBoxLayout()

        self.autosave_checkbox = (
            QCheckBox(
                "Enable Auto Save"
            )
        )

        self.confirm_checkbox = (
            QCheckBox(
                "Confirm Before Clear"
            )
        )

        scratchpad_layout.addWidget(
            self.autosave_checkbox
        )

        scratchpad_layout.addWidget(
            self.confirm_checkbox
        )

        scratchpad_group.setLayout(
            scratchpad_layout
        )

        layout.addWidget(
            scratchpad_group
        )

        # --------------------------
        # Reading Goals
        # --------------------------

        goals_group = QGroupBox(
            "Reading Goals"
        )

        goals_layout = QVBoxLayout()

        goals_layout.addWidget(
            QLabel(
                "Books per Year"
            )
        )

        self.books_goal_spin = (
            QSpinBox()
        )

        self.books_goal_spin.setRange(
            1,
            1000,
        )

        goals_layout.addWidget(
            self.books_goal_spin
        )

        goals_layout.addWidget(
            QLabel(
                "Pages per Day"
            )
        )

        self.pages_goal_spin = (
            QSpinBox()
        )

        self.pages_goal_spin.setRange(
            1,
            5000,
        )

        goals_layout.addWidget(
            self.pages_goal_spin
        )

        goals_group.setLayout(
            goals_layout
        )

        layout.addWidget(
            goals_group
        )

        # --------------------------
        # Save Button
        # --------------------------

        self.save_button = QPushButton(
            "Save Settings"
        )

        self.save_button.clicked.connect(
            self.save
        )

        layout.addWidget(
            self.save_button
        )

        layout.addStretch()

    # ==========================
    # Load
    # ==========================

    def load(self):

        self.settings = (
            SettingsService.get()
        )

        self.theme_combo.setCurrentText(

            self.settings.theme

        )

        self.autosave_checkbox.setChecked(

            self.settings.autosave_scratchpad

        )

        self.confirm_checkbox.setChecked(

            self.settings.confirm_before_clear

        )

        self.books_goal_spin.setValue(

            self.settings.reading_goal_books

        )

        self.pages_goal_spin.setValue(

            self.settings.reading_goal_pages

        )

    # ==========================
    # Save
    # ==========================

    def save(self):

        SettingsService.save(

            theme=self.theme_combo.currentText(),

            autosave=self.autosave_checkbox.isChecked(),

            confirm_clear=self.confirm_checkbox.isChecked(),

            reading_goal_books=(
                self.books_goal_spin.value()
            ),

            reading_goal_pages=(
                self.pages_goal_spin.value()
            ),

        )

        QMessageBox.information(

            self,

            "Settings",

            "Settings saved."

        )

        self.load()

    # ==========================
    # Refresh
    # ==========================

    def refresh(self):

        self.load()