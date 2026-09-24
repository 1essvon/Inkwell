import os
from pathlib import Path
import shutil
import sqlite3
import tempfile

from app.database.engine import engine


class BackupService:

    @staticmethod
    def export_database(
        destination: str
    ) -> bool:

        source = Path(
            engine.url.database
        )

        if not source.exists():

            return False

        destination_path = Path(
            destination
        )

        shutil.copy2(

            source,

            destination_path

        )

        return True

    @staticmethod
    def import_database(
        source: str
    ) -> bool:

        source_path = Path(
            source
        )

        if not source_path.is_file():

            return False

        database_name = engine.url.database

        if not database_name or database_name == ":memory:":
            raise ValueError(
                "The active database does not have a file path."
            )

        target_path = Path(database_name)

        if source_path.resolve() == target_path.resolve():
            raise ValueError(
                "The selected backup is already the active database."
            )

        descriptor, staging_name = tempfile.mkstemp(
            prefix=f".{target_path.name}.restore-",
            suffix=".tmp",
            dir=str(target_path.parent),
        )
        os.close(descriptor)

        staging_path = Path(staging_name)

        try:
            shutil.copy2(
                source_path,
                staging_path,
            )

            BackupService._validate_sqlite_database(
                staging_path
            )

            # All app services close their local sessions. Dispose idle pooled
            # connections before replacing the file; future sessions can use
            # this same Engine and will open fresh connections.
            engine.dispose()

            # The staging file is in the target directory, so replacement is
            # atomic on the same filesystem and the old DB remains intact if
            # validation or replacement fails.
            os.replace(
                staging_path,
                target_path,
            )
        finally:
            if staging_path.exists():
                staging_path.unlink()

        return True

    @staticmethod
    def _validate_sqlite_database(
        path: Path
    ) -> None:

        database_uri = f"{path.resolve().as_uri()}?mode=ro"

        try:
            connection = sqlite3.connect(
                database_uri,
                uri=True,
            )
            try:
                result = connection.execute(
                    "PRAGMA quick_check"
                ).fetchone()
            finally:
                connection.close()
        except sqlite3.DatabaseError as error:
            raise ValueError(
                "The selected file is not a valid SQLite database."
            ) from error

        if result is None or result[0] != "ok":
            raise ValueError(
                "The selected SQLite database failed its integrity check."
            )
