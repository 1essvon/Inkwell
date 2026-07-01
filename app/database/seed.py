"""
File:
    seed.py

Purpose:
    Populate development database with sample data.

Responsibilities:
    - Seed books
    - Seed notes
    - Seed quotes

Notes:
    Runs only when database is empty.
"""

from app.database.session import (
    SessionLocal
)

from app.models.book import Book

from app.constants.book_status import (
    BookStatus
)

def seed_database():

    session = SessionLocal()

    try:

        if session.query(Book).count() > 0:

            return

        seed_books(
            session
        )

        seed_notes(
            session
        )

        seed_quotes(
            session
        )

        session.commit()

    finally:

        session.close()

def seed_books(
    session
):

    books = [
        {
            "title": "Almond",
            "author": "Sohn Won-pyung",
            "publisher": "HarperVia",
            "genre": "Fiction",
            "page_count": 213,
            "current_page": 14,
            "status": BookStatus.READING
        },

        {
            "title": "Animal Farm",
            "author": "George Orwell",
            "publisher": "Penguin",
            "genre": "Classic",
            "page_count": 120,
            "current_page": 35,
            "status": BookStatus.READING
        },

        {
            "title": "The Psychology of Money",
            "author": "Morgan Housel",
            "publisher": "Harriman House",
            "genre": "Finance",
            "page_count": 256,
            "current_page": 89,
            "status": BookStatus.READING
        },

        {
            "title": "The Pragmatic Programmer",
            "author": "Andrew Hunt",
            "publisher": "Addison-Wesley",
            "genre": "Programming",
            "page_count": 352,
            "current_page": 120,
            "status": BookStatus.READING
        },

        {
            "title": "Atomic Habits",
            "author": "James Clear",
            "publisher": "Avery",
            "genre": "Self Help",
            "page_count": 320,
            "current_page": 320,
            "status": BookStatus.COMPLETED
        },

        {
            "title": "Deep Work",
            "author": "Cal Newport",
            "publisher": "Grand Central",
            "genre": "Productivity",
            "page_count": 304,
            "current_page": 304,
            "status": BookStatus.COMPLETED
        },

        {
            "title": "Naoko",
            "author": "Keigo Higashino",
            "publisher": "Gramedia",
            "genre": "Fiction",
            "page_count": 456,
            "current_page": 456,
            "status": BookStatus.COMPLETED
        },

        {
            "title": "Bumi",
            "author": "Tere Liye",
            "publisher": "Gramedia Pustaka Utama",
            "genre": "Fantasy",
            "page_count": 300,
            "current_page": 300,
            "status": BookStatus.COMPLETED
        },

        {
            "title": "Educated",
            "author": "Tara Westover",
            "publisher": "Random House",
            "genre": "Memoir",
            "page_count": 352,
            "current_page": 352,
            "status": BookStatus.COMPLETED
        },

        {
            "title": "The Little Prince",
            "author": "Antoine de Saint-Exupéry",
            "publisher": "Reynal & Hitchcock",
            "genre": "Fiction",
            "page_count": 96,
            "current_page": 96,
            "status": BookStatus.COMPLETED
        },

        {
            "title": "Sapiens",
            "author": "Yuval Noah Harari",
            "publisher": "Harper",
            "genre": "History",
            "page_count": 498,
            "status": BookStatus.WANT_TO_READ
        },

        {
            "title": "Homo Deus",
            "author": "Yuval Noah Harari",
            "publisher": "Harper",
            "genre": "History",
            "page_count": 450,
            "status": BookStatus.WANT_TO_READ
        },

        {
            "title": "Thinking, Fast and Slow",
            "author": "Daniel Kahneman",
            "publisher": "Farrar, Straus and Giroux",
            "genre": "Psychology",
            "page_count": 512,
            "status": BookStatus.WANT_TO_READ
        },

        {
            "title": "Clean Architecture",
            "author": "Robert C. Martin",
            "publisher": "Prentice Hall",
            "genre": "Programming",
            "page_count": 432,
            "status": BookStatus.WANT_TO_READ
        },

        {
            "title": "Project Hail Mary",
            "author": "Andy Weir",
            "publisher": "Ballantine Books",
            "genre": "Sci-Fi",
            "page_count": 496,
            "status": BookStatus.WANT_TO_READ
        },

        {
            "title": "The Lord of the Rings",
            "author": "J.R.R. Tolkien",
            "publisher": "Allen & Unwin",
            "genre": "Fantasy",
            "page_count": 1178,
            "current_page": 150,
            "status": BookStatus.PAUSED
        },

        {
            "title": "Crime and Punishment",
            "author": "Fyodor Dostoevsky",
            "publisher": "The Russian Messenger",
            "genre": "Classic",
            "page_count": 671,
            "current_page": 210,
            "status": BookStatus.PAUSED
        },

        {
            "title": "Infinite Jest",
            "author": "David Foster Wallace",
            "publisher": "Little, Brown",
            "genre": "Fiction",
            "page_count": 1079,
            "current_page": 70,
            "status": BookStatus.DROPPED
        },

        {
            "title": "Ulysses",
            "author": "James Joyce",
            "publisher": "Shakespeare and Company",
            "genre": "Classic",
            "page_count": 730,
            "current_page": 55,
            "status": BookStatus.DROPPED
        }
    ]

    session.add_all(
        Book(**book)
        for book in books
    )

def seed_notes(
        session
    ):
    pass

def seed_quotes(
    session
    ):
    pass