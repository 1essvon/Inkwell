"""Application logging configuration."""

import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
import sys

from PySide6.QtCore import QStandardPaths


MAX_LOG_BYTES = 1_000_000
LOG_BACKUP_COUNT = 3
_HANDLER_MARKER = "_inkwell_application_handler"


def default_log_directory() -> Path:
    """Return a stable user data location, independent of storage root/CWD."""
    data_directory = QStandardPaths.writableLocation(
        QStandardPaths.StandardLocation.GenericDataLocation
    )
    if not data_directory:
        data_directory = str(Path.home() / ".local" / "share")

    return Path(data_directory) / "TheInkwell" / "logs"


def configure_logging(log_directory: Path | str | None = None) -> logging.Logger:
    """Configure bounded file logging, falling back to stderr on I/O errors."""
    application_logger = logging.getLogger("app")
    application_logger.setLevel(logging.INFO)
    application_logger.propagate = False

    if any(
        getattr(handler, _HANDLER_MARKER, False)
        for handler in application_logger.handlers
    ):
        return application_logger

    formatter = logging.Formatter(
        "%(asctime)s %(levelname)s %(name)s: %(message)s"
    )
    try:
        directory = (
            Path(log_directory)
            if log_directory is not None
            else default_log_directory()
        )
        directory.mkdir(parents=True, exist_ok=True)
        handler = RotatingFileHandler(
            directory / "inkwell.log",
            maxBytes=MAX_LOG_BYTES,
            backupCount=LOG_BACKUP_COUNT,
            encoding="utf-8",
        )
    except (OSError, ValueError) as error:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(formatter)
        setattr(handler, _HANDLER_MARKER, True)
        application_logger.addHandler(handler)
        application_logger.warning(
            "File logging unavailable (%s); using stderr",
            type(error).__name__,
        )
        return application_logger

    handler.setFormatter(formatter)
    setattr(handler, _HANDLER_MARKER, True)
    application_logger.addHandler(handler)
    return application_logger
