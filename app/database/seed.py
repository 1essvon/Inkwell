"""
File:
    seed.py

Purpose:
    Populate development database
    with realistic demo data.

Responsibilities:
    - Seed books
    - Seed reading sessions
    - Seed notes
    - Seed quotes

Notes:
    Runs only when database is empty.
"""

# ==================================================
# IMPORTS
# ==================================================

from datetime import (
    datetime,
    timedelta,
)

from app.database.session import (
    SessionLocal,
)

from app.models.book import Book
from app.models.note import Note
from app.models.quote import Quote
from app.models.reading_session import ReadingSession

from app.constants.book_status import (
    BookStatus,
)

# ==================================================
# BOOKS
# ==================================================

BOOKS = [

    dict(
        title="Almond",
        author="Sohn Won-pyung",
        publisher="HarperVia",
        genre="Fiction",
        page_count=213,
        current_page=14,
        status=BookStatus.READING,
    ),

    dict(
        title="Animal Farm",
        author="George Orwell",
        publisher="Penguin",
        genre="Classic",
        page_count=120,
        current_page=35,
        status=BookStatus.READING,
    ),

    dict(
        title="The Psychology of Money",
        author="Morgan Housel",
        publisher="Harriman House",
        genre="Finance",
        page_count=256,
        current_page=89,
        status=BookStatus.READING,
    ),

    dict(
        title="The Pragmatic Programmer",
        author="Andrew Hunt",
        publisher="Addison-Wesley",
        genre="Programming",
        page_count=352,
        current_page=120,
        status=BookStatus.READING,
    ),

    dict(
        title="Atomic Habits",
        author="James Clear",
        publisher="Avery",
        genre="Self Help",
        page_count=320,
        current_page=320,
        status=BookStatus.COMPLETED,
    ),

    dict(
        title="Deep Work",
        author="Cal Newport",
        publisher="Grand Central",
        genre="Productivity",
        page_count=304,
        current_page=304,
        status=BookStatus.COMPLETED,
    ),

    dict(
        title="Naoko",
        author="Keigo Higashino",
        publisher="Gramedia",
        genre="Fiction",
        page_count=456,
        current_page=456,
        status=BookStatus.COMPLETED,
    ),

    dict(
        title="Bumi",
        author="Tere Liye",
        publisher="Gramedia Pustaka Utama",
        genre="Fantasy",
        page_count=300,
        current_page=300,
        status=BookStatus.COMPLETED,
    ),

    dict(
        title="Educated",
        author="Tara Westover",
        publisher="Random House",
        genre="Memoir",
        page_count=352,
        current_page=352,
        status=BookStatus.COMPLETED,
    ),

    dict(
        title="The Little Prince",
        author="Antoine de Saint-Exupéry",
        publisher="Reynal & Hitchcock",
        genre="Fiction",
        page_count=96,
        current_page=96,
        status=BookStatus.COMPLETED,
    ),

    dict(
        title="Sapiens",
        author="Yuval Noah Harari",
        publisher="Harper",
        genre="History",
        page_count=498,
        current_page=0,
        status=BookStatus.WANT_TO_READ,
    ),

    dict(
        title="Homo Deus",
        author="Yuval Noah Harari",
        publisher="Harper",
        genre="History",
        page_count=450,
        current_page=0,
        status=BookStatus.WANT_TO_READ,
    ),

    dict(
        title="Thinking, Fast and Slow",
        author="Daniel Kahneman",
        publisher="Farrar, Straus and Giroux",
        genre="Psychology",
        page_count=512,
        current_page=0,
        status=BookStatus.WANT_TO_READ,
    ),

    dict(
        title="Clean Architecture",
        author="Robert C. Martin",
        publisher="Prentice Hall",
        genre="Programming",
        page_count=432,
        current_page=0,
        status=BookStatus.WANT_TO_READ,
    ),

    dict(
        title="Project Hail Mary",
        author="Andy Weir",
        publisher="Ballantine Books",
        genre="Sci-Fi",
        page_count=496,
        current_page=0,
        status=BookStatus.WANT_TO_READ,
    ),

    dict(
        title="The Lord of the Rings",
        author="J.R.R. Tolkien",
        publisher="Allen & Unwin",
        genre="Fantasy",
        page_count=1178,
        current_page=150,
        status=BookStatus.PAUSED,
    ),

    dict(
        title="Crime and Punishment",
        author="Fyodor Dostoevsky",
        publisher="The Russian Messenger",
        genre="Classic",
        page_count=671,
        current_page=210,
        status=BookStatus.PAUSED,
    ),

    dict(
        title="Infinite Jest",
        author="David Foster Wallace",
        publisher="Little, Brown",
        genre="Fiction",
        page_count=1079,
        current_page=70,
        status=BookStatus.DROPPED,
    ),

    dict(
        title="Ulysses",
        author="James Joyce",
        publisher="Shakespeare and Company",
        genre="Classic",
        page_count=730,
        current_page=55,
        status=BookStatus.DROPPED,
    ),

]

