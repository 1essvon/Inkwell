import json
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest import mock

from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from app.database.base import Base
import app.models  # Register application tables for the temporary fixture.
from app.services.storage_service import (
    StorageMigrationError,
    StorageService,
)
import app.services.storage_service as storage_service_module
from app.storage_config import StorageConfig


class StorageServiceTests(unittest.TestCase):

    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.base_path = Path(self.temporary_directory.name)
        self.source_root = self.base_path / "source"
        self.source_root.mkdir()
        self.covers_directory = self.source_root / "data" / "covers"
        self.covers_directory.mkdir(parents=True)

        self.config = StorageConfig(
            config_path=self.base_path / "config" / "storage.json",
            user_data_directory=self.base_path / "user-data",
        )
        self.config.save_storage_root(self.source_root)
        self.config.storage_root()

        # This SQLAlchemy engine and schema are created only in the test's
        # TemporaryDirectory; the application engine is never imported.
        self.fixture_engine = create_engine(
            URL.create(
                "sqlite",
                database=str(self.config.database_path()),
            )
        )
        self.addCleanup(self.fixture_engine.dispose)
        Base.metadata.create_all(self.fixture_engine)

        self.cover_relative_path = Path("data/covers/fixture-cover.jpg")
        self.cover_file = self.source_root / self.cover_relative_path
        self.cover_file.write_bytes(b"temporary cover fixture")
        self._insert_book_with_cover(self.cover_relative_path.as_posix())

        self.storage_config_patch = mock.patch.object(
            storage_service_module,
            "storage_config",
            self.config,
        )
        self.storage_config_patch.start()
        self.addCleanup(self.storage_config_patch.stop)

    def _insert_book_with_cover(self, cover_path):
        with sqlite3.connect(self.config.database_path()) as connection:
            connection.execute(
                """
                INSERT INTO books (
                    title, author, cover_path, current_page, status,
                    date_added, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    "Temporary fixture book",
                    "Test Author",
                    cover_path,
                    12,
                    "Reading",
                    "2026-01-01 00:00:00",
                    "2026-01-01 00:00:00",
                ),
            )

    def _assert_no_staging_directories(self, destination):
        staging_directories = list(
            destination.parent.glob(f".{destination.name}.staging-*")
        )
        self.assertEqual(staging_directories, [])

    def test_migrates_database_and_relative_cover_to_new_root(self):
        destination = self.base_path / "destination"

        result = StorageService.migrate_storage(destination)

        self.assertEqual(result, destination)
        self.assertTrue((destination / "inkwell.db").is_file())
        self.assertEqual(
            (destination / self.cover_relative_path).read_bytes(),
            b"temporary cover fixture",
        )
        with sqlite3.connect(destination / "inkwell.db") as connection:
            self.assertEqual(
                connection.execute(
                    "SELECT title, cover_path FROM books"
                ).fetchone(),
                ("Temporary fixture book", "data/covers/fixture-cover.jpg"),
            )
            self.assertEqual(
                connection.execute("PRAGMA quick_check").fetchone()[0],
                "ok",
            )

        self.assertTrue(self.config.database_path().is_file())
        self.assertTrue(self.cover_file.is_file())
        self.assertEqual(self.config.storage_root(), self.source_root.resolve())
        saved_config = json.loads(
            self.config.config_path.read_text(encoding="utf-8")
        )
        self.assertEqual(saved_config["storage_root"], str(destination.resolve()))
        self._assert_no_staging_directories(destination)

    def test_replaces_existing_empty_destination_directory(self):
        destination = self.base_path / "empty-destination"
        destination.mkdir()

        self.assertEqual(StorageService.migrate_storage(destination), destination)
        self.assertTrue((destination / "inkwell.db").is_file())
        self.assertTrue((destination / "data" / "covers").is_dir())

    def test_rejects_nonempty_destination_without_modifying_it(self):
        destination = self.base_path / "conflicting-destination"
        destination.mkdir()
        sentinel = destination / "keep.txt"
        sentinel.write_text("preserve", encoding="utf-8")

        with self.assertRaises(StorageMigrationError):
            StorageService.validate_destination(destination)

        self.assertEqual(sentinel.read_text(encoding="utf-8"), "preserve")
        self.assertEqual(self.config.storage_root(), self.source_root.resolve())

    def test_rejects_absolute_cover_path_and_cleans_staging(self):
        external_cover = self.base_path / "outside-cover.jpg"
        external_cover.write_bytes(b"outside")
        with sqlite3.connect(self.config.database_path()) as connection:
            connection.execute(
                "UPDATE books SET cover_path = ?",
                (str(external_cover),),
            )
        destination = self.base_path / "destination"

        with self.assertRaisesRegex(StorageMigrationError, "absolute cover_path"):
            StorageService.migrate_storage(destination)

        self.assertFalse(destination.exists())
        self.assertEqual(self.config.storage_root(), self.source_root.resolve())
        saved_config = json.loads(
            self.config.config_path.read_text(encoding="utf-8")
        )
        self.assertEqual(saved_config["storage_root"], str(self.source_root.resolve()))
        self._assert_no_staging_directories(destination)

    def test_copy_failure_keeps_active_root_and_cleans_staging(self):
        destination = self.base_path / "destination"
        with mock.patch.object(
            StorageService,
            "_copy_covers",
            side_effect=StorageMigrationError("simulated copy failure"),
        ):
            with self.assertRaisesRegex(StorageMigrationError, "simulated copy failure"):
                StorageService.migrate_storage(destination)

        self.assertFalse(destination.exists())
        self.assertTrue(self.config.database_path().is_file())
        self.assertTrue(self.cover_file.is_file())
        self.assertEqual(self.config.storage_root(), self.source_root.resolve())
        saved_config = json.loads(
            self.config.config_path.read_text(encoding="utf-8")
        )
        self.assertEqual(saved_config["storage_root"], str(self.source_root.resolve()))
        self._assert_no_staging_directories(destination)


if __name__ == "__main__":
    unittest.main()
