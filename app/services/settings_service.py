from app.database.session import (
    SessionLocal
)

from app.models.app_settings import (
    AppSettings
)


class SettingsService:

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

    @staticmethod
    def save(

        theme,
        autosave,
        confirm_clear

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

            session.commit()

        finally:

            session.close()

    @staticmethod
    def reset():

        SettingsService.save(

            theme="Dark",

            autosave=False,

            confirm_clear=True

        )