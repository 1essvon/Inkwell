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

import requests


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

        response = requests.get(

            API_URL,

            params={
                "q": query,
                "maxResults": limit,
            },

            timeout=cls.TIMEOUT,

        )

        response.raise_for_status()

        payload = response.json()

        items = payload.get(
            "items",
            [],
        )

        return [

            cls._parse(item)

            for item in items

        ]

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