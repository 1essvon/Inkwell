import os
from pathlib import Path, PureWindowsPath
import shutil
import sqlite3
import tempfile

from app.database.base import Base
import app.models  # Register the application's tables in Base.metadata.
from app.storage_config import (
    storage_config,
)


class StorageMigrationError(RuntimeError):
    """Raised when a storage root cannot be copied safely."""


class StorageService:

    @staticmethod
    def validate_destination(new_root: Path | str) -> Path:
        requested_root = Path(new_root).expanduser()

        if not requested_root.is_absolute():
            raise StorageMigrationError(
                "The new storage root must be an absolute path."
            )

        destination_root = requested_root.resolve()
        source_root = storage_config.storage_root().resolve()

        if destination_root == source_root:
            raise StorageMigrationError(
                "The new storage root is already active."
            )

        if (
            destination_root.is_relative_to(source_root)
            or source_root.is_relative_to(destination_root)
        ):
            raise StorageMigrationError(
                "The new storage root cannot be inside or contain the active storage root."
            )

        if destination_root.exists():
            if not destination_root.is_dir():
                raise StorageMigrationError(
                    f"Destination is not a directory: {destination_root}"
                )

            try:
                if any(destination_root.iterdir()):
                    raise StorageMigrationError(
                        f"Destination already contains data: {destination_root}"
                    )
            except OSError as error:
                raise StorageMigrationError(
                    f"Could not inspect destination directory {destination_root}: {error}"
                ) from error

        destination_parent = destination_root.parent

        if (
            not destination_parent.is_dir()
            or not os.access(destination_parent, os.W_OK | os.X_OK)
        ):
            raise StorageMigrationError(
                f"Destination parent must be an existing writable directory: {destination_parent}"
            )

        return destination_root

    @staticmethod
    def migrate_storage(new_root: Path | str) -> Path:
        destination_root = StorageService.validate_destination(new_root)
        destination_was_empty = destination_root.is_dir()
        source_root = storage_config.storage_root().resolve()
        destination_parent = destination_root.parent

        source_database = storage_config.database_path()

        if not source_database.is_file():
            raise StorageMigrationError(
                f"Active database was not found: {source_database}"
            )

        staging_root = Path(
            tempfile.mkdtemp(
                prefix=f".{destination_root.name}.staging-",
                dir=destination_parent,
            )
        )

        try:
            staging_database = staging_root / "inkwell.db"
            StorageService._create_database_snapshot(
                source_database,
                staging_database,
            )

            relative_cover_paths = StorageService._validate_staged_database(
                staging_database,
                source_root,
            )

            source_covers = storage_config.covers_directory()
            staging_covers = staging_root / "data" / "covers"
            StorageService._copy_covers(
                source_covers,
                source_root,
                staging_covers,
            )

            for relative_path in relative_cover_paths:
                staged_cover = staging_root / relative_path

                if not staged_cover.is_file():
                    raise StorageMigrationError(
                        f"Cover was not present at its expected staged path: {relative_path}"
                    )

            # Staging is a sibling on the same filesystem. An existing empty
            # directory is removed only after the replacement is fully ready.
            if destination_was_empty:
                destination_root.rmdir()

            try:
                os.replace(
                    staging_root,
                    destination_root,
                )
            except Exception:
                if destination_was_empty and not destination_root.exists():
                    destination_root.mkdir()
                raise

            try:
                storage_config.save_storage_root(destination_root)
            except Exception as error:
                try:
                    StorageService._remove_tree(destination_root)
                    if destination_was_empty:
                        destination_root.mkdir()
                except OSError as cleanup_error:
                    raise StorageMigrationError(
                        "Could not save the new storage configuration, and the unconfigured destination could not be cleaned: "
                        f"{destination_root} ({cleanup_error})"
                    ) from error

                raise StorageMigrationError(
                    "Could not save the new storage configuration; the active root is unchanged."
                ) from error

            return destination_root

        except StorageMigrationError:
            raise
        except Exception as error:
            raise StorageMigrationError(
                f"Storage migration failed: {error}"
            ) from error
        finally:
            if staging_root.exists():
                StorageService._remove_tree(staging_root)

    @staticmethod
    def _create_database_snapshot(
        source: Path,
        destination: Path,
    ) -> None:
        source_connection = None
        destination_connection = None

        try:
            source_uri = f"{source.resolve().as_uri()}?mode=ro"
            source_connection = sqlite3.connect(
                source_uri,
                uri=True,
            )
            destination_connection = sqlite3.connect(destination)
            source_connection.backup(destination_connection)
        except sqlite3.DatabaseError as error:
            raise StorageMigrationError(
                f"Could not create a consistent SQLite snapshot: {error}"
            ) from error
        finally:
            if destination_connection is not None:
                destination_connection.close()
            if source_connection is not None:
                source_connection.close()

    @staticmethod
    def _validate_staged_database(
        database_path: Path,
        source_root: Path,
    ) -> tuple[Path, ...]:
        connection = None

        try:
            database_uri = f"{database_path.resolve().as_uri()}?mode=ro"
            connection = sqlite3.connect(
                database_uri,
                uri=True,
            )

            integrity_results = connection.execute(
                "PRAGMA quick_check"
            ).fetchall()

            if not integrity_results or any(
                row[0] != "ok" for row in integrity_results
            ):
                raise StorageMigrationError(
                    "The staged database failed SQLite quick_check."
                )

            StorageService._validate_application_schema(connection)
            return StorageService._validate_cover_paths(
                connection,
                source_root,
            )
        except sqlite3.DatabaseError as error:
            raise StorageMigrationError(
                f"The staged database cannot be opened or read: {error}"
            ) from error
        finally:
            if connection is not None:
                connection.close()

    @staticmethod
    def _validate_application_schema(
        connection: sqlite3.Connection,
    ) -> None:
        tables = {
            row[0]
            for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            )
        }

        missing_tables = set(Base.metadata.tables) - tables

        if missing_tables:
            names = ", ".join(sorted(missing_tables))
            raise StorageMigrationError(
                f"The staged database is missing application tables: {names}"
            )

        for table in Base.metadata.sorted_tables:
            escaped_name = table.name.replace('"', '""')
            columns = {
                row[1]
                for row in connection.execute(
                    f'PRAGMA table_info("{escaped_name}")'
                )
            }
            missing_columns = {
                column.name for column in table.columns
            } - columns

            if missing_columns:
                names = ", ".join(sorted(missing_columns))
                raise StorageMigrationError(
                    f"The staged database table {table.name} is missing columns: {names}"
                )

    @staticmethod
    def _validate_cover_paths(
        connection: sqlite3.Connection,
        source_root: Path,
    ) -> tuple[Path, ...]:
        source_root = source_root.resolve()
        source_covers = (source_root / "data" / "covers").resolve()
        validated_paths = set()

        for book_id, cover_value in connection.execute(
            "SELECT id, cover_path FROM books WHERE cover_path IS NOT NULL"
        ):
            cover_text = str(cover_value).strip()

            if not cover_text:
                continue

            relative_path = Path(cover_text)
            windows_path = PureWindowsPath(cover_text)

            if (
                relative_path.is_absolute()
                or windows_path.is_absolute()
                or windows_path.drive
            ):
                raise StorageMigrationError(
                    f"Book {book_id} has an absolute cover_path; migration was stopped: {cover_text}"
                )

            resolved_cover = (source_root / relative_path).resolve()

            if not StorageService._is_relative_to(
                resolved_cover,
                source_root,
            ):
                raise StorageMigrationError(
                    f"Book {book_id} has a cover_path outside the active storage root: {cover_text}"
                )

            if not StorageService._is_relative_to(
                resolved_cover,
                source_covers,
            ):
                raise StorageMigrationError(
                    f"Book {book_id} has a cover_path outside data/covers, which this migration copies: {cover_text}"
                )

            if not resolved_cover.is_file():
                raise StorageMigrationError(
                    f"Book {book_id} references a missing cover file: {cover_text}"
                )

            validated_paths.add(relative_path)

        return tuple(sorted(validated_paths, key=str))

    @staticmethod
    def _copy_covers(
        source_covers: Path,
        source_root: Path,
        staging_covers: Path,
    ) -> None:
        if source_covers.is_symlink():
            raise StorageMigrationError(
                "The active data/covers directory is a symbolic link; migration was stopped."
            )

        if source_covers.exists():
            resolved_covers = source_covers.resolve()

            if not StorageService._is_relative_to(
                resolved_covers,
                source_root.resolve(),
            ):
                raise StorageMigrationError(
                    "The active data/covers directory resolves outside the storage root."
                )

            if not source_covers.is_dir():
                raise StorageMigrationError(
                    f"The covers path is not a directory: {source_covers}"
                )

            for path in source_covers.rglob("*"):
                if path.is_symlink():
                    raise StorageMigrationError(
                        f"The covers directory contains a symbolic link: {path}"
                    )

            try:
                shutil.copytree(
                    source_covers,
                    staging_covers,
                )
            except OSError as error:
                raise StorageMigrationError(
                    f"Could not copy covers to staging: {error}"
                ) from error
        else:
            staging_covers.mkdir(
                parents=True,
                exist_ok=True,
            )

    @staticmethod
    def _remove_tree(path: Path) -> None:
        def retry_with_write_permission(function, failed_path, _error_info):
            os.chmod(failed_path, 0o700)
            function(failed_path)

        shutil.rmtree(
            path,
            onerror=retry_with_write_permission,
        )

    @staticmethod
    def _is_relative_to(path: Path, root: Path) -> bool:
        try:
            path.relative_to(root)
            return True
        except ValueError:
            return False
