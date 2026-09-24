import io
import logging
from pathlib import Path
import tempfile
import unittest
from unittest import mock

from app import logging_config


class LoggingConfigurationTests(unittest.TestCase):
    def setUp(self):
        self.logger = logging.getLogger("app")
        self.original_handlers = list(self.logger.handlers)
        self.original_level = self.logger.level
        self.original_propagate = self.logger.propagate
        self.addCleanup(self._restore_logger)

    def _restore_logger(self):
        for handler in list(self.logger.handlers):
            if handler not in self.original_handlers:
                self.logger.removeHandler(handler)
                handler.close()
        self.logger.handlers[:] = self.original_handlers
        self.logger.setLevel(self.original_level)
        self.logger.propagate = self.original_propagate

    def test_configures_rotating_file_handler_in_requested_directory(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            log_directory = Path(temporary_directory) / "logs"

            configured_logger = logging_config.configure_logging(log_directory)
            configured_logger.error("isolated test event")
            configured_logger.handlers[0].flush()

            log_file = log_directory / "inkwell.log"
            self.assertTrue(log_file.is_file())
            self.assertIn("isolated test event", log_file.read_text(encoding="utf-8"))
            self.assertIsInstance(
                configured_logger.handlers[0],
                logging_config.RotatingFileHandler,
            )
            self.assertEqual(
                configured_logger.handlers[0].maxBytes,
                logging_config.MAX_LOG_BYTES,
            )
            self.assertEqual(
                configured_logger.handlers[0].backupCount,
                logging_config.LOG_BACKUP_COUNT,
            )

    def test_falls_back_to_stderr_when_file_handler_cannot_be_created(self):
        stderr = io.StringIO()
        with tempfile.TemporaryDirectory() as temporary_directory, \
                mock.patch.object(logging_config, "RotatingFileHandler", side_effect=OSError("denied")), \
                mock.patch.object(logging_config.sys, "stderr", stderr):
            configured_logger = logging_config.configure_logging(temporary_directory)
            configured_logger.error("fallback event")

            self.assertIsInstance(configured_logger.handlers[0], logging.StreamHandler)
            self.assertIn("File logging unavailable", stderr.getvalue())
            self.assertIn("fallback event", stderr.getvalue())
            self.assertEqual(list(Path(temporary_directory).iterdir()), [])

    def test_repeated_configuration_does_not_add_duplicate_handlers(self):
        with tempfile.TemporaryDirectory() as temporary_directory:
            configured_logger = logging_config.configure_logging(temporary_directory)
            first_handler = configured_logger.handlers[0]

            logging_config.configure_logging(temporary_directory)

            self.assertEqual(configured_logger.handlers.count(first_handler), 1)
            self.assertEqual(len(configured_logger.handlers), len(self.original_handlers) + 1)

    def test_default_directory_uses_stable_user_data_location(self):
        with mock.patch.object(
            logging_config.QStandardPaths,
            "writableLocation",
            return_value="/user-data",
        ):
            self.assertEqual(
                logging_config.default_log_directory(),
                Path("/user-data") / "TheInkwell" / "logs",
            )


if __name__ == "__main__":
    unittest.main()
