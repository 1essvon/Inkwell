import os
from pathlib import Path
import sqlite3
import tempfile
import unittest
import zipfile
from types import SimpleNamespace
from unittest import mock


_profile = tempfile.TemporaryDirectory(prefix="inkwell-backup-tests-")
os.environ["XDG_CONFIG_HOME"] = str(Path(_profile.name) / "config")
os.environ["XDG_DATA_HOME"] = str(Path(_profile.name) / "data")
os.environ["HOME"] = str(Path(_profile.name) / "home")

from app.services.backup_service import BackupService
from app.storage_config import StorageConfig
from tests.backup_test_helpers import create_fixture_database, create_fixture_storage


class BackupServiceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="inkwell-backup-case-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name)
        self.active = self.base / "active"
        self.active.mkdir()
        create_fixture_storage(self.active)
        self.config = StorageConfig(
            config_path=self.base / "config" / "storage.json",
            user_data_directory=self.base / "user-data",
        )
        self.config.save_storage_root(self.active)
        self.config.storage_root()
        self.config_patch = mock.patch("app.services.backup_service.storage_config", self.config)
        self.config_patch.start()
        self.addCleanup(self.config_patch.stop)
        self.dispose_patch = mock.patch("app.services.backup_service.engine.dispose")
        self.dispose_patch.start()
        self.addCleanup(self.dispose_patch.stop)

    def _book_title(self, database):
        with sqlite3.connect(database) as connection:
            return connection.execute("SELECT title FROM books").fetchone()[0]

    def _assert_active_unchanged(self, db_bytes, cover_bytes):
        self.assertEqual((self.active / "inkwell.db").read_bytes(), db_bytes)
        self.assertEqual(
            (self.active / "data" / "covers" / "cover-1.jpg").read_bytes(),
            cover_bytes,
        )

    def test_backup_contains_consistent_database_and_referenced_cover(self):
        destination = self.base / "export" / "library.zip"
        before_title = self._book_title(self.active / "inkwell.db")

        self.assertTrue(BackupService.export_database(str(destination)))

        with zipfile.ZipFile(destination) as archive:
            self.assertEqual(set(archive.namelist()), {"inkwell.db", "data/covers/cover-1.jpg"})
            extracted = self.base / "check.db"
            extracted.write_bytes(archive.read("inkwell.db"))
            self.assertEqual(archive.read("data/covers/cover-1.jpg"), b"cover-fixture")
        self.assertEqual(self._book_title(extracted), before_title)
        self.assertEqual(self._book_title(self.active / "inkwell.db"), before_title)

    def test_restore_preserves_database_data_and_relative_cover_path(self):
        archive_path = self.base / "source.zip"
        self.assertTrue(BackupService.export_database(str(archive_path)))
        target = self.base / "restored"
        target.mkdir()
        target_config = StorageConfig(
            config_path=self.base / "restore-config" / "storage.json",
            user_data_directory=self.base / "restore-data",
        )
        target_config.save_storage_root(target)
        target_config.storage_root()
        with mock.patch("app.services.backup_service.storage_config", target_config):
            self.assertTrue(BackupService.import_database(str(archive_path)))

        self.assertEqual(self._book_title(target / "inkwell.db"), "Fixture Book")
        with sqlite3.connect(target / "inkwell.db") as connection:
            cover_path = connection.execute("SELECT cover_path FROM books").fetchone()[0]
        self.assertEqual(cover_path, "data/covers/cover-1.jpg")
        self.assertEqual((target / cover_path).read_bytes(), b"cover-fixture")

    def test_restore_rejects_active_database_as_source(self):
        with self.assertRaisesRegex(ValueError, "Select a ZIP backup"):
            BackupService.import_database(str(self.active / "inkwell.db"))

    def test_rejects_unsafe_cover_references_without_changing_active_storage(self):
        cases = (
            ("/tmp/cover.jpg", "absolute cover_path"),
            ("outside/cover.jpg", "outside data/covers"),
            ("data/covers/../secret.jpg", "unsafe cover_path"),
        )
        for cover_path, error in cases:
            with self.subTest(cover_path=cover_path):
                db_bytes = (self.active / "inkwell.db").read_bytes()
                cover_bytes = (self.active / "data" / "covers" / "cover-1.jpg").read_bytes()
                candidate = self.base / "candidate.db"
                create_fixture_database(candidate, cover_path=cover_path)
                with self.assertRaisesRegex(ValueError, error):
                    BackupService._validate_database(candidate, self.base)
                self._assert_active_unchanged(db_bytes, cover_bytes)

    def test_rejects_missing_referenced_cover(self):
        (self.active / "data" / "covers" / "cover-1.jpg").unlink()
        destination = self.base / "missing-cover.zip"
        with self.assertRaisesRegex(ValueError, "Referenced cover is missing"):
            BackupService.export_database(str(destination))
        self.assertFalse(destination.exists())

    def test_backup_excludes_unreferenced_cover_files(self):
        (self.active / "data" / "covers" / "unused.jpg").write_bytes(b"not-referenced")
        destination = self.base / "referenced-only.zip"
        self.assertTrue(BackupService.export_database(str(destination)))
        with zipfile.ZipFile(destination) as archive:
            self.assertEqual(
                set(archive.namelist()),
                {"inkwell.db", "data/covers/cover-1.jpg"},
            )

    def _write_archive(self, path, members):
        with zipfile.ZipFile(path, "w") as archive:
            for name, data in members:
                archive.writestr(name, data)

    def test_restore_rejects_archive_missing_a_referenced_cover(self):
        db_path = self.base / "only-db.db"
        create_fixture_database(db_path)
        archive_path = self.base / "missing-cover-entry.zip"
        self._write_archive(archive_path, [("inkwell.db", db_path.read_bytes())])
        db_bytes = (self.active / "inkwell.db").read_bytes()
        cover_bytes = (self.active / "data" / "covers" / "cover-1.jpg").read_bytes()

        with self.assertRaisesRegex(ValueError, "Backup is missing referenced cover"):
            BackupService.import_database(str(archive_path))

        self._assert_active_unchanged(db_bytes, cover_bytes)

    def test_insufficient_staging_space_is_rejected_before_replacement(self):
        archive_path = self.base / "source.zip"
        self.assertTrue(BackupService.export_database(str(archive_path)))
        db_bytes = (self.active / "inkwell.db").read_bytes()
        cover_bytes = (self.active / "data" / "covers" / "cover-1.jpg").read_bytes()
        with mock.patch(
            "app.services.backup_service.shutil.disk_usage",
            return_value=SimpleNamespace(free=0),
        ):
            with self.assertRaisesRegex(ValueError, "available space"):
                BackupService.import_database(str(archive_path))
        self._assert_active_unchanged(db_bytes, cover_bytes)
        self.assertEqual(list(self.active.glob(".inkwell-restore-*")), [])

    def test_rejects_malicious_archives_and_keeps_active_files_unchanged(self):
        db_bytes = (self.active / "inkwell.db").read_bytes()
        cover_bytes = (self.active / "data" / "covers" / "cover-1.jpg").read_bytes()
        valid_db = self.base / "valid.db"
        create_fixture_database(valid_db)
        db_data = valid_db.read_bytes()
        cases = [
            ([ ("../escape", b"bad"), ("inkwell.db", db_data) ], "unsafe path"),
            ([ ("inkwell.db", db_data), ("inkwell.db", db_data) ], "duplicate path"),
            ([ ("inkwell.db", db_data), ("data/covers/link.jpg", b"x") ], None),
            ([ ("data/covers/cover-1.jpg", b"x") ], "does not contain inkwell.db"),
            ([ ("inkwell.db", b"not sqlite") ], "not a valid Inkwell SQLite database"),
            ([ ("inkwell.db", db_data), ("data/covers/cover-1.jpg", b"wrong"), ("data/covers/cover-1.jpg", b"duplicate") ], "duplicate path"),
        ]
        for index, (members, expected) in enumerate(cases):
            with self.subTest(index=index):
                archive_path = self.base / f"bad-{index}.zip"
                self._write_archive(archive_path, members)
                if index == 2:
                    # Unix symlink marker in the ZIP external attributes.
                    with zipfile.ZipFile(archive_path, "w") as archive:
                        archive.writestr("inkwell.db", db_data)
                        info = zipfile.ZipInfo("data/covers/link.jpg")
                        info.create_system = 3
                        info.external_attr = (0o120777 << 16)
                        archive.writestr(info, b"target")
                with self.assertRaises(ValueError) as caught:
                    BackupService.import_database(str(archive_path))
                if expected:
                    self.assertIn(expected, str(caught.exception))
                self._assert_active_unchanged(db_bytes, cover_bytes)

    def test_rejects_sqlite_without_full_application_schema(self):
        db_path = self.base / "partial.db"
        with sqlite3.connect(db_path) as connection:
            connection.execute("CREATE TABLE books (id INTEGER PRIMARY KEY)")
        with self.assertRaisesRegex(ValueError, "missing required Inkwell tables"):
            BackupService._validate_database(db_path, self.base)

    def test_failed_cover_replacement_rolls_back_and_cleans_staging(self):
        archive_path = self.base / "source.zip"
        self.assertTrue(BackupService.export_database(str(archive_path)))
        old_cover = self.active / "data" / "covers" / "cover-1.jpg"
        old_cover.write_bytes(b"old-cover")
        create_fixture_database(self.active / "inkwell.db", title="Old Active Book")
        real_replace = os.replace
        failed = False

        def replace_with_one_failure(source, destination):
            nonlocal failed
            source_path = Path(source)
            destination_path = Path(destination)
            if (
                not failed
                and source_path.name == "covers"
                and source_path.parent.name == "data"
                and destination_path == self.active / "data" / "covers"
            ):
                failed = True
                raise OSError("simulated covers replacement failure")
            return real_replace(source, destination)

        with mock.patch("app.services.backup_service.os.replace", side_effect=replace_with_one_failure):
            with self.assertRaisesRegex(OSError, "simulated covers replacement failure"):
                BackupService.import_database(str(archive_path))

        self.assertTrue(failed)
        self.assertEqual(self._book_title(self.active / "inkwell.db"), "Old Active Book")
        self.assertEqual(old_cover.read_bytes(), b"old-cover")
        self.assertEqual(list(self.active.glob(".inkwell-restore-*")), [])


if __name__ == "__main__":
    unittest.main()
