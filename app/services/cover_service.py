"""
Service:
    Cover Service

Responsibilities:
    - Download cover image
    - Save locally
    - Return local path

Does NOT:
    - Access database
    - Know about Book
    - Know about Qt
"""

from pathlib import Path
from uuid import uuid4

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

        try:

            response = requests.get(
                url,
                timeout=cls.TIMEOUT,
            )

            response.raise_for_status()

        except requests.RequestException:

            return None

        extension = ".jpg"

        if "." in url:

            last = url.rsplit(".", 1)[-1]

            if len(last) <= 5:

                extension = "." + last.split("?")[0]

        filename = f"{uuid4().hex}{extension}"

        path = COVER_DIR / filename

        path.write_bytes(
            response.content
        )

        return str(path)