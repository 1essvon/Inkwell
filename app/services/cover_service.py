from hashlib import sha256
from pathlib import Path
from urllib.parse import urlparse

import requests


COVER_DIR = Path("data/covers")


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
            return str(path)

        try:
            response = requests.get(
                url,
                timeout=cls.TIMEOUT,
            )

            response.raise_for_status()

        except requests.RequestException:
            return None

        if not response.content:
            return None

        try:
            path.write_bytes(response.content)
        except OSError:
            return None

        return str(path)

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