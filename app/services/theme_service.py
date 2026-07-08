from pathlib import Path

from app.services.settings_service import (
    SettingsService,
)


class ThemeService:

    @staticmethod
    def get_theme_name():

        settings = SettingsService.get()

        return settings.theme.lower()

    @staticmethod
    def load_theme():

        theme = ThemeService.get_theme_name()

        theme_file = (

            Path(__file__).parent.parent
            / "styles"
            / f"{theme}.qss"

        )

        if not theme_file.exists():

            theme_file = (

                Path(__file__).parent.parent
                / "styles"
                / "dark.qss"

            )

        return theme_file.read_text(
            encoding="utf-8"
        )

    @staticmethod
    def apply_theme(app):

        app.setStyleSheet(

            ThemeService.load_theme()

        )