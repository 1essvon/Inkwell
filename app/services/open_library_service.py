from dataclasses import dataclass
import logging

import requests
from requests import RequestException


logger = logging.getLogger(__name__)


SEARCH_API_URL = "https://openlibrary.org/search.json"
WORK_API_URL = "https://openlibrary.org"


@dataclass(slots=True)
class OpenLibraryBook:
    title: str
    authors: list[str]
    isbn: str | None
    publisher: str | None
    published_year: int | None
    description: str | None
    page_count: int | None
    genre: str | None
    thumbnail: str | None
    key: str | None = None


class OpenLibraryService:

    TIMEOUT = 10

    @classmethod
    def search(
        cls,
        query: str,
        limit: int = 10,
    ) -> list[OpenLibraryBook]:

        query = query.strip()

        if not query:
            return []

        try:
            response = requests.get(
                SEARCH_API_URL,
                params={
                    "q": query,
                    "limit": limit,
                    "fields": (
                        "key,title,author_name,isbn,publisher,"
                        "first_publish_year,publish_year,"
                        "number_of_pages_median,subject,cover_i"
                    ),
                },
                timeout=cls.TIMEOUT,
            )

            response.raise_for_status()

        except RequestException as error:
            logger.warning("Open Library request failed (%s)", type(error).__name__)
            return []

        try:
            payload = response.json()
        except ValueError as error:
            logger.warning(
                "Open Library search response was not valid JSON (%s)",
                type(error).__name__,
            )
            return []

        docs = payload.get("docs")

        if not docs:
            return []

        books = []

        for doc in docs:
            try:
                books.append(cls._parse(doc))
            except Exception as error:
                logger.warning("Could not parse an Open Library result (%s)", type(error).__name__)

        return books

    @classmethod
    def _parse(cls, doc) -> OpenLibraryBook:

        authors = doc.get("author_name", [])

        isbn_list = doc.get("isbn", [])
        isbn = isbn_list[0] if isbn_list else None

        published_year = doc.get("first_publish_year")

        if not published_year:
            years = doc.get("publish_year", [])
            published_year = max(years) if years else None

        publishers = doc.get("publisher", [])
        publisher = publishers[0] if publishers else None

        subjects = doc.get("subject", [])
        genre = subjects[0] if subjects else None

        cover_id = doc.get("cover_i")

        thumbnail = (
            f"https://covers.openlibrary.org/b/id/{cover_id}-M.jpg"
            if cover_id
            else None
        )

        key = doc.get("key")

        description = cls._get_description(key)

        return OpenLibraryBook(
            title=doc.get("title", ""),
            authors=authors,
            isbn=isbn,
            publisher=publisher,
            published_year=published_year,
            description=description,
            page_count=doc.get("number_of_pages_median"),
            genre=genre,
            thumbnail=thumbnail,
            key=key,
        )

    @classmethod
    def _get_description(
        cls,
        key: str | None,
    ) -> str | None:

        if not key:
            return None

        if not key.startswith("/works/"):
            return None

        url = f"{WORK_API_URL}{key}.json"

        try:
            response = requests.get(
                url,
                timeout=cls.TIMEOUT,
            )

            response.raise_for_status()

        except RequestException as error:
            logger.warning("Open Library description request failed (%s)", type(error).__name__)
            return None

        try:
            payload = response.json()
        except ValueError as error:
            logger.warning(
                "Open Library description response was not valid JSON (%s)",
                type(error).__name__,
            )
            return None

        description = payload.get("description")

        if isinstance(description, dict):
            description = description.get("value")

        if not isinstance(description, str):
            return None

        description = description.strip()

        return description or None
