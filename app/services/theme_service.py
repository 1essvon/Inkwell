from pathlib import Path

from app.services.settings_service import (
    SettingsService,
)
from app.styles.load_styles import (
    load_styles,
)

class ThemeService:

    @staticmethod
    def get_theme_name():

        settings = SettingsService.get()
        theme_name = getattr(settings, "theme", None)

        if not isinstance(theme_name, str):
            return "dark"

        theme_name = theme_name.strip().lower()

        if theme_name != "dark":
            return "dark"

        return theme_name

    @staticmethod
    def load_theme():

        theme_name = ThemeService.get_theme_name()
        theme_loaders = {
            "dark": load_styles,
        }

        return theme_loaders.get(
            theme_name,
            load_styles,
        )()

    @staticmethod
    def apply_theme(app):

        app.setStyleSheet(

            ThemeService.load_theme()

        )