# ==================================================
# READING SESSIONS
# ==================================================

SESSIONS = [

    # ----------------------------------------------
    # Atomic Habits (Completed)
    # ----------------------------------------------

    dict(book="Atomic Habits", start=0, end=18, minutes=24, days_ago=48),
    dict(book="Atomic Habits", start=18, end=37, minutes=28, days_ago=47),
    dict(book="Atomic Habits", start=37, end=58, minutes=31, days_ago=45),
    dict(book="Atomic Habits", start=58, end=82, minutes=35, days_ago=44),
    dict(book="Atomic Habits", start=82, end=101, minutes=29, days_ago=42),
    dict(book="Atomic Habits", start=101, end=126, minutes=37, days_ago=40),
    dict(book="Atomic Habits", start=126, end=148, minutes=30, days_ago=38),
    dict(book="Atomic Habits", start=148, end=171, minutes=33, days_ago=36),
    dict(book="Atomic Habits", start=171, end=194, minutes=31, days_ago=34),
    dict(book="Atomic Habits", start=194, end=216, minutes=34, days_ago=32),
    dict(book="Atomic Habits", start=216, end=239, minutes=32, days_ago=30),
    dict(book="Atomic Habits", start=239, end=262, minutes=30, days_ago=28),
    dict(book="Atomic Habits", start=262, end=283, minutes=28, days_ago=26),
    dict(book="Atomic Habits", start=283, end=303, minutes=27, days_ago=24),
    dict(book="Atomic Habits", start=303, end=320, minutes=26, days_ago=22),

    # ----------------------------------------------
    # Deep Work (Completed)
    # ----------------------------------------------

    dict(book="Deep Work", start=0, end=20, minutes=26, days_ago=20),
    dict(book="Deep Work", start=20, end=44, minutes=30, days_ago=19),
    dict(book="Deep Work", start=44, end=70, minutes=33, days_ago=18),
    dict(book="Deep Work", start=70, end=96, minutes=36, days_ago=17),
    dict(book="Deep Work", start=96, end=126, minutes=38, days_ago=16),
    dict(book="Deep Work", start=126, end=161, minutes=42, days_ago=15),
    dict(book="Deep Work", start=161, end=203, minutes=46, days_ago=14),
    dict(book="Deep Work", start=203, end=250, minutes=48, days_ago=13),
    dict(book="Deep Work", start=250, end=280, minutes=36, days_ago=12),
    dict(book="Deep Work", start=280, end=304, minutes=30, days_ago=11),

    # ----------------------------------------------
    # The Pragmatic Programmer (Reading)
    # ----------------------------------------------

    dict(book="The Pragmatic Programmer", start=0, end=22, minutes=28, days_ago=10),
    dict(book="The Pragmatic Programmer", start=22, end=45, minutes=31, days_ago=9),
    dict(book="The Pragmatic Programmer", start=45, end=68, minutes=34, days_ago=8),
    dict(book="The Pragmatic Programmer", start=68, end=89, minutes=30, days_ago=7),
    dict(book="The Pragmatic Programmer", start=89, end=105, minutes=24, days_ago=5),
    dict(book="The Pragmatic Programmer", start=105, end=120, minutes=23, days_ago=2),

    # ----------------------------------------------
    # The Psychology of Money (Reading)
    # ----------------------------------------------

    dict(book="The Psychology of Money", start=0, end=20, minutes=25, days_ago=18),
    dict(book="The Psychology of Money", start=20, end=39, minutes=26, days_ago=17),
    dict(book="The Psychology of Money", start=39, end=58, minutes=28, days_ago=15),
    dict(book="The Psychology of Money", start=58, end=73, minutes=24, days_ago=13),
    dict(book="The Psychology of Money", start=73, end=89, minutes=23, days_ago=6),

    # ----------------------------------------------
    # Animal Farm (Reading)
    # ----------------------------------------------

    dict(book="Animal Farm", start=0, end=10, minutes=14, days_ago=12),
    dict(book="Animal Farm", start=10, end=18, minutes=15, days_ago=9),
    dict(book="Animal Farm", start=18, end=27, minutes=18, days_ago=4),
    dict(book="Animal Farm", start=27, end=35, minutes=16, days_ago=1),

    # ----------------------------------------------
    # Almond (Reading)
    # ----------------------------------------------

    dict(book="Almond", start=0, end=14, minutes=21, days_ago=3),

]

