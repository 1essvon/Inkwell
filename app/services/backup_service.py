from pathlib import Path
import shutil


class BackupService:

    @staticmethod
    def export_database(
        destination: str
    ) -> bool:

        source = Path(
            "inkwell.db"
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

        if not source_path.exists():

            return False

        shutil.copy2(

            source_path,

            "inkwell.db"

        )

        return True