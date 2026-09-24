from hashlib import sha256
import logging
from pathlib import Path
from urllib.parse import urlparse

import requests

from app.storage_config import storage_config


logger = logging.getLogger(__name__)


COVER_DIR = storage_config.covers_directory()
_COVER_RELATIVE_DIR = Path("data") / "covers"


class CoverService:

    TIMEOUT = 10

    @classmethod
    def download(
        cls,
        url: str,
    ) -> str | None:

        if not url:
            return None

        COVER_DIR.mkdir(
            parents=True,
            exist_ok=True,
        )

        extension = cls._get_extension(url)
        filename = cls._get_filename(url, extension)
        path = COVER_DIR / filename

        # Return cached cover if it already exists.
        if path.exists():
            return str(_COVER_RELATIVE_DIR / filename)

        try:
            response = requests.get(
                url,
                timeout=cls.TIMEOUT,
            )

            response.raise_for_status()

        except requests.RequestException as error:
            logger.warning("Cover download failed (%s)", type(error).__name__)
            return None

        if not response.content:
            return None

        try:
            path.write_bytes(response.content)
        except OSError as error:
            logger.warning("Could not save downloaded cover (%s)", type(error).__name__)
            return None

        return str(_COVER_RELATIVE_DIR / filename)

    @staticmethod
    def _get_filename(
        url: str,
        extension: str,
    ) -> str:

        cache_key = sha256(
            url.encode("utf-8")
        ).hexdigest()

        return f"{cache_key}{extension}"

    @staticmethod
    def _get_extension(url: str) -> str:

        path = urlparse(url).path
        suffix = Path(path).suffix.lower()

        allowed_extensions = {
            ".jpg",
            ".jpeg",
            ".png",
            ".webp",
        }

        if suffix in allowed_extensions:
            return suffix

        return ".jpg"