# ==================================================
# NOTES
# ==================================================

NOTES = [

    # ----------------------------------------------
    # Atomic Habits
    # ----------------------------------------------

    dict(
        book="Atomic Habits",
        title="Identity Before Outcome",
        content=(
            "Real change starts from identity. "
            "Instead of chasing goals, become the type of "
            "person who naturally performs the habit."
        ),
    ),

    dict(
        book="Atomic Habits",
        title="Environment Beats Motivation",
        content=(
            "Design the environment first. "
            "Good habits become easier when the cue "
            "is obvious."
        ),
    ),

    dict(
        book="Atomic Habits",
        title="Small Improvements",
        content=(
            "Improving one percent every day compounds "
            "into remarkable long-term results."
        ),
    ),

    dict(
        book="Atomic Habits",
        title="Habit Tracking",
        content=(
            "A visible habit tracker gives immediate "
            "feedback and encourages consistency."
        ),
    ),

    dict(
        book="Atomic Habits",
        title="Never Miss Twice",
        content=(
            "Missing one day is normal. "
            "Missing twice starts a new habit."
        ),
    ),

    # ----------------------------------------------
    # Deep Work
    # ----------------------------------------------

    dict(
        book="Deep Work",
        title="Focus Is Valuable",
        content=(
            "The ability to focus without distraction "
            "is becoming increasingly rare and valuable."
        ),
    ),

    dict(
        book="Deep Work",
        title="Eliminate Distractions",
        content=(
            "Notifications interrupt concentration far "
            "more than expected."
        ),
    ),

    dict(
        book="Deep Work",
        title="Schedule Deep Work",
        content=(
            "Treat deep work like a meeting on the calendar."
        ),
    ),

    dict(
        book="Deep Work",
        title="Shutdown Ritual",
        content=(
            "Ending the workday intentionally reduces "
            "mental fatigue."
        ),
    ),

    # ----------------------------------------------
    # The Pragmatic Programmer
    # ----------------------------------------------

    dict(
        book="The Pragmatic Programmer",
        title="Broken Windows",
        content=(
            "Fix small issues early before they become "
            "accepted as normal."
        ),
    ),

    dict(
        book="The Pragmatic Programmer",
        title="DRY Principle",
        content=(
            "Every piece of knowledge should have a "
            "single authoritative representation."
        ),
    ),

    dict(
        book="The Pragmatic Programmer",
        title="Tracer Bullets",
        content=(
            "Deliver something small that works before "
            "building everything."
        ),
    ),

    # ----------------------------------------------
    # Psychology of Money
    # ----------------------------------------------

    dict(
        book="The Psychology of Money",
        title="Behavior Matters",
        content=(
            "Financial success depends more on behavior "
            "than intelligence."
        ),
    ),

    dict(
        book="The Psychology of Money",
        title="Compounding",
        content=(
            "Long-term consistency beats short-term brilliance."
        ),
    ),

    dict(
        book="The Psychology of Money",
        title="Enough",
        content=(
            "Knowing when you have enough is one of the "
            "most valuable financial skills."
        ),
    ),

    # ----------------------------------------------
    # Animal Farm
    # ----------------------------------------------

    dict(
        book="Animal Farm",
        title="Power Changes Language",
        content=(
            "The manipulation of language slowly changes "
            "how people perceive reality."
        ),
    ),

    dict(
        book="Animal Farm",
        title="Equality",
        content=(
            "Some are always tempted to rewrite the rules "
            "once they gain power."
        ),
    ),

    # ----------------------------------------------
    # Almond
    # ----------------------------------------------

    dict(
        book="Almond",
        title="Emotional Growth",
        content=(
            "The protagonist learns emotions through "
            "relationships rather than instinct."
        ),
    ),

]

