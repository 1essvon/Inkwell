import json
import os
from pathlib import Path
import tempfile

from PySide6.QtCore import QStandardPaths


class StorageConfigurationError(RuntimeError):
    """Raised when Inkwell's configured storage root cannot be used."""


class StorageConfig:

    def __init__(
        self,
        config_path: Path | str | None = None,
        user_data_directory: Path | str | None = None,
    ):
        if config_path is None:
            config_directory = QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.GenericConfigLocation
            )

            if not config_directory:
                config_directory = str(Path.home() / ".config")

            config_path = Path(config_directory) / "the-inkwell" / "storage.json"

        self.config_path = Path(config_path).expanduser().absolute()
        self.user_data_directory = (
            Path(user_data_directory).expanduser().absolute()
            if user_data_directory is not None
            else None
        )
        self._storage_root = None

    def storage_root(self) -> Path:
        if self._storage_root is None:
            self._storage_root = self._load_or_initialize()

        return self._storage_root

    def database_path(self) -> Path:
        return self.storage_root() / "inkwell.db"

    def covers_directory(self) -> Path:
        return self.storage_root() / "data" / "covers"

    def save_storage_root(self, root: Path | str) -> Path:
        """Persist an absolute root for the next application launch."""
        candidate = Path(root).expanduser()

        if not candidate.is_absolute():
            candidate = Path.cwd() / candidate

        candidate = candidate.resolve()
        self._validate_root(candidate)
        self._write_config(candidate)

        # The active process keeps its already-resolved root. A changed root
        # takes effect after restart, when engine.py is imported again.
        return candidate

    def _load_or_initialize(self) -> Path:
        if self.config_path.exists():
            try:
                configuration = json.loads(
                    self.config_path.read_text(encoding="utf-8")
                )
                configured_root = configuration["storage_root"]
            except (OSError, json.JSONDecodeError, KeyError, TypeError) as error:
                raise StorageConfigurationError(
                    f"Cannot read storage configuration at {self.config_path}: {error}"
                ) from error

            if not isinstance(configured_root, str) or not configured_root.strip():
                raise StorageConfigurationError(
                    "Storage configuration must contain a non-empty storage_root."
                )

            root = Path(configured_root).expanduser()

            if not root.is_absolute():
                root = self.config_path.parent / root

            root = root.resolve()
            self._validate_root(root)

            if configured_root != str(root):
                self._write_config(root)

            return root

        working_directory = Path.cwd().resolve()
        legacy_database = working_directory / "inkwell.db"

        if legacy_database.is_file():
            # The old relative database resolves from CWD. Adopt that location
            # only when its database is present, without moving any data.
            self._validate_root(working_directory)
            self._write_config(working_directory)
            return working_directory

        # A fresh installation must not bind itself to an arbitrary launch
        # directory. Persist a stable per-user data root instead.
        stable_root = self._stable_default_root()

        try:
            stable_root.mkdir(
                parents=True,
                exist_ok=True,
            )
        except OSError as error:
            raise StorageConfigurationError(
                f"Cannot create the default storage root {stable_root}: {error}"
            ) from error

        self._validate_root(stable_root)
        self._write_config(stable_root)
        return stable_root

    def _stable_default_root(self) -> Path:
        if self.user_data_directory is None:
            data_directory = QStandardPaths.writableLocation(
                QStandardPaths.StandardLocation.GenericDataLocation
            )

            if not data_directory:
                data_directory = str(Path.home() / ".local" / "share")

            user_data_directory = Path(data_directory)
        else:
            user_data_directory = self.user_data_directory

        return (user_data_directory / "Inkwell").resolve()

    @staticmethod
    def _validate_root(root: Path) -> None:
        if not root.exists() or not root.is_dir():
            raise StorageConfigurationError(
                f"Storage root is not an existing directory: {root}"
            )

        if not os.access(root, os.W_OK | os.X_OK):
            raise StorageConfigurationError(
                f"Storage root is not writable: {root}"
            )

    def _write_config(self, root: Path) -> None:
        try:
            self.config_path.parent.mkdir(
                parents=True,
                exist_ok=True,
            )

            descriptor, temporary_name = tempfile.mkstemp(
                prefix=f".{self.config_path.name}.",
                suffix=".tmp",
                dir=self.config_path.parent,
                text=True,
            )

            try:
                with os.fdopen(
                    descriptor,
                    "w",
                    encoding="utf-8",
                ) as config_file:
                    json.dump(
                        {"storage_root": str(root)},
                        config_file,
                        indent=2,
                    )
                    config_file.write("\n")
                    config_file.flush()
                    os.fsync(config_file.fileno())

                os.replace(
                    temporary_name,
                    self.config_path,
                )
            finally:
                if os.path.exists(temporary_name):
                    os.unlink(temporary_name)
        except OSError as error:
            raise StorageConfigurationError(
                f"Cannot write storage configuration at {self.config_path}: {error}"
            ) from error


storage_config = StorageConfig()
