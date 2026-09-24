"""
Service:
    Google Books API

Responsibilities:
    - Search books
    - Parse response
    - Return clean Python data

Does NOT:
    - Access database
    - Know about Qt
    - Create Book model
"""

from dataclasses import dataclass
import logging

import requests

from requests import RequestException


logger = logging.getLogger(__name__)


API_URL = "https://www.googleapis.com/books/v1/volumes"


@dataclass(slots=True)
class GoogleBook:

    title: str

    authors: list[str]

    isbn: str | None

    publisher: str | None

    published_year: int | None

    description: str | None

    page_count: int | None

    genre: str | None

    thumbnail: str | None


class GoogleBooksService:

    TIMEOUT = 10

    @classmethod
    def search(
        cls,
        query: str,
        limit: int = 10,
    ) -> list[GoogleBook]:

        query = query.strip()

        if not query:
            return []

        try:

            response = requests.get(

                API_URL,

                params={
                    "q": query,
                    "maxResults": limit,
                },

                timeout=cls.TIMEOUT,

            )

            response.raise_for_status()

        except RequestException as error:
            logger.warning("Google Books request failed (%s)", type(error).__name__)

            return []

        try:

            payload = response.json()

        except ValueError as error:
            logger.warning(
                "Google Books response was not valid JSON (%s)",
                type(error).__name__,
            )

            return []

        items = payload.get("items")

        if not items:

            return []

        books = []

        for item in items:

            try:

                books.append(
                    cls._parse(item)
                )

            except Exception as error:
                logger.warning(
                    "Could not parse a Google Books result (%s)",
                    type(error).__name__,
                )

        return books

    @staticmethod
    def _parse(
        item,
    ) -> GoogleBook:

        info = item.get(
            "volumeInfo",
            {},
        )

        isbn = None

        for identifier in info.get(
            "industryIdentifiers",
            [],
        ):

            if identifier["type"] in (
                "ISBN_13",
                "ISBN_10",
            ):

                isbn = identifier["identifier"]

                break

        year = None

        published = info.get(
            "publishedDate"
        )

        if published:

            try:

                year = int(
                    published[:4]
                )

            except ValueError:

                pass

        return GoogleBook(

            title=info.get(
                "title",
                "",
            ),

            authors=info.get(
                "authors",
                [],
            ),

            isbn=isbn,

            publisher=info.get(
                "publisher",
            ),

            published_year=year,

            description=info.get(
                "description",
            ),

            page_count=info.get(
                "pageCount",
            ),

            genre=", ".join(
                info.get(
                    "categories",
                    [],
                )
            )
            or None,

            thumbnail=(
                info.get(
                    "imageLinks",
                    {},
                ).get(
                    "thumbnail"
                )
            ),

        )