# ==================================================
# QUOTES
# ==================================================

QUOTES = [

    # ----------------------------------------------
    # Atomic Habits
    # ----------------------------------------------

    dict(
        book="Atomic Habits",
        page=27,
        content="You do not rise to the level of your goals. You fall to the level of your systems.",
    ),

    dict(
        book="Atomic Habits",
        page=61,
        content="Habits are the compound interest of self-improvement.",
    ),

    dict(
        book="Atomic Habits",
        page=104,
        content="Every action you take is a vote for the type of person you wish to become.",
    ),

    dict(
        book="Atomic Habits",
        page=198,
        content="Success is the product of daily habits, not once-in-a-lifetime transformations.",
    ),

    # ----------------------------------------------
    # Deep Work
    # ----------------------------------------------

    dict(
        book="Deep Work",
        page=31,
        content="Clarity about what matters provides clarity about what does not.",
    ),

    dict(
        book="Deep Work",
        page=143,
        content="Who you are, what you think, feel, and do is the sum of what you focus on.",
    ),

    dict(
        book="Deep Work",
        page=218,
        content="A distracted mind is rarely a productive mind.",
    ),

    # ----------------------------------------------
    # The Psychology of Money
    # ----------------------------------------------

    dict(
        book="The Psychology of Money",
        page=45,
        content="Doing well with money has little to do with how smart you are.",
    ),

    dict(
        book="The Psychology of Money",
        page=78,
        content="The highest form of wealth is the ability to wake up every morning and say, I can do whatever I want today.",
    ),

    dict(
        book="The Psychology of Money",
        page=112,
        content="Enough is realizing that an insatiable appetite will push you to regret.",
    ),

    # ----------------------------------------------
    # The Pragmatic Programmer
    # ----------------------------------------------

    dict(
        book="The Pragmatic Programmer",
        page=23,
        content="Care about your craft.",
    ),

    dict(
        book="The Pragmatic Programmer",
        page=45,
        content="Don't live with broken windows.",
    ),

    dict(
        book="The Pragmatic Programmer",
        page=67,
        content="Program close to the problem domain.",
    ),

    # ----------------------------------------------
    # Animal Farm
    # ----------------------------------------------

    dict(
        book="Animal Farm",
        page=12,
        content="All animals are equal, but some animals are more equal than others.",
    ),

    dict(
        book="Animal Farm",
        page=34,
        content="The creatures outside looked from pig to man, and from man to pig.",
    ),

    # ----------------------------------------------
    # Almond
    # ----------------------------------------------

    dict(
        book="Almond",
        page=56,
        content="Not every emotion can be explained with words.",
    ),

    dict(
        book="Almond",
        page=89,
        content="Sometimes understanding another person begins with listening.",
    ),

    # ----------------------------------------------
    # Educated
    # ----------------------------------------------

    dict(
        book="Educated",
        page=102,
        content="An education is not so much about making a living as making a person.",
    ),

    # ----------------------------------------------
    # The Little Prince
    # ----------------------------------------------

    dict(
        book="The Little Prince",
        page=45,
        content="It is only with the heart that one can see rightly.",
    ),

    dict(
        book="The Little Prince",
        page=67,
        content="What is essential is invisible to the eye.",
    ),

]

