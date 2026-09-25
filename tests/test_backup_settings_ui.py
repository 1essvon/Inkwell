import os
from pathlib import Path
import tempfile
import unittest
from types import SimpleNamespace
from unittest import mock

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
_profile = tempfile.TemporaryDirectory(prefix="inkwell-backup-ui-tests-")
os.environ["XDG_CONFIG_HOME"] = str(Path(_profile.name) / "config")
os.environ["XDG_DATA_HOME"] = str(Path(_profile.name) / "data")
os.environ["HOME"] = str(Path(_profile.name) / "home")

from PySide6.QtWidgets import QApplication, QMessageBox

from app.services.backup_service import BackupService
from app.services.settings_service import SettingsService
from app.storage_config import storage_config
from app.ui.settings_view import SettingsView


class BackupSettingsUiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication.instance() or QApplication([])

    def setUp(self):
        self.get_settings = mock.patch.object(
            SettingsService,
            "get",
            return_value=SimpleNamespace(
                theme="black_on_white",
                autosave_scratchpad=True,
                confirm_before_clear=True,
                reading_goal_books=12,
                reading_goal_pages=20,
            ),
        )
        self.get_settings.start()
        self.addCleanup(self.get_settings.stop)
        self.storage_root = mock.patch.object(
            storage_config,
            "storage_root",
            return_value=Path(tempfile.gettempdir()) / "inkwell-ui-test-storage",
        )
        self.storage_root.start()
        self.addCleanup(self.storage_root.stop)
        self.view = SettingsView()
        self.addCleanup(self.view.deleteLater)

    def test_cancel_backup_does_not_call_service_or_show_error(self):
        with (
            mock.patch("app.ui.settings_view.QFileDialog.getSaveFileName", return_value=("", "")),
            mock.patch.object(BackupService, "export_database") as export,
            mock.patch.object(QMessageBox, "critical") as error_message,
        ):
            self.view.backup_database()
        export.assert_not_called()
        error_message.assert_not_called()

    def test_backup_appends_zip_and_reports_success_or_failure(self):
        with (
            mock.patch("app.ui.settings_view.QFileDialog.getSaveFileName", return_value=("/tmp/manual-test", "")),
            mock.patch.object(BackupService, "export_database", return_value=True) as export,
            mock.patch.object(QMessageBox, "information") as success_message,
        ):
            self.view.backup_database()
        export.assert_called_once_with("/tmp/manual-test.zip")
        self.assertIn("/tmp/manual-test.zip", success_message.call_args.args[2])

        with (
            mock.patch("app.ui.settings_view.QFileDialog.getSaveFileName", return_value=("/tmp/manual-test.zip", "")),
            mock.patch.object(BackupService, "export_database", side_effect=OSError("disk full")) as export,
            mock.patch.object(QMessageBox, "critical") as error_message,
        ):
            self.view.backup_database()
        export.assert_called_once_with("/tmp/manual-test.zip")
        self.assertIn("disk full", error_message.call_args.args[2])

    def test_cancel_restore_file_and_confirmation_do_not_call_service(self):
        with (
            mock.patch("app.ui.settings_view.QFileDialog.getOpenFileName", return_value=("", "")),
            mock.patch.object(BackupService, "import_database") as restore,
            mock.patch.object(QMessageBox, "question") as confirm,
        ):
            self.view.restore_database()
        restore.assert_not_called()
        confirm.assert_not_called()

        with (
            mock.patch("app.ui.settings_view.QFileDialog.getOpenFileName", return_value=("/tmp/backup.zip", "")),
            mock.patch.object(QMessageBox, "question", return_value=QMessageBox.No),
            mock.patch.object(BackupService, "import_database") as restore,
        ):
            self.view.restore_database()
        restore.assert_not_called()

    def test_restore_requires_zip_and_reports_result(self):
        with (
            mock.patch("app.ui.settings_view.QFileDialog.getOpenFileName", return_value=("/tmp/backup.db", "")),
            mock.patch.object(BackupService, "import_database") as restore,
            mock.patch.object(QMessageBox, "critical") as error_message,
        ):
            self.view.restore_database()
        restore.assert_not_called()
        self.assertIn(".zip", error_message.call_args.args[2])

        with (
            mock.patch("app.ui.settings_view.QFileDialog.getOpenFileName", return_value=("/tmp/backup.zip", "")),
            mock.patch.object(QMessageBox, "question", return_value=QMessageBox.Yes),
            mock.patch.object(BackupService, "import_database", return_value=True) as restore,
            mock.patch.object(QMessageBox, "information") as success_message,
        ):
            self.view.restore_database()
        restore.assert_called_once_with("/tmp/backup.zip")
        self.assertIn("restart", success_message.call_args.args[2].lower())

        with (
            mock.patch("app.ui.settings_view.QFileDialog.getOpenFileName", return_value=("/tmp/backup.zip", "")),
            mock.patch.object(QMessageBox, "question", return_value=QMessageBox.Yes),
            mock.patch.object(BackupService, "import_database", side_effect=ValueError("invalid archive")) as restore,
            mock.patch.object(QMessageBox, "critical") as error_message,
        ):
            self.view.restore_database()
        restore.assert_called_once_with("/tmp/backup.zip")
        self.assertIn("invalid archive", error_message.call_args.args[2])


if __name__ == "__main__":
    unittest.main()
