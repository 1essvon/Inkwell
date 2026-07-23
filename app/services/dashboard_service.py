from datetime import date, timedelta

from app.constants.book_status import BookStatus

from app.services.book_service import BookService
from app.services.settings_service import SettingsService
from app.services.statistics_service import StatisticsService


class DashboardService:

    # ==================================================
    # Dashboard
    # ==================================================

    @staticmethod
    def get_dashboard_data():

        return {

            "continue_reading":
                DashboardService.get_continue_reading(),

            "reading_goal":
                DashboardService.get_reading_goal(),

            "reading_streak":
                DashboardService.get_reading_streak(),

            "summary":
                DashboardService.get_summary(),

            "library_summary":
                DashboardService.get_library_summary(),

            "recent_books":
                DashboardService.get_recent_books(),

        }

    # ==================================================
    # Continue Reading
    # ==================================================

    @staticmethod
    def get_continue_reading():

        #
        # Data
        #

        book = BookService.get_current_reading()

        if not book:

            return None

        current_page = book.current_page or 0

        total_pages = book.page_count or 0

        #
        # Business Rule
        #

        percentage = 0

        if total_pages > 0:

            percentage = round(
                current_page / total_pages * 100
            )

        progress_text = (
            f"{current_page} / {total_pages} pages"
        )

        if percentage == 100:

            status = "Finished reading 🎉"

        elif percentage >= 75:

            status = "Almost there!"

        elif percentage >= 50:

            status = "Keep going!"

        elif percentage >= 25:

            status = "Good progress."

        else:

            status = "Just getting started."

        #
        # ViewModel
        #

        return {

            "title":
                book.title,

            "author":
                book.author,

            "current_page":
                current_page,

            "total_pages":
                total_pages,

            "percentage":
                percentage,

            "progress_text":
                progress_text,

            "status":
                status,

        }

    # ==================================================
    # Reading Goal
    # ==================================================

    @staticmethod
    def get_reading_goal():

        #
        # Data
        #

        settings = SettingsService.get()

        summary = BookService.get_status_summary()

        goal = settings.reading_goal_books or 0

        completed = summary.get(
            BookStatus.COMPLETED,
            0,
        )

        #
        # Business Rule
        #

        if goal <= 0:

            status = "No reading goal configured"

            remaining = 0

        else:

            remaining = max(
                goal - completed,
                0,
            )

            if remaining == 0:

                status = "Goal achieved! 🎉"

            else:

                status = (
                    f"{remaining} book(s) remaining"
                )

        #
        # ViewModel
        #

        return {

            "completed":
                completed,

            "goal":
                goal,

            "remaining":
                remaining,

            "status":
                status,

        }

    # ==================================================
    # Reading Streak
    # ==================================================

    @staticmethod
    def get_reading_streak():

        #
        # Data
        #

        statistics = StatisticsService.get_statistics()

        streak = statistics.get(
            "reading_streak",
            0,
        )

        best = statistics.get(
            "best_streak",
            0,
        )

        last_read = statistics.get(
            "last_read",
        )

        today = date.today()

        yesterday = today - timedelta(
            days=1,
        )

        #
        # Business Rule
        #

        if streak == 0:

            status = "Let's start today."

        elif streak < 7:

            status = "Nice start!"

        elif streak < 30:

            status = "You're building a habit."

        elif streak < 100:

            status = "Amazing consistency!"

        else:

            status = "You're unstoppable!"

        if last_read is None:

            last_text = "Never"

        elif last_read == today:

            last_text = "Today"

        elif last_read == yesterday:

            last_text = "Yesterday"

        else:

            last_text = last_read.strftime(
                "%d %b %Y"
            )

        #
        # ViewModel
        #

        return {

            "current":
                f"{streak} days",

            "best":
                f"{best} days",

            "last_read":
                last_text,

            "status":
                status,

        }

    # ==================================================
    # Summary
    # ==================================================

    @staticmethod
    def get_summary():

        statistics = StatisticsService.get_statistics()

        return {

            "books":
                statistics["books"],

            "notes":
                statistics["notes"],

            "quotes":
                statistics["quotes"],

            "sessions":
                statistics["reading_sessions"],

            "pages_read":
                statistics["pages_read"],

            "reading_minutes":
                statistics["reading_minutes"],

        }

    # ==================================================
    # Library Summary
    # ==================================================

    @staticmethod
    def get_library_summary():

        #
        # Data
        #

        summary = BookService.get_status_summary()

        #
        # ViewModel
        #

        return {

            "reading":
                summary.get(
                    BookStatus.READING,
                    0,
                ),

            "want_to_read":
                summary.get(
                    BookStatus.WANT_TO_READ,
                    0,
                ),

            "completed":
                summary.get(
                    BookStatus.COMPLETED,
                    0,
                ),

            "paused":
                summary.get(
                    BookStatus.PAUSED,
                    0,
                ),

            "dropped":
                summary.get(
                    BookStatus.DROPPED,
                    0,
                ),

        }

    # ==================================================
    # Recent Books
    # ==================================================

    @staticmethod
    def get_recent_books():

        #
        # Data
        #

        books = BookService.get_recent_books()

        #
        # ViewModel
        #

        return [

            {

                "title":
                    book.title,

                "author":
                    book.author,

            }

            for book in books

        ]