# ==================================================
# SEED FUNCTIONS
# ==================================================

def seed_database():

    session = SessionLocal()

    try:

        # ------------------------------------------
        # Prevent duplicate demo data
        # ------------------------------------------

        if session.query(Book).count() > 0:

            print(
                "Database already contains data. "
                "Skipping demo seed."
            )

            return

        # ------------------------------------------
        # Seed order
        # ------------------------------------------

        seed_books(
            session
        )

        seed_sessions(
            session
        )

        seed_notes(
            session
        )

        seed_quotes(
            session
        )

        session.commit()

        print(
            "Demo database seeded successfully."
        )

    except Exception:

        session.rollback()

        raise

    finally:

        session.close()

def seed_books(
    session,
):

    books = []

    for data in BOOKS:

        book = Book(
            **data
        )

        books.append(
            book
        )

    session.add_all(
        books
    )

    session.flush()

    print(
        f"Seeded {len(books)} books."
    )

def seed_sessions(
    session,
):

    # ------------------------------------------
    # Build book lookup
    # ------------------------------------------

    books = {

        book.title: book

        for book in session.query(Book).all()

    }

    now = datetime.now()

    sessions = []

    # ------------------------------------------
    # Create reading sessions
    # ------------------------------------------

    for data in SESSIONS:

        book = books.get(
            data["book"]
        )

        if book is None:

            continue

        ended_at = (
            now
            - timedelta(
                days=data["days_ago"]
            )
        )

        started_at = (
            ended_at
            - timedelta(
                minutes=data["minutes"]
            )
        )

        sessions.append(

            ReadingSession(

                book_id=book.id,

                start_page=data["start"],

                end_page=data["end"],

                duration_minutes=data["minutes"],

                started_at=started_at,

                ended_at=ended_at,

            )

        )

    session.add_all(
        sessions
    )

    session.flush()

    print(
        f"Seeded {len(sessions)} reading sessions."
    )

def seed_notes(
    session,
):

    # ------------------------------------------
    # Build book lookup
    # ------------------------------------------

    books = {

        book.title: book

        for book in session.query(Book).all()

    }

    notes = []

    # ------------------------------------------
    # Create notes
    # ------------------------------------------

    for data in NOTES:

        book = books.get(
            data["book"]
        )

        if book is None:

            continue

        notes.append(

            Note(

                book_id=book.id,

                title=data["title"],

                content=data["content"],

            )

        )

    session.add_all(
        notes
    )

    session.flush()

    print(
        f"Seeded {len(notes)} notes."
    )

def seed_quotes(
    session,
):

    # ------------------------------------------
    # Build book lookup
    # ------------------------------------------

    books = {

        book.title: book

        for book in session.query(Book).all()

    }

    quotes = []

    # ------------------------------------------
    # Create quotes
    # ------------------------------------------

    for data in QUOTES:

        book = books.get(
            data["book"]
        )

        if book is None:

            continue

        quotes.append(

            Quote(

                book_id=book.id,

                content=data["content"],

                page=data["page"],

            )

        )

    session.add_all(
        quotes
    )

    session.flush()

    print(
        f"Seeded {len(quotes)} quotes."
    )

# ==================================================
# MAIN
# ==================================================

if __name__ == "__main__":

    seed_database()