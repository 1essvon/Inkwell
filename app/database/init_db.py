"""Prepare and validate the active application database at startup."""

import logging
import os
from pathlib import Path
import sqlite3
import tempfile
from contextlib import closing

from alembic import command
from alembic.config import Config
from alembic.script import ScriptDirectory
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL

from app.database.base import Base
from app.database.engine import engine
import app.models  # Register all application tables with Base.metadata.


logger = logging.getLogger(__name__)
_ALEMBIC_CONFIG_PATH = Path(__file__).resolve().parents[2] / "alembic.ini"


class DatabaseBootstrapError(RuntimeError):
    """Raised when the active database cannot be bootstrapped safely."""


def _alembic_config() -> Config:
    if not _ALEMBIC_CONFIG_PATH.is_file():
        raise DatabaseBootstrapError(
            f"Alembic configuration is missing: {_ALEMBIC_CONFIG_PATH}"
        )

    config = Config(str(_ALEMBIC_CONFIG_PATH))
    # env.py receives the staging connection directly. Keep Alembic's file
    # logging configuration from replacing the application's logger setup.
    config.attributes["connection"] = None
    config.attributes["configure_logger"] = False
    return config


def _active_revision() -> str:
    revision = ScriptDirectory.from_config(_alembic_config()).get_current_head()
    if not revision:
        raise DatabaseBootstrapError("Alembic has no active schema revision.")
    return revision


def _read_database_state(database_path: Path, active_revision: str) -> str:
    """Inspect SQLite without creating a missing file or modifying its contents."""
    if database_path.is_symlink():
        raise DatabaseBootstrapError(
            f"Database path must not be a symbolic link: {database_path}"
        )
    if not database_path.exists():
        return "missing"
    if not database_path.is_file():
        raise DatabaseBootstrapError(
            f"Database path is not a file: {database_path}"
        )

    uri = f"{database_path.resolve().as_uri()}?mode=ro"
    try:
        with closing(sqlite3.connect(uri, uri=True)) as connection:
            check = connection.execute("PRAGMA quick_check").fetchone()
            if not check or check[0] != "ok":
                raise DatabaseBootstrapError(
                    f"Database failed SQLite integrity check: {database_path}"
                )

            objects = {
                (row[0], row[1])
                for row in connection.execute(
                    "SELECT type, name FROM sqlite_master "
                    "WHERE name NOT LIKE 'sqlite_%'"
                )
            }
            tables = {
                name for kind, name in objects if kind == "table"
            }

            if "alembic_version" not in tables:
                if objects:
                    raise DatabaseBootstrapError(
                        "Database contains tables but has no Alembic revision; "
                        "automatic bootstrap was stopped to protect its data."
                    )
                return "empty"

            revisions = [
                row[0]
                for row in connection.execute(
                    "SELECT version_num FROM alembic_version"
                )
            ]
            expected_tables = set(Base.metadata.tables)
            missing_tables = expected_tables - tables

            if revisions != [active_revision]:
                raise DatabaseBootstrapError(
                    "Database has an unknown or unsupported Alembic revision; "
                    "automatic migration was stopped."
                )
            if missing_tables:
                missing = ", ".join(sorted(missing_tables))
                raise DatabaseBootstrapError(
                    f"Database is stamped at the active revision but is missing "
                    f"application tables: {missing}."
                )

            missing_columns = {}
            for table_name, table in Base.metadata.tables.items():
                escaped_name = table_name.replace('"', '""')
                actual_columns = {
                    row[1]
                    for row in connection.execute(
                        f'PRAGMA table_info("{escaped_name}")'
                    )
                }
                absent = {
                    column.name for column in table.columns
                } - actual_columns
                if absent:
                    missing_columns[table_name] = sorted(absent)

            if missing_columns:
                details = "; ".join(
                    f"{table}: {', '.join(columns)}"
                    for table, columns in sorted(missing_columns.items())
                )
                raise DatabaseBootstrapError(
                    "Database is stamped at the active revision but has an "
                    f"incomplete application schema ({details})."
                )

            return "current"
    except sqlite3.DatabaseError as error:
        raise DatabaseBootstrapError(
            f"Database is not a valid readable SQLite database: {database_path}"
        ) from error


def _validate_staged_database(database_path: Path, active_revision: str) -> None:
    state = _read_database_state(database_path, active_revision)
    if state != "current":
        raise DatabaseBootstrapError(
            "Staged database did not reach the complete active schema revision."
        )


def _remove_staging_files(database_path: Path) -> None:
    cleanup_errors = []
    for suffix in ("", "-journal", "-wal", "-shm"):
        candidate = Path(f"{database_path}{suffix}")
        try:
            candidate.unlink(missing_ok=True)
        except OSError as error:
            cleanup_errors.append(error)
            logger.error(
                "Could not remove database bootstrap staging file (%s)",
                type(error).__name__,
            )
    if cleanup_errors:
        raise DatabaseBootstrapError(
            "Could not completely remove database bootstrap staging files."
        ) from cleanup_errors[0]


def _migrate_to_staging(database_path: Path, active_revision: str) -> None:
    database_path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, staging_name = tempfile.mkstemp(
        prefix=f".{database_path.name}.bootstrap-",
        suffix=".db",
        dir=database_path.parent,
    )
    os.close(descriptor)
    staging_path = Path(staging_name)
    staging_engine = None

    try:
        staging_engine = create_engine(
            URL.create("sqlite", database=str(staging_path))
        )
        config = _alembic_config()
        config.attributes["connection"] = staging_engine.connect()

        try:
            command.upgrade(config, "head")
        finally:
            config.attributes["connection"].close()

        staging_engine.dispose()
        staging_engine = None
        _validate_staged_database(staging_path, active_revision)

        # Recheck after the potentially long migration. Never replace a target
        # another process populated while this staging database was prepared.
        target_state = _read_database_state(database_path, active_revision)
        if target_state == "current":
            return
        if target_state not in ("missing", "empty"):
            raise DatabaseBootstrapError(
                "Database changed during bootstrap; staged schema was not installed."
            )

        os.replace(staging_path, database_path)
        logger.info("Initialized the application database schema.")
    except Exception:
        logger.exception("Database schema bootstrap failed")
        raise
    finally:
        if staging_engine is not None:
            staging_engine.dispose()
        _remove_staging_files(staging_path)


def init_database() -> None:
    """Bootstrap a new/empty DB, or validate an existing stamped DB."""
    database_path = Path(engine.url.database).expanduser().resolve()
    active_revision = _active_revision()
    state = _read_database_state(database_path, active_revision)

    if state in ("missing", "empty"):
        _migrate_to_staging(database_path, active_revision)

    # This is reached only after a current schema is verified or the staged
    # migration was atomically installed. It preserves the existing engine and
    # SessionLocal binding used by application services.
    with engine.connect() as connection:
        connection.execute(text("SELECT 1"))
