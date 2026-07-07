from PySide6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QGroupBox,
    QComboBox,
    QCheckBox,
    QPushButton,
    QMessageBox,
)

from app.services.settings_service import (
    SettingsService,
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

        title = QLabel("Settings")
        title.setObjectName("pageTitle")
        layout.addWidget(title)

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

    # ==========================
    # Save
    # ==========================

    def save(self):

        SettingsService.save(

            theme=self.theme_combo.currentText(),

            autosave=self.autosave_checkbox.isChecked(),

            confirm_clear=(
                self.confirm_checkbox.isChecked()
            ),

        )

        QMessageBox.information(

            self,

            "Settings",

            "Settings saved."

        )

    # ==========================
    # Refresh
    # ==========================

    def refresh(self):

        self.load()