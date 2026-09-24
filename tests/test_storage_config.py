import json
import os
from pathlib import Path
import tempfile
import unittest

from app.storage_config import (
    StorageConfig,
    StorageConfigurationError,
)


class StorageConfigTests(unittest.TestCase):

    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        self.base_path = Path(self.temporary_directory.name)

    def make_config(self, name="storage.json"):
        return StorageConfig(
            config_path=self.base_path / "config" / name,
            user_data_directory=self.base_path / "user-data",
        )

    def test_uses_valid_configured_root_and_resolves_paths(self):
        root = self.base_path / "configured-root"
        root.mkdir()
        config = self.make_config()
        config.config_path.parent.mkdir(parents=True)
        config.config_path.write_text(
            json.dumps({"storage_root": str(root)}),
            encoding="utf-8",
        )

        self.assertEqual(config.storage_root(), root.resolve())
        self.assertEqual(config.database_path(), root / "inkwell.db")
        self.assertEqual(
            config.covers_directory(),
            root / "data" / "covers",
        )

    def test_invalid_configured_root_raises_without_fallback(self):
        launch_directory = self.base_path / "launch"
        launch_directory.mkdir()
        (launch_directory / "inkwell.db").write_bytes(b"legacy marker")
        original_directory = Path.cwd()
        self.addCleanup(os.chdir, original_directory)
        os.chdir(launch_directory)

        config = self.make_config()
        config.config_path.parent.mkdir(parents=True)
        config.config_path.write_text(
            json.dumps(
                {"storage_root": str(self.base_path / "missing-root")}
            ),
            encoding="utf-8",
        )

        with self.assertRaises(StorageConfigurationError):
            config.storage_root()

        self.assertEqual(
            json.loads(config.config_path.read_text(encoding="utf-8")),
            {"storage_root": str(self.base_path / "missing-root")},
        )

    def test_adopts_legacy_root_only_when_database_exists(self):
        legacy_root = self.base_path / "legacy"
        legacy_root.mkdir()
        (legacy_root / "inkwell.db").write_bytes(b"legacy marker")
        original_directory = Path.cwd()
        self.addCleanup(os.chdir, original_directory)
        os.chdir(legacy_root)

        config = self.make_config()

        self.assertEqual(config.storage_root(), legacy_root.resolve())
        saved = json.loads(config.config_path.read_text(encoding="utf-8"))
        self.assertEqual(saved["storage_root"], str(legacy_root.resolve()))

    def test_uses_stable_user_data_root_without_legacy_database(self):
        launch_directory = self.base_path / "launch"
        launch_directory.mkdir()
        original_directory = Path.cwd()
        self.addCleanup(os.chdir, original_directory)
        os.chdir(launch_directory)

        config = self.make_config()
        root = config.storage_root()

        self.assertEqual(
            root,
            (self.base_path / "user-data" / "Inkwell").resolve(),
        )
        self.assertNotEqual(root, launch_directory.resolve())
        self.assertFalse((launch_directory / "inkwell.db").exists())
        saved = json.loads(config.config_path.read_text(encoding="utf-8"))
        self.assertEqual(saved["storage_root"], str(root))

    def test_configured_root_is_independent_of_current_directory(self):
        configured_root = self.base_path / "configured-root"
        configured_root.mkdir()
        config = self.make_config()
        config.config_path.parent.mkdir(parents=True)
        config.config_path.write_text(
            json.dumps({"storage_root": str(configured_root)}),
            encoding="utf-8",
        )

        first_root = config.storage_root()
        other_directory = self.base_path / "other-launch"
        other_directory.mkdir()
        original_directory = Path.cwd()
        self.addCleanup(os.chdir, original_directory)
        os.chdir(other_directory)

        reloaded_config = self.make_config()
        self.assertEqual(reloaded_config.storage_root(), first_root)

    def test_saving_root_persists_absolute_path_without_runtime_switch(self):
        active_root = self.base_path / "active"
        active_root.mkdir()
        new_root = self.base_path / "new-root"
        new_root.mkdir()
        config = self.make_config()
        config.save_storage_root(active_root)
        self.assertEqual(config.storage_root(), active_root.resolve())

        saved_root = config.save_storage_root(new_root)

        self.assertEqual(saved_root, new_root.resolve())
        self.assertEqual(config.storage_root(), active_root.resolve())
        saved = json.loads(config.config_path.read_text(encoding="utf-8"))
        self.assertEqual(saved["storage_root"], str(new_root.resolve()))


if __name__ == "__main__":
    unittest.main()
