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

        return settings.theme.lower()

    @staticmethod
    def load_theme():

        return load_styles()

    @staticmethod
    def apply_theme(app):

        app.setStyleSheet(

            ThemeService.load_theme()

        )