from PySide6.QtCore import Qt
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
    QFileDialog,
)

from app.services.settings_service import (
    SettingsService,
)
from app.services.backup_service import (
    BackupService,
)
from app.services.storage_service import (
    StorageService,
)
from app.storage_config import storage_config

from app.ui.components.page_header import (
    PageHeader,
)


class SettingsView(QWidget):

    def __init__(self):

        super().__init__()

        self.settings = None
        self.pending_storage_root = None

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
        # Storage
        # --------------------------

        storage_group = QGroupBox(
            "Storage"
        )

        storage_layout = QVBoxLayout()

        self.storage_root_label = QLabel()
        self.storage_root_label.setObjectName(
            "secondaryText"
        )
        self.storage_root_label.setWordWrap(True)
        self.storage_root_label.setTextInteractionFlags(
            Qt.TextInteractionFlag.TextSelectableByMouse
        )

        storage_layout.addWidget(
            self.storage_root_label
        )

        self.change_storage_button = QPushButton(
            "Change Storage Location"
        )
        self.change_storage_button.clicked.connect(
            self.change_storage_location
        )

        storage_layout.addWidget(
            self.change_storage_button
        )

        storage_group.setLayout(
            storage_layout
        )

        layout.addWidget(
            storage_group
        )

        # --------------------------
        # Backup
        # --------------------------

        backup_group = QGroupBox(
            "Backup"
        )

        backup_layout = QVBoxLayout()

        self.backup_button = QPushButton(
            "Backup Database and Covers"
        )

        self.backup_button.clicked.connect(
            self.backup_database
        )

        backup_layout.addWidget(
            self.backup_button
        )

        self.restore_button = QPushButton(
            "Restore Backup"
        )

        self.restore_button.clicked.connect(
            self.restore_database
        )

        backup_layout.addWidget(
            self.restore_button
        )

        backup_group.setLayout(
            backup_layout
        )

        layout.addWidget(
            backup_group
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

        self.update_storage_display()

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
    # Backup
    # ==========================

    def backup_database(self):

        destination, _selected_filter = (
            QFileDialog.getSaveFileName(
                self,
                "Backup Database and Covers",
                "inkwell_backup.zip",
                "Inkwell Backup (*.zip)",
            )
        )

        if not destination:
            return

        try:
            success = BackupService.export_database(
                destination
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                "Backup Failed",
                f"Complete backup failed: {error}",
            )
            return

        if not success:
            QMessageBox.critical(
                self,
                "Backup Failed",
                "Backup failed. The active database file could not be found.",
            )
            return

        QMessageBox.information(
            self,
            "Backup Complete",
            f"Complete backup saved to:\n{destination}",
        )

    def restore_database(self):

        source, _selected_filter = (
            QFileDialog.getOpenFileName(
                self,
                "Restore Backup",
                "",
                "Inkwell Backup (*.zip)",
            )
        )

        if not source:
            return

        reply = QMessageBox.question(
            self,
            "Confirm Complete Restore",
            (
                "Restoring this backup will replace the application's database "
                "and cover files. This cannot be undone. Continue?"
            ),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply != QMessageBox.Yes:
            return

        try:
            success = BackupService.import_database(
                source
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                "Restore Failed",
                f"Restore failed. The current database and covers were rolled back where possible.\n\n{error}",
            )
            return

        if not success:
            QMessageBox.critical(
                self,
                "Restore Failed",
                "The selected backup file could not be found. Current data was not replaced.",
            )
            return

        QMessageBox.information(
            self,
            "Restore Complete",
            (
                "The database and covers were restored successfully. "
                "Please restart The Inkwell before continuing."
            ),
        )

    def change_storage_location(self):

        active_root = storage_config.storage_root()
        destination = QFileDialog.getExistingDirectory(
            self,
            "Choose Storage Folder",
            str(active_root.parent),
            QFileDialog.Option.ShowDirsOnly,
        )

        if not destination:
            return

        try:
            destination = StorageService.validate_destination(
                destination
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                "Invalid Storage Folder",
                f"This folder cannot be used for storage migration:\n{error}",
            )
            return

        reply = QMessageBox.question(
            self,
            "Confirm Storage Migration",
            (
                "Inkwell will copy the database and cover files to:\n\n"
                f"{destination}\n\n"
                "The current storage will remain unchanged. The new location "
                "will become active after restarting the application. Continue?"
            ),
            QMessageBox.Yes | QMessageBox.No,
            QMessageBox.No,
        )

        if reply != QMessageBox.Yes:
            return

        try:
            migrated_root = StorageService.migrate_storage(
                destination
            )
        except Exception as error:
            QMessageBox.critical(
                self,
                "Storage Migration Failed",
                (
                    "Storage was not changed. The current root remains active.\n\n"
                    f"{error}"
                ),
            )
            return

        self.pending_storage_root = migrated_root
        self.change_storage_button.setEnabled(False)
        self.update_storage_display()

        QMessageBox.information(
            self,
            "Storage Migration Complete",
            (
                "The database and cover files were copied successfully to:\n\n"
                f"{migrated_root}\n\n"
                "Restart The Inkwell for the new storage root to become active."
            ),
        )

    def update_storage_display(self):

        active_root = storage_config.storage_root()

        if self.pending_storage_root is not None:
            self.storage_root_label.setText(
                f"Active until restart: {active_root}\n"
                f"Configured after restart: {self.pending_storage_root}"
            )
            return

        self.storage_root_label.setText(
            f"Active storage root: {active_root}"
        )

    # ==========================
    # Refresh
    # ==========================

    def refresh(self):

        self.load()
        self.update_storage_display()
