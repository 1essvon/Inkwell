from pathlib import Path, PurePosixPath, PureWindowsPath
import os
import shutil
import sqlite3
import stat
import tempfile
import zipfile

from app.database.engine import engine
from app.storage_config import storage_config


class BackupService:
    """Create and restore complete Inkwell ZIP backups."""

    DATABASE_MEMBER = "inkwell.db"
    COVERS_MEMBER = "data/covers/"
    REQUIRED_TABLE_COLUMNS = {
        "books": {
            "id", "title", "author", "isbn", "publisher", "published_year",
            "genre", "description", "page_count", "cover_path", "current_page",
            "status", "rating", "date_added", "updated_at",
        },
        "notes": {
            "id", "book_id", "page", "title", "content", "created_at", "updated_at",
        },
        "quotes": {
            "id", "book_id", "content", "page", "note", "tags", "created_at", "updated_at",
        },
        "reading_sessions": {
            "id", "book_id", "start_page", "end_page", "duration_minutes",
            "started_at", "ended_at",
        },
        "scratchpad_entries": {
            "id", "title", "content", "created_at", "updated_at",
        },
        "app_settings": {
            "id", "theme", "autosave_scratchpad", "confirm_before_clear",
            "updated_at", "reading_goal_books", "reading_goal_pages",
        },
    }

    @staticmethod
    def export_database(destination: str) -> bool:
        source = storage_config.database_path()
        if not source.is_file():
            return False

        destination_path = Path(destination)
        root = storage_config.storage_root().resolve()
        if source.is_symlink() or not source.resolve().is_relative_to(root):
            raise ValueError("The active database path is a symbolic link or is outside the storage root.")
        staging = Path(tempfile.mkdtemp(prefix=".inkwell-backup-"))
        try:
            staged_db = staging / BackupService.DATABASE_MEMBER
            BackupService._snapshot_database(source, staged_db)
            referenced = BackupService._validate_database(staged_db, staging)
            protected_paths = {source.resolve()}
            protected_paths.update((root / relative).resolve() for relative in referenced)
            if destination_path.resolve() in protected_paths:
                raise ValueError("The backup destination must not replace the active database or a referenced cover.")
            destination_path.parent.mkdir(parents=True, exist_ok=True)
            descriptor, archive_tmp_name = tempfile.mkstemp(
                prefix=f".{destination_path.name}.",
                suffix=".tmp",
                dir=destination_path.parent,
            )
            os.close(descriptor)
            archive_tmp = Path(archive_tmp_name)
            try:
                with zipfile.ZipFile(archive_tmp, "w", zipfile.ZIP_DEFLATED) as archive:
                    archive.write(staged_db, BackupService.DATABASE_MEMBER)
                    for relative in referenced:
                        live = root / relative
                        BackupService._safe_cover_path(live, root, relative)
                        if not live.is_file():
                            raise ValueError(f"Referenced cover is missing: {relative}")
                        archive.write(live, relative.as_posix())
                os.replace(archive_tmp, destination_path)
            finally:
                if archive_tmp.exists():
                    archive_tmp.unlink()
            return True
        finally:
            shutil.rmtree(staging, ignore_errors=True)

    @staticmethod
    def import_database(source: str) -> bool:
        source_path = Path(source)
        if not source_path.is_file():
            return False

        target_db = Path(storage_config.database_path())
        root = storage_config.storage_root().resolve()
        covers = root / "data" / "covers"
        if not target_db or str(target_db) == ":memory:":
            raise ValueError("The active database does not have a file path.")
        if source_path.resolve() == target_db.resolve():
            raise ValueError("Select a ZIP backup, not the active database.")
        if target_db.is_symlink() or not target_db.resolve().is_relative_to(root):
            raise ValueError("The active database path is a symbolic link or is outside the storage root.")

        staging_parent = target_db.parent
        staging = Path(tempfile.mkdtemp(prefix=".inkwell-restore-", dir=staging_parent))
        staged_db = staging / BackupService.DATABASE_MEMBER
        staged_covers = staging / "data" / "covers"
        db_old = staging / "previous.db"
        covers_old = staging / "previous-covers"
        db_installed = covers_installed = db_saved = covers_saved = False
        preserve_staging = False
        try:
            BackupService._extract_and_validate(source_path, staging, staged_db)
            referenced = BackupService._validate_database(staged_db, staging)
            for relative in referenced:
                staged_cover = staging / relative
                BackupService._safe_cover_path(staged_cover, staging, relative)
                if not staged_cover.is_file():
                    raise ValueError(f"Backup is missing referenced cover: {relative}")

            # Keep rollback copies on the same filesystem until both replacements succeed.
            covers.parent.mkdir(parents=True, exist_ok=True)
            if covers.parent.is_symlink() or covers.is_symlink():
                raise ValueError("The active data/covers path contains a symbolic link.")
            if not covers.resolve().is_relative_to(root):
                raise ValueError("The active data/covers path escapes the storage root.")
            engine.dispose()
            if target_db.exists():
                os.replace(target_db, db_old)
                db_saved = True
            if covers.exists():
                os.replace(covers, covers_old)
                covers_saved = True
            os.replace(staged_db, target_db)
            db_installed = True
            if staged_covers.exists():
                os.replace(staged_covers, covers)
                covers_installed = True
            else:
                covers.mkdir(parents=True)
                covers_installed = True
        except Exception as restore_error:
            # Restore both original paths if any installation step failed.
            rollback_errors = []
            try:
                if covers_installed:
                    BackupService._remove_path(covers)
                if covers_saved and covers_old.exists():
                    os.replace(covers_old, covers)
            except OSError as error:
                rollback_errors.append(f"covers: {error}")
            try:
                if db_installed:
                    BackupService._remove_path(target_db)
                if db_saved and db_old.exists():
                    os.replace(db_old, target_db)
            except OSError as error:
                rollback_errors.append(f"database: {error}")
            engine.dispose()
            if rollback_errors:
                preserve_staging = True
                details = "; ".join(rollback_errors)
                raise RuntimeError(
                    "Restore failed and rollback was incomplete. Recovery copies "
                    f"were preserved at {staging}: {details}"
                ) from restore_error
            raise
        finally:
            if not preserve_staging:
                shutil.rmtree(staging, ignore_errors=True)
        return True

    @staticmethod
    def _snapshot_database(source: Path, destination: Path) -> None:
        src = dst = None
        try:
            src = sqlite3.connect(f"{source.resolve().as_uri()}?mode=ro", uri=True)
            dst = sqlite3.connect(destination)
            src.backup(dst)
        except sqlite3.DatabaseError as error:
            raise ValueError(f"Could not create a consistent SQLite snapshot: {error}") from error
        finally:
            if dst is not None:
                dst.close()
            if src is not None:
                src.close()

    @staticmethod
    def _validate_database(database: Path, package_root: Path) -> tuple[Path, ...]:
        connection = None
        try:
            connection = sqlite3.connect(f"{database.resolve().as_uri()}?mode=ro", uri=True)
            checks = connection.execute("PRAGMA quick_check").fetchall()
            if not checks or any(row[0] != "ok" for row in checks):
                raise ValueError("The SQLite database failed its integrity check.")
            tables = {row[0] for row in connection.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )}
            missing_tables = set(BackupService.REQUIRED_TABLE_COLUMNS) - tables
            if missing_tables:
                raise ValueError(
                    "The SQLite database is missing required Inkwell tables: "
                    + ", ".join(sorted(missing_tables))
                )
            for table, required_columns in BackupService.REQUIRED_TABLE_COLUMNS.items():
                actual_columns = {
                    row[1] for row in connection.execute(f'PRAGMA table_info("{table}")')
                }
                missing_columns = required_columns - actual_columns
                if missing_columns:
                    raise ValueError(
                        f"The SQLite database table {table} is missing required columns: "
                        + ", ".join(sorted(missing_columns))
                    )
            foreign_key_errors = connection.execute("PRAGMA foreign_key_check").fetchall()
            if foreign_key_errors:
                raise ValueError("The SQLite database contains broken foreign key references.")
            paths = connection.execute(
                "SELECT id, cover_path FROM books WHERE cover_path IS NOT NULL"
            ).fetchall()
            relatives = set()
            for book_id, cover_text in paths:
                relative = BackupService._cover_relative(cover_text, book_id)
                BackupService._safe_cover_path(package_root / relative, package_root, relative)
                relatives.add(relative)
            return tuple(sorted(relatives, key=lambda path: path.as_posix()))
        except sqlite3.DatabaseError as error:
            raise ValueError("The selected file is not a valid Inkwell SQLite database.") from error
        finally:
            if connection is not None:
                connection.close()

    @staticmethod
    def _cover_relative(value: str, book_id: object) -> Path:
        posix = PurePosixPath(value)
        windows = PureWindowsPath(value)
        if posix.is_absolute() or windows.is_absolute() or windows.drive:
            raise ValueError(f"Book {book_id} has an absolute cover_path: {value}")
        parts = posix.parts
        if not parts or any(part in ("", ".", "..") for part in parts):
            raise ValueError(f"Book {book_id} has an unsafe cover_path: {value}")
        if parts[:2] != ("data", "covers"):
            raise ValueError(f"Book {book_id} cover_path is outside data/covers: {value}")
        return Path(*parts)

    @staticmethod
    def _safe_cover_path(path: Path, root: Path, relative: Path) -> None:
        if not path.resolve().is_relative_to(root.resolve()):
            raise ValueError(f"Cover path escapes its storage root: {relative}")
        cursor = root
        for part in relative.parts:
            cursor = cursor / part
            if cursor.is_symlink():
                raise ValueError(f"Symbolic links are not allowed in cover paths: {relative}")

    @staticmethod
    def _extract_and_validate(archive_path: Path, staging: Path, staged_db: Path) -> None:
        try:
            with zipfile.ZipFile(archive_path) as archive:
                members = archive.infolist()
                names = set()
                for member in members:
                    name = member.filename
                    if name in names:
                        raise ValueError(f"Backup contains a duplicate path: {name}")
                    path = PurePosixPath(name)
                    windows_path = PureWindowsPath(name)
                    raw_parts = name.split("/")
                    if member.is_dir() and raw_parts[-1] == "":
                        raw_parts = raw_parts[:-1]
                    if (
                        "\\" in name
                        or path.is_absolute()
                        or windows_path.is_absolute()
                        or windows_path.drive
                        or any(part in (".", "..", "") for part in raw_parts)
                        or any(part == ".." for part in windows_path.parts)
                    ):
                        raise ValueError(f"Backup contains an unsafe path: {name}")
                    canonical_name = "/".join(raw_parts)
                    if canonical_name in names:
                        raise ValueError(f"Backup contains a duplicate path: {name}")
                    names.add(canonical_name)
                    if member.is_dir():
                        if canonical_name != "data/covers" and not canonical_name.startswith("data/covers/"):
                            raise ValueError(f"Unexpected backup directory: {name}")
                    elif canonical_name != BackupService.DATABASE_MEMBER and not canonical_name.startswith(BackupService.COVERS_MEMBER):
                        raise ValueError(f"Unexpected backup entry: {name}")
                    mode = member.external_attr >> 16
                    file_type = stat.S_IFMT(mode)
                    expected_type = stat.S_IFDIR if member.is_dir() else stat.S_IFREG
                    if file_type and file_type != expected_type:
                        raise ValueError(f"Backup contains a symlink or special file: {name}")
                if BackupService.DATABASE_MEMBER not in names:
                    raise ValueError("Backup does not contain inkwell.db.")
                expanded_size = sum(
                    member.file_size for member in members if not member.is_dir()
                )
                if expanded_size > shutil.disk_usage(staging).free:
                    raise ValueError(
                        "Backup contents exceed the available space for safe extraction."
                    )
                for member in members:
                    if member.is_dir():
                        continue
                    destination = staging.joinpath(*PurePosixPath(member.filename).parts)
                    destination.parent.mkdir(parents=True, exist_ok=True)
                    with archive.open(member) as input_file, destination.open("xb") as output_file:
                        shutil.copyfileobj(input_file, output_file)
        except zipfile.BadZipFile as error:
            raise ValueError("The selected file is not a valid ZIP backup.") from error

    @staticmethod
    def _remove_path(path: Path) -> None:
        if path.is_dir() and not path.is_symlink():
            shutil.rmtree(path)
        elif path.exists() or path.is_symlink():
            path.unlink()
