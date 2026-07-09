from app.database.session import (
    SessionLocal,
)

from app.models.app_settings import (
    AppSettings,
)


class SettingsService:

    # ==========================
    # Get
    # ==========================

    @staticmethod
    def get():

        session = SessionLocal()

        try:

            settings = (

                session.query(
                    AppSettings
                ).first()

            )

            if settings is None:

                settings = AppSettings()

                session.add(
                    settings
                )

                session.commit()

                session.refresh(
                    settings
                )

            return settings

        finally:

            session.close()

    # ==========================
    # Save
    # ==========================

    @staticmethod
    def save(

        theme,
        autosave,
        confirm_clear,
        reading_goal_books,
        reading_goal_pages,

    ):

        session = SessionLocal()

        try:

            settings = (

                session.query(
                    AppSettings
                ).first()

            )

            if settings is None:

                settings = AppSettings()

                session.add(
                    settings
                )

            settings.theme = theme

            settings.autosave_scratchpad = autosave

            settings.confirm_before_clear = (
                confirm_clear
            )

            settings.reading_goal_books = (
                reading_goal_books
            )

            settings.reading_goal_pages = (
                reading_goal_pages
            )

            session.commit()

        finally:

            session.close()

    # ==========================
    # Reset
    # ==========================

    @staticmethod
    def reset():

        SettingsService.save(

            theme="Dark",

            autosave=False,

            confirm_clear=True,

            reading_goal_books=20,

            reading_goal_pages=30,

        )