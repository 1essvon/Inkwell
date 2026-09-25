import sqlite3
from pathlib import Path


SCHEMA = """
CREATE TABLE books (
    id INTEGER PRIMARY KEY, title TEXT NOT NULL, author TEXT NOT NULL,
    isbn TEXT, publisher TEXT, published_year INTEGER, genre TEXT,
    description TEXT, page_count INTEGER, cover_path TEXT, current_page INTEGER NOT NULL,
    status TEXT NOT NULL, rating INTEGER, date_added TEXT NOT NULL, updated_at TEXT NOT NULL
);
CREATE TABLE notes (
    id INTEGER PRIMARY KEY, book_id INTEGER NOT NULL REFERENCES books(id), page INTEGER NOT NULL,
    title TEXT NOT NULL, content TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL
);
CREATE TABLE quotes (
    id INTEGER PRIMARY KEY, book_id INTEGER NOT NULL REFERENCES books(id), content TEXT NOT NULL,
    page INTEGER NOT NULL, note TEXT NOT NULL, tags TEXT NOT NULL,
    created_at TEXT NOT NULL, updated_at TEXT NOT NULL
);
CREATE TABLE reading_sessions (
    id INTEGER PRIMARY KEY, book_id INTEGER NOT NULL REFERENCES books(id),
    start_page INTEGER NOT NULL, end_page INTEGER NOT NULL, duration_minutes INTEGER NOT NULL,
    started_at TEXT NOT NULL, ended_at TEXT NOT NULL
);
CREATE TABLE scratchpad_entries (
    id INTEGER PRIMARY KEY, title TEXT NOT NULL, content TEXT NOT NULL,
    created_at TEXT NOT NULL, updated_at TEXT NOT NULL
);
CREATE TABLE app_settings (
    id INTEGER PRIMARY KEY, theme TEXT NOT NULL, autosave_scratchpad INTEGER NOT NULL,
    confirm_before_clear INTEGER NOT NULL, updated_at TEXT NOT NULL,
    reading_goal_books INTEGER NOT NULL, reading_goal_pages INTEGER NOT NULL
);
"""


def create_fixture_database(path: Path, cover_path="data/covers/cover-1.jpg", title="Fixture Book"):
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        path.unlink()
    connection = sqlite3.connect(path)
    try:
        connection.executescript(SCHEMA)
        connection.execute(
            """INSERT INTO books (
                title, author, isbn, publisher, published_year, genre, description,
                page_count, cover_path, current_page, status, rating, date_added, updated_at
            ) VALUES (?, ?, NULL, NULL, NULL, NULL, NULL, ?, ?, ?, ?, NULL, ?, ?)""",
            (title, "Test Author", 120, cover_path, 14, "Reading", "2026-01-01", "2026-01-01"),
        )
        connection.commit()
    finally:
        connection.close()


def create_fixture_storage(root: Path, title="Fixture Book", cover_path="data/covers/cover-1.jpg"):
    covers = root / "data" / "covers"
    covers.mkdir(parents=True, exist_ok=True)
    (covers / "cover-1.jpg").write_bytes(b"cover-fixture")
    create_fixture_database(root / "inkwell.db", cover_path=cover_path, title=title)
    return root / "inkwell.db"
