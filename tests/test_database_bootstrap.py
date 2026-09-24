import hashlib
import logging
import os
from pathlib import Path
import sqlite3
import tempfile
import unittest
from unittest import mock

from sqlalchemy import create_engine
from sqlalchemy.engine import URL

from app.database import init_db as database_init


ACTIVE_REVISION = "c3e91f7a4b26"


class DatabaseBootstrapTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.root = Path(self.temporary_directory.name)
        self.database_path = self.root / "storage" / "inkwell.db"
        self.database_path.parent.mkdir()
        self.engine = create_engine(
            URL.create("sqlite", database=str(self.database_path))
        )
        self.addCleanup(self.engine.dispose)
        self.engine_patch = mock.patch.object(
            database_init,
            "engine",
            self.engine,
        )
        self.engine_patch.start()
        self.addCleanup(self.engine_patch.stop)

    def _connect(self):
        return sqlite3.connect(self.database_path)

    def _initialize(self):
        database_init.init_database()

    def _assert_current_schema(self):
        with self._connect() as connection:
            tables = {
                row[0]
                for row in connection.execute(
                    "SELECT name FROM sqlite_master WHERE type = 'table'"
                )
            }
            revision = connection.execute(
                "SELECT version_num FROM alembic_version"
            ).fetchone()[0]
            result = connection.execute("PRAGMA quick_check").fetchone()[0]

        self.assertEqual(
            tables,
            {
                "alembic_version",
                "books",
                "notes",
                "quotes",
                "reading_sessions",
                "scratchpad_entries",
                "app_settings",
            },
        )
        self.assertEqual(revision, ACTIVE_REVISION)
        self.assertEqual(result, "ok")

    def _assert_no_staging_files(self):
        self.assertEqual(
            list(self.database_path.parent.glob(".inkwell.db.bootstrap-*.db*")),
            [],
        )

    def test_missing_database_is_migrated_in_storage_root(self):
        working_directory = self.root / "cwd"
        working_directory.mkdir()
        previous_directory = Path.cwd()
        try:
            os.chdir(working_directory)
            self._initialize()
        finally:
            os.chdir(previous_directory)

        self._assert_current_schema()
        self.assertFalse((working_directory / "inkwell.db").exists())
        self._assert_no_staging_files()

    def test_existing_empty_sqlite_file_is_atomically_initialized(self):
        self.database_path.touch()

        self._initialize()

        self._assert_current_schema()
        self._assert_no_staging_files()

    def test_database_at_active_revision_is_not_migrated_again(self):
        self._initialize()
        with mock.patch.object(
            database_init.command,
            "upgrade",
            side_effect=AssertionError("baseline must not run twice"),
        ):
            self._initialize()

        self._assert_current_schema()

    def test_tables_without_revision_fail_closed_without_modification(self):
        with self._connect() as connection:
            connection.execute("CREATE TABLE books (id INTEGER PRIMARY KEY)")
        before = hashlib.sha256(self.database_path.read_bytes()).digest()

        with self.assertRaisesRegex(
            database_init.DatabaseBootstrapError,
            "no Alembic revision",
        ):
            self._initialize()

        self.assertEqual(hashlib.sha256(self.database_path.read_bytes()).digest(), before)
        self._assert_no_staging_files()

    def test_unknown_revision_fails_closed_without_modification(self):
        with self._connect() as connection:
            connection.execute(
                "CREATE TABLE alembic_version (version_num VARCHAR(32) NOT NULL)"
            )
            connection.execute(
                "INSERT INTO alembic_version VALUES ('unknown-revision')"
            )
        before = hashlib.sha256(self.database_path.read_bytes()).digest()

        with self.assertRaisesRegex(
            database_init.DatabaseBootstrapError,
            "unknown or unsupported",
        ):
            self._initialize()

        self.assertEqual(hashlib.sha256(self.database_path.read_bytes()).digest(), before)
        self._assert_no_staging_files()

    def test_active_revision_with_partial_schema_fails_closed(self):
        with self._connect() as connection:
            connection.execute(
                "CREATE TABLE alembic_version (version_num VARCHAR(32) NOT NULL)"
            )
            connection.execute(
                "INSERT INTO alembic_version VALUES (?)",
                (ACTIVE_REVISION,),
            )
            connection.execute("CREATE TABLE books (id INTEGER PRIMARY KEY)")
        before = hashlib.sha256(self.database_path.read_bytes()).digest()

        with self.assertRaisesRegex(
            database_init.DatabaseBootstrapError,
            "missing application tables",
        ):
            self._initialize()

        self.assertEqual(hashlib.sha256(self.database_path.read_bytes()).digest(), before)

    def test_active_revision_with_missing_column_fails_closed(self):
        self._initialize()
        with self._connect() as connection:
            connection.execute(
                "ALTER TABLE books RENAME COLUMN title TO unexpected_title"
            )
        before = hashlib.sha256(self.database_path.read_bytes()).digest()

        with self.assertRaisesRegex(
            database_init.DatabaseBootstrapError,
            "incomplete application schema",
        ):
            self._initialize()

        self.assertEqual(hashlib.sha256(self.database_path.read_bytes()).digest(), before)

    def test_corrupt_database_fails_closed_without_modification(self):
        self.database_path.write_bytes(b"not a SQLite database")
        before = hashlib.sha256(self.database_path.read_bytes()).digest()

        with self.assertRaisesRegex(
            database_init.DatabaseBootstrapError,
            "not a valid readable SQLite",
        ):
            self._initialize()

        self.assertEqual(hashlib.sha256(self.database_path.read_bytes()).digest(), before)
        self._assert_no_staging_files()

    def test_migration_failure_preserves_missing_target_and_cleans_staging(self):
        def fail_after_partial_staging(config, _revision):
            connection = config.attributes["connection"]
            connection.exec_driver_sql("CREATE TABLE partial (id INTEGER)")
            raise RuntimeError("simulated migration failure")

        with mock.patch.object(
            database_init.command,
            "upgrade",
            side_effect=fail_after_partial_staging,
        ):
            with self.assertRaisesRegex(RuntimeError, "simulated migration failure"):
                self._initialize()

        self.assertFalse(self.database_path.exists())
        self._assert_no_staging_files()

    def test_migration_failure_preserves_existing_empty_target(self):
        self.database_path.touch()
        before = self.database_path.read_bytes()

        def fail_after_partial_staging(config, _revision):
            connection = config.attributes["connection"]
            connection.exec_driver_sql("CREATE TABLE partial (id INTEGER)")
            raise RuntimeError("simulated migration failure")

        with mock.patch.object(
            database_init.command,
            "upgrade",
            side_effect=fail_after_partial_staging,
        ):
            with self.assertRaisesRegex(RuntimeError, "simulated migration failure"):
                self._initialize()

        self.assertTrue(self.database_path.is_file())
        self.assertEqual(self.database_path.read_bytes(), before)
        self._assert_no_staging_files()

    def test_alembic_migration_does_not_replace_application_logger(self):
        application_logger = logging.getLogger("app")
        original_handlers = list(application_logger.handlers)
        original_level = application_logger.level
        original_propagate = application_logger.propagate

        self._initialize()

        self.assertEqual(application_logger.handlers, original_handlers)
        self.assertEqual(application_logger.level, original_level)
        self.assertEqual(application_logger.propagate, original_propagate)


if __name__ == "__main__":
    unittest.main()